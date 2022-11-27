# -*- coding: utf-8 -*-

import sys
import os
import traceback

import mido
import log

from .port import cleanup as port_cleanup
from .port import get_input_port
from .message import Message
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
from .exceptions import MIDIException


def __bootstrap():
    """Initialize MIDI backend (mido)"""

    # Make sure we're using rtmidi backend
    mido.set_backend("mido.backends.rtmidi")

    # Initialize CC and Note subsystems
    cc_bootstrap()
    note_bootstrap()


def __get_midi_message(msg) -> Message:
    """
    Create a Message-based object from a mido MIDI message.
    Returns None if message type is not supported
    """
    handler_msg = None

    if msg.type == "control_change" or msg.type == "note_on" or msg.type == "note_off":

        # Convert CC messages to proper ControlChangeMessage
        if msg.type == "control_change":
            handler_msg = ControlChangeMessage(id=msg.control)
            handler_msg.value = msg.value

        # Convert note messages from mido to proper NoteMessage
        elif msg.type == "note_on" or msg.type == "note_off":
            note_on = False if msg.type == "note_off" else True
            handler_msg = NoteMessage(id=msg.note, velocity=msg.velocity, on=note_on)

        # Set channel appropriately (this applies to all cases)
        handler_msg.channel = msg.channel
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
            if m.type == Message.TYPE_CC:
                cc_get_handler(cc=m.id)(m)  # invoke CC handler
            elif m.type == Message.TYPE_NOTE:
                note_get_handler(note=m.id)(m)  # invoke note handler
            else:
                log.warn(f"(mido) {msg.type}: MIDI message type not supported")
    except Exception as e:
        log.error(f'{"CC" if m.type == Message.TYPE_CC else "NOTE"}:{m.id} errored')
        __handle_except(e)


# FIXME: doc me
def cleanup() -> None:
    port_cleanup()


def message_pump(*, setup_func: callable) -> None:
    """Main MIDI event message pump"""

    # Intialize MIDI backend
    __bootstrap()

    # Any setting up can be done at this point
    setup_func()

    # Open the port for input and output and process messages
    # with mido.open_input(__in_port_name) as in_port:
    in_port = get_input_port()
    if in_port is not None and not in_port.closed:
        for msg in in_port:
            __handle_msg(msg)
    else:
        raise MIDIException("No input port connected")
