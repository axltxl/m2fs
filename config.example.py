# -*- coding: utf-8 -*-

import math
import midi
import flightsim

# MIDI device for this configuration
MIDI_PORT = "Generic"

def hdg_incdec(m: midi.Message) -> None:
    """Heading bug (+/-)"""

    flightsim.send_event("HEADING_BUG_INC")

def hdg_set(m: midi.Message) -> None:
    """Heading bug set (FIXME)"""

    current_heading = int(math.degrees(flightsim.get_variable("HEADING_INDICATOR").value))
    flightsim.send_event("HEADING_BUG_SET", current_heading)

def alt_incdec(m: midi.Message) -> None:
    """AP Altitude bug (+/-)"""

    flightsim.send_event("AP_ALT_VAR_INC")

def note_middlec_example(m: midi.Message) -> None:
    """Example note handler using middle C key"""

    flightsim.set_variable("LIGHT_STROBE", True)

def note_middlecsh_example(m: midi.Message):
    """Example note handler using middle C key"""
    pass




def on_init() -> None:
    # CC handlers
    midi.subscribe_to_cc(cc=midi.CC_112, handler=hdg_incdec)
    midi.subscribe_to_cc(cc=midi.CC_113, handler=hdg_set)
    midi.subscribe_to_cc(cc=midi.CC_114, handler=alt_incdec)

    # Note handlers
    midi.subscribe_to_note(note=midi.NOTE_060, handler=note_middlec_example)
    midi.subscribe_to_note(note=midi.NOTE_061, handler=note_middlecsh_example)
