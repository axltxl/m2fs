# -*- coding: utf-8 -*-

import sys
import os
import traceback
import threading
import time

import mido

# Make sure we're using rtmidi backend
import mido.backends.rtmidi

# There are message pump threads created per each MIDI input
# port specified on config. Each one of those
# polling for input indefinitely at the frequency
# set here
MIDI_IN_THREAD_SLEEP_TIME = 1.0 / 66  # 66 Hz

from .log import log
from .port import cleanup as port_cleanup
from .port import get_all_input_ports
from .message import BaseMessage
from .message import TYPE_CC, TYPE_NOTE, TYPE_PITCHWHEEL
from .cc import (
    ControlChangeMessage,
    bootstrap as cc_bootstrap,
    get_handler as cc_get_handler,
)
from .note import (
    NoteMessage,
    bootstrap as note_bootstrap,
    get_handler as note_get_handler,
)

from .pitchwheel import (
    PitchWheelMessage,
    bootstrap as pw_bootstrap,
    get_handler as pw_get_handler,
)

from .exceptions import MIDIException


__in_port_msg_pump_threads = []


def bootstrap():
    """Initialize MIDI backend (mido)"""

    # Initialize MIDI subsystems
    cc_bootstrap()
    note_bootstrap()
    pw_bootstrap()


def reset() -> None:
    """Reset MIDI engine to defaults"""

    cleanup()  # do housekeeping
    bootstrap()  # bootstrap the MIDI engine again


def __get_midi_message(msg) -> BaseMessage:
    """
    Create a Message-based object from a mido MIDI message.
    Returns None if message type is not supported
    """
    handler_msg = None

    if msg.type in ["control_change", "note_on", "note_off", "pitchwheel"]:

        # Convert CC messages to proper ControlChangeMessage
        if msg.type == "control_change":
            handler_msg = ControlChangeMessage(
                id=msg.control, value=msg.value, channel=msg.channel
            )

        # Convert note messages from mido to proper NoteMessage
        elif msg.type == "note_on" or msg.type == "note_off":
            note_on = False if msg.type == "note_off" else True
            handler_msg = NoteMessage(
                id=msg.note, velocity=msg.velocity, on=note_on, channel=msg.channel
            )

        # Convert pitch wheel messages from mido to proper PitchWheelMessage
        elif msg.type == "pitchwheel":
            handler_msg = PitchWheelMessage(value=msg.pitch, channel=msg.channel)

    return handler_msg


def __handle_except(e):
    """
    Handle (log) any exception
    """
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    log.error(
        "Unhandled {e} at {file}:{line}: '{msg}'".format(
            e=exc_type.__name__, file=fname, line=exc_tb.tb_lineno, msg=e
        )
    )
    log.error(traceback.format_exc())


def __handle_msg(msg) -> None:
    """Handle a raw mido MIDI message via a handler"""

    # Get a Message
    m = __get_midi_message(msg)

    # ... and process it accordingly depending on its type
    # NOTE: at the time of writing, only MIDI CC and NOTE_ON/NOTE_OFF messages
    # are supported
    try:
        if m is not None:
            if m.type == TYPE_CC:
                cc_get_handler(cc=m.id)(m)  # invoke CC handler
            elif m.type == TYPE_NOTE:
                note_get_handler(note=m.id)(m)  # invoke note handler
            elif m.type == TYPE_PITCHWHEEL:
                pw_get_handler()(m)  # invoke pitch wheel handler
        else:
            log.debug(f"(mido) {msg.type}: MIDI message type not supported")
    except Exception as e:
        log.error("handler errored!")
        __handle_except(e)


def cleanup() -> None:
    """Take care of business"""

    port_cleanup()
    message_pump_stop()


def __in_port_message_pump(in_port: mido.ports.BaseInput):
    """Input port message pump"""

    # Source: https://mido.readthedocs.io/en/latest/ports.html
    # > This will iterate over messages as they arrive on the port until the port closes.
    # > (So far only socket ports actually close by themselves. This happens if the other end disconnects.)
    # for msg in in_port:
    #     __handle_msg(msg)

    # > This will iterate over all messages that have already arrived.
    # > It is typically used in main loops where you want to do something
    # > else while you wait for messages:
    while not in_port.closed:
        for msg in in_port.iter_pending():
            __handle_msg(msg)
        time.sleep(
            MIDI_IN_THREAD_SLEEP_TIME
        )  # so, it does not eat CPU time unnecessarily


def message_pump_stop() -> None:
    """Stop all MIDI input port message pump threads"""

    global __in_port_msg_pump_threads
    for t in __in_port_msg_pump_threads:
        log.debug(f"stopping message pump thread: {t.getName()}")
        try:
            t.join()
        except RuntimeError:
            pass
    __in_port_msg_pump_threads = []
    log.debug("stopped all message pump threads")


def message_pump_start() -> None:
    """Main MIDI event message pump"""

    global __in_port_msg_pump_threads

    for port in get_all_input_ports():

        log.debug(f"{port.name}: starting message pump thread")

        # Start a separate thread per input port
        # (set to daemon, so it doesn't need to be explicitely dealt with
        # when exiting)
        # NOTE: consider a ThreadPoolExecutor in the future
        msg_pump_thread = threading.Thread(target=__in_port_message_pump, args=(port,))
        msg_pump_thread.setName(name=f"midi:in_port:{port.name}")
        msg_pump_thread.start()

        __in_port_msg_pump_threads.append(msg_pump_thread)
