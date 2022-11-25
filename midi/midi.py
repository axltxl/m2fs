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

# FIXME: doc me
__midi_port = ""

# FIXME: doc me


# Make sure we're using rtmidi backend
mido.set_backend('mido.backends.rtmidi')


def set_port(port: str) -> None:
    global __midi_port
    __midi_port = port


def list_ports() -> dict:
    """List all physical MIDI ports (devices)"""

    return {
        'input': mido.get_input_names(),
        'output': mido.get_output_names(),
        'io': mido.get_ioport_names()
    }


# FIXME: doc me
def __get_midi_message(msg) -> Message:
    callback_msg = None
    if msg.type == 'control_change' or msg.type == 'note_on' or msg.type == 'note_off':
        if msg.type == 'control_change':
            callback_msg = ControlChangeMessage(id=msg.control)
            callback_msg.value = msg.value
        else:
            callback_msg = NoteMessage(id=msg.note, velocity=msg.velocity)
        callback_msg.channel = msg.channel
    return callback_msg


# FIXME: doc me
def __handle_msg(msg) -> int:
    m = __get_midi_message(msg)
    if m is not None:
        if m.type == Message.TYPE_CC:
            return cc_get_handler(cc=m.id)(m)
    log.warn(f'(mido) {msg.type}: MIDI message type not supported')


def message_pump() -> None:
    # FIXME: doc me
    cc_bootstrap()

    # FIXME: doc me
    with mido.open_ioport(__midi_port) as port:
        for msg in port:
            if __handle_msg(msg):
                log.warn("Something ain't right FIXME")
