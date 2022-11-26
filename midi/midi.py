# -*- coding: utf-8 -*-
import mido
import log

from .message import Message
from .cc import (
    ControlChangeMessage,
    bootstrap as cc_bootstrap,
    get_handler as cc_get_handler
)
from .note import (
    NoteMessage,
    bootstrap as note_bootstrap,
    get_handler as note_get_handler,
)



def __bootstrap():
    """Initialize MIDI backend (mido)"""

    # Make sure we're using rtmidi backend
    mido.set_backend('mido.backends.rtmidi')

    # Initialize CC and Note subsystems
    cc_bootstrap()
    note_bootstrap()



def list_ports() -> dict:
    """List all physical MIDI ports (devices)"""

    return {
        'input': mido.get_input_names(),
        'output': mido.get_output_names(),
        'io': mido.get_ioport_names()
    }


def __get_midi_message(msg) -> Message:
    """
    Create a Message-based object from a mido MIDI message.
    Returns None if message type is not supported
    """
    handler_msg = None

    if msg.type == 'control_change'  \
            or msg.type == 'note_on' or msg.type == 'note_off':

        # Convert CC messages to proper ControlChangeMessage
        if msg.type == 'control_change':
            handler_msg = ControlChangeMessage(id=msg.control)
            handler_msg.value = msg.value

        # Convert note messages from mido to proper NoteMessage
        elif msg.type == 'note_on' or msg.type == 'note_off':
            note_on = False if msg.type == 'note_off' else True
            handler_msg = NoteMessage(
                id=msg.note, velocity=msg.velocity, on=note_on)

        # Set channel appropriately (this applies to all cases)
        handler_msg.channel = msg.channel
    return handler_msg


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
        elif m.type == Message.TYPE_NOTE:
            note_get_handler(note=m.id)(m)
        else:
            log.warn(f'(mido) {msg.type}: MIDI message type not supported')


def message_pump(*, port_name: str, setup_func: callable) -> None:
    """Main MIDI event message pump"""

    # Intialize MIDI backend
    __bootstrap()

    # FIXME: doc me
    setup_func()

    # Open the port for input and output and process messages
    with mido.open_input(port_name) as port:
        for msg in port:
            __handle_msg(msg)
