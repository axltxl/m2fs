# -*- coding: utf-8 -*-

import midi
import flightsim
import log

# MIDI device for this configuration
# MIDI_PORT = "Arturia MiniLab mkII 0"
MIDI_PORT = "LPX MIDI 1"
MIDI_PORTS = [

]


def hdg_incdec(m):
    """Default CC handler"""

    log.info("hello from hdg_incdec :)")
    return (midi.MIDI_MSG_SUCCESS, "")


def note_middlec_example(m):
    """Example note handler using middle C key"""

    log.info("!!!! MIDDLE C !!!! Hello from config! :)")
    return (midi.MIDI_MSG_SUCCESS, "")


def note_middlecsh_example(m):
    """Example note handler using middle C key"""

    log.info("!!!! MIDDLE C# !!!! Hello from config! :)")
    return (midi.MIDI_MSG_SUCCESS, "")


def on_init() -> None:
    # CC handlers
    midi.set_cc_handler(cc=midi.CC_112, handler=hdg_incdec)

    # Note handlers
    midi.set_note_handler(note=midi.NOTE_060, handler=note_middlec_example)
    midi.set_note_handler(note=midi.NOTE_061, handler=note_middlecsh_example)

# FIXME remove me
# MIDI_CC_HANDLERS = {
#     midi.CC_112: hdg_incdec
# }

# MIDI_NOTE_HANDLERS = {
#     midi.NOTE_060: note_middlec_example,
#     midi.NOTE_061: note_middlecsh_example
# }


# def example_cc
