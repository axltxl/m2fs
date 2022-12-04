# -*- coding: utf-8 -*-

import math
from m2fs import simc, midi, config

# MIDI device for this configuration
MIDI_PORT_IN = "Generic (you'd better change me buddy)"


def hdg_incdec(m):
    """Heading bug (+/-)"""

    simc.send_event("HEADING_BUG_INC")


def hdg_set(m):
    """Heading bug set"""

    current_heading = int(math.degrees(simc.get_variable("HEADING_INDICATOR").value))
    simc.send_event("HEADING_BUG_SET", current_heading)


def alt_incdec(m):
    """AP Altitude bug (+/-)"""

    simc.send_event("AP_ALT_VAR_INC")


def note_middlec_example(m):
    """Example note handler using middle C key"""

    simc.set_variable("LIGHT_STROBE", True)


def note_middlecsh_example(m):
    """Example note handler using middle C key"""
    pass


# Proceed to start up the engines
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config.setup(
    midi_input_ports=[MIDI_PORT_IN],
    midi_cc_handlers=[
        # AP Panel handlers
        # ----------------------
        # ALT
        (midi.CC_114, alt_incdec),
        # HDG
        (midi.CC_013, hdg_set),
        (midi.CC_012, hdg_incdec),
    ],
    midi_note_handlers=[
        # Middle C example
        (midi.NOTE_060, note_middlec_example),
        # Middle C# example
        (midi.NOTE_061, note_middlecsh_example),
    ],
)
