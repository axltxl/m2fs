# -*- coding: utf-8 -*-
import mido
import log

from .message import Message
from .cc import (
    ControlChangeMessage,
    bootstrap as cc_bootstrap,
    get_handler as cc_get_handler
)
from .note import NoteMessage

# MIDI port (device) to be used is set here
__midi_port = ""


def __bootstrap():
    """Initialize MIDI backend (mido)"""

    # Make sure we're using rtmidi backend
    mido.set_backend('mido.backends.rtmidi')


def set_port(port: str) -> None:
    """Set MIDI port (device) to use"""

    global __midi_port
    __midi_port = port


def list_ports() -> dict:
    """List all physical MIDI ports (devices)"""

    return {
        'input': mido.get_input_names(),
        'output': mido.get_output_names(),
        'io': mido.get_ioport_names()
    }


def __get_midi_message(msg) -> Message:
    """Create a Message-based object from a mido MIDI message"""
    callback_msg = None
    if msg.type == 'control_change' or msg.type == 'note_on' or msg.type == 'note_off':
        if msg.type == 'control_change':
            callback_msg = ControlChangeMessage(id=msg.control)
            callback_msg.value = msg.value
        else:
            callback_msg = NoteMessage(id=msg.note, velocity=msg.velocity)
        callback_msg.channel = msg.channel
    return callback_msg


def __handle_msg(msg) -> None:
    """Handle a raw mido MIDI message via a handler"""

    # Get a Message
    m = __get_midi_message(msg)

    # ... and process it accordingly depending on its type
    # NOTE: at the time of writing, only MIDI CC and NOTE_ON/NOTE_OFF messages
    # are supported
    if m is not None:
        if m.type == Message.TYPE_CC:
            cc_get_handler(cc=m.id)(m)
        else:
            log.warn(f'(mido) {msg.type}: MIDI message type not supported')


def message_pump() -> None:
    """Main MIDI event message pump"""

    if not len(__midi_port):
        raise Exception("MIDI port has not been set!")

    # Initialize MIDI, first of all
    __bootstrap()
    cc_bootstrap()

    # Open the port for input and output and process messages
    with mido.open_ioport(__midi_port) as port:
        for msg in port:
            __handle_msg(msg)
