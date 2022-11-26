# -*- coding: utf-8 -*-

import midi
import flightsim

# MIDI device for this configuration
MIDI_PORT = "Arturia MiniLab mkII 0"


def hdg_incdec(m):
    """Default CC handler"""

    flightsim.send_event("HEADING_BUG_INC")
    return (midi.MIDI_MSG_SUCCESS, "")


def note_middlec_example(m):
    """Example note handler using middle C key"""

    flightsim.set_variable("LIGHT_STROBE", True)
    return (midi.MIDI_MSG_SUCCESS, "")


def note_middlecsh_example(m):
    """Example note handler using middle C key"""

    return (midi.MIDI_MSG_SUCCESS, "")


def on_init() -> None:
    # CC handlers
    midi.subscribe_to_cc(cc=midi.CC_112, handler=hdg_incdec)

    # Note handlers
    midi.subscribe_to_note(note=midi.NOTE_060, handler=note_middlec_example)
    midi.subscribe_to_note(note=midi.NOTE_061, handler=note_middlecsh_example)
