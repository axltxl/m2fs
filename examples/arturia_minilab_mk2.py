# -*- coding: utf-8 -*-

import math

from midi2sim import simc, midi
import midi2sim.utils.arturia as arturia

# MIDI device for this configuration
MIDI_PORT_IN = "Arturia MiniLab mkII 0"

# Some basics for making life easier
KNOB_MODE = arturia.ENC_MODE_REL_1

KNOB_01_SHIFT = midi.CC_041
KNOB_02_SHIFT = midi.CC_042

KNOB_01_SWITCH = midi.NOTE_113
KNOB_02_SWITCH = midi.NOTE_115

KNOB_01 = midi.CC_021
KNOB_02 = midi.CC_022
KNOB_03 = midi.CC_023
KNOB_04 = midi.CC_024
KNOB_05 = midi.CC_025
KNOB_06 = midi.CC_026
KNOB_07 = midi.CC_027
KNOB_08 = midi.CC_028
KNOB_09 = midi.CC_029
KNOB_10 = midi.CC_030
KNOB_11 = midi.CC_031
KNOB_12 = midi.CC_032
KNOB_13 = midi.CC_033
KNOB_14 = midi.CC_034
KNOB_15 = midi.CC_035
KNOB_16 = midi.CC_036

PAD_01 = midi.NOTE_036
PAD_02 = midi.NOTE_037
PAD_03 = midi.NOTE_038
PAD_04 = midi.NOTE_039
PAD_05 = midi.NOTE_040
PAD_06 = midi.NOTE_041
PAD_07 = midi.NOTE_042
PAD_08 = midi.NOTE_043
PAD_09 = midi.NOTE_044
PAD_10 = midi.NOTE_045
PAD_11 = midi.NOTE_046
PAD_12 = midi.NOTE_047
PAD_13 = midi.NOTE_048
PAD_14 = midi.NOTE_049
PAD_15 = midi.NOTE_050
PAD_16 = midi.NOTE_051


def __send_evt_on_encoder_rotation(cc_value, evt_cw, evt_ccw):
    er = arturia.get_encoder_rotation(cc_value, mode=KNOB_MODE)
    if er > 0:
        simc.send_event(evt_cw)
    elif er < 0:
        simc.send_event(evt_ccw)


def __send_evt_on_note_toggle(note, evt_on, evt_off):
    if note.on:
        simc.send_event(evt_on)
    else:
        simc.send_event(evt_off)


def ap_hdg_incdec(m: midi.ControlChangeMessage) -> None:
    """Heading bug (+/-)"""

    __send_evt_on_encoder_rotation(m.value, "HEADING_BUG_INC", "HEADING_BUG_DEC")


def ap_hdg_set(m: midi.NoteMessage) -> None:
    """Heading bug set"""

    if simc.get_backend() == simc.SIMCONNECT_BACKEND_DEFAULT:
        simvar_name = "HEADING_INDICATOR"
    if simc.get_backend() == simc.SIMCONNECT_BACKEND_MOBIFLIGHT:
        simvar_name = "(A:HEADING INDICATOR,radians)"

    current_heading = math.ceil(math.degrees(simc.get_variable(simvar_name).value))
    simc.send_event("HEADING_BUG_SET", current_heading)


def ap_hdg_mode_toggle(m: midi.NoteMessage) -> None:
    """Heading mode toggle"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_HDG_PRESSED")


def ap_alt_incdec(m: midi.ControlChangeMessage) -> None:
    """AP Altitude bug (+/-)"""

    __send_evt_on_encoder_rotation(m.value, "AP_ALT_VAR_INC", "AP_ALT_VAR_DEC")


def ap_vs_toggle(m: midi.NoteMessage):
    """Toggle VS mode"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_VS_PRESSED")


def ap_vs_incdec(m: midi.ControlChangeMessage) -> None:
    """VS Mode knob (+/-)"""

    __send_evt_on_encoder_rotation(
        m.value, "MobiFlight.WT_CJ4_AP_VS_INC", "MobiFlight.WT_CJ4_AP_VS_DEC"
    )


def ap_toggle(m: midi.NoteMessage):
    """Toggle autopilot"""

    if m.on:
        simc.send_event("AP_MASTER")


def yawdamper_toggle(m: midi.NoteMessage) -> None:
    """Toggle yaw damper"""

    if m.on:
        simc.send_event("YAW_DAMPER_TOGGLE")


def on_autopilot_change(v: simc.SimVar) -> None:
    # FIXME: doc me
    print("HOLA")


def on_init() -> None:
    # FIXME: doc me
    # ----------------------
    midi.connect_input_port(name=MIDI_PORT_IN)

    # CC handlers
    # ----------------------
    midi.subscribe_to_cc(cc=KNOB_01, handler=ap_hdg_incdec)
    midi.subscribe_to_cc(cc=KNOB_02, handler=ap_alt_incdec)
    midi.subscribe_to_cc(cc=KNOB_10, handler=ap_vs_incdec)

    # Note handlers
    # ----------------------
    midi.subscribe_to_note(note=KNOB_01_SWITCH, handler=ap_hdg_set)
    midi.subscribe_to_note(note=PAD_02, handler=ap_vs_toggle)
    midi.subscribe_to_note(note=PAD_07, handler=yawdamper_toggle)
    midi.subscribe_to_note(note=PAD_08, handler=ap_toggle)
    midi.subscribe_to_note(note=PAD_01, handler=ap_hdg_mode_toggle)

    # SimVar change handlers
    # ----------------------
    # You can subscribe a function so that it gets invoked upon a change
    # on a SimVar
    simc.subscribe_to_simvar("AUTOPILOT_MASTER", handler=on_autopilot_change)
