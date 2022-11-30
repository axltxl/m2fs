# -*- coding: utf-8 -*-

import math

from midi2sim import midi, simc
from midi2sim.midi import NoteMessage, ControlChangeMessage
from midi2sim.midi import TYPE_NOTE, TYPE_CC, TYPE_PITCHWHEEL
from midi2sim.utils import arturia

# MIDI device for this configuration
MIDI_PORT_IN = "Arturia MiniLab mkII 0"

# Some basics for making life easier
KNOB_MODE = arturia.ENC_MODE_REL_1

KNOB_01_SHIFT = midi.CC_041
KNOB_09_SHIFT = midi.CC_042

KNOB_01_SWITCH = midi.NOTE_113
KNOB_09_SWITCH = midi.NOTE_115

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


def ap_hdg_incdec(m: ControlChangeMessage) -> None:
    """Heading bug (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        # m.value, evt_cw="HEADING_BUG_INC", evt_ccw="HEADING_BUG_DEC", mode=KNOB_MODE
        m.value,
        evt_cw="MobiFlight.WT_CJ4_AP_HDG_INC",
        evt_ccw="MobiFlight.WT_CJ4_AP_HDG_DEC",
        mode=KNOB_MODE,
    )


def ap_hdg_set(m: NoteMessage) -> None:
    """Heading bug set"""

    simc.send_event("MobiFlight.WT_CJ4_AP_HDG_SYNC")


def ap_hdg_toggle(m: NoteMessage) -> None:
    """Heading mode toggle"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_HDG_PRESSED")


def ap_alt_incdec(m: ControlChangeMessage) -> None:
    """AP Altitude bug (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value, evt_cw="AP_ALT_VAR_INC", evt_ccw="AP_ALT_VAR_DEC", mode=KNOB_MODE
    )


def ap_alt_toggle(m: NoteMessage):
    """Toggle ALT HOLD mode"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_ALT_PRESSED")


def ap_vs_toggle(m: NoteMessage):
    """Toggle VS mode"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_VS_PRESSED")


def ap_vs_incdec(m: ControlChangeMessage) -> None:
    """VS Mode knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.WT_CJ4_AP_VS_INC",
        evt_ccw="MobiFlight.WT_CJ4_AP_VS_DEC",
    )


def ap_flc_toggle(m: NoteMessage):
    """Toggle flc mode"""

    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_FLC_PRESSED")


def ap_flc_incdec(m: ControlChangeMessage) -> None:
    """flc Mode knob (+/-)"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="AP_SPD_VAR_INC",
        evt_ccw="AP_SPD_VAR_DEC",
    )


# FIXME: doc variables reference
# source: mobiflight events for this aircraft here: https://github.com/MobiFlight/MobiFlight-WASM-Module/blob/main/src/Sources/Code/events.txt#L4641
# official docs about the Working title Cj4 here: https://www.workingtitle.aero/packages/cj4/guides/simvars


def ap_toggle(m: NoteMessage):
    """Toggle autopilot"""

    if m.on:
        simc.send_event("AP_MASTER")


def yawdamper_toggle(m: NoteMessage) -> None:
    """Toggle yaw damper"""

    if m.on:
        simc.send_event("YAW_DAMPER_TOGGLE")


def lights_panel_incdec(m: ControlChangeMessage) -> None:
    """Panel lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.WT_CJ4_PANEL_LIGHTS_INC",
        evt_ccw="MobiFlight.WT_CJ4_PANEL_LIGHTS_DEC",
    )


def lights_cabin_incdec(m: ControlChangeMessage) -> None:
    """Panel lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.WT_CJ4_CABIN1_LIGHT_INC",
        evt_ccw="MobiFlight.WT_CJ4_CABIN1_LIGHT_DEC",
    )


def lights_flood_incdec(m: ControlChangeMessage) -> None:
    """Flood lights potentiometer"""

    arturia.send_evt_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.WT_CJ4_FLOOD_LIGHT_INC",
        evt_ccw="MobiFlight.WT_CJ4_FLOOD_LIGHT_DEC",
    )


def lights_displays_incdec(m: ControlChangeMessage) -> None:
    """Display lights potentiometer (MFD and PFD)"""

    light_events = [
        ("MobiFlight.WT_CJ4_MFD1_LIGHT_INC", "MobiFlight.WT_CJ4_MFD1_LIGHT_DEC"),
        ("MobiFlight.WT_CJ4_MFD2_LIGHT_INC", "MobiFlight.WT_CJ4_MFD2_LIGHT_DEC"),
        ("MobiFlight.WT_CJ4_PFD1_LIGHT_INC", "MobiFlight.WT_CJ4_PFD1_LIGHT_DEC"),
        ("MobiFlight.WT_CJ4_PFD2_LIGHT_INC", "MobiFlight.WT_CJ4_PFD2_LIGHT_DEC"),
    ]

    for event in light_events:
        arturia.send_evt_on_encoder_rotation(
            m.value,
            mode=KNOB_MODE,
            evt_cw=event[0],
            evt_ccw=event[1],
        )


# FIXME: doc me
def ap_lnav_toggle(m: ControlChangeMessage):
    # WT_CJ4_AP_NAV_PRESSED
    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_NAV_PRESSED")


def ap_vnav_toggle(m: NoteMessage):
    # WT_CJ4_AP_VNAV_PRESSED
    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_VNAV_PRESSED")


def ap_appr_toggle(m: NoteMessage):
    # WT_CJ4_AP_APPR_PRESSED
    if m.on:
        simc.send_event("MobiFlight.WT_CJ4_AP_APPR_PRESSED")


def baro_toggle(m: NoteMessage):
    pass


def baro_incdec(m: ControlChangeMessage):

    for i in range(1, 4):
        arturia.send_evt_on_encoder_rotation(
            m.value,
            mode=KNOB_MODE,
            evt_cw=f"MobiFlight.WT_CJ4_BARO{i}_INC",
            evt_ccw=f"MobiFlight.WT_CJ4_BARO{i}_DEC",
        )


def on_autopilot_change(v: simc.SimVar) -> None:
    # FIXME: doc me
    print("HOLA")


# FIXME: doc me
def batch_assign_handlers(binding_map: list[tuple]):
    for binding in binding_map:
        t, i, h = binding
        if t == TYPE_CC:
            midi.subscribe_to_cc(cc=i, handler=h)
        if t == TYPE_NOTE:
            midi.subscribe_to_note(note=i, handler=h)
        if t == TYPE_PITCHWHEEL:
            midi.subscribe_to_pitchwheel(handler=h)


def on_init() -> None:
    if simc.get_backend() != simc.SIMCONNECT_BACKEND_MOBIFLIGHT:
        raise Exception(
            f"Only '{simc.SIMCONNECT_BACKEND_MOBIFLIGHT_NAME}' is supported in this config!"
        )

    # FIXME: doc me
    # ----------------------
    midi.connect_input_port(name=MIDI_PORT_IN)

    batch_assign_handlers(
        [
            # AP Panel handlers
            # ----------------------
            (TYPE_NOTE, PAD_08, ap_toggle),  # AP master switch
            (TYPE_NOTE, PAD_07, yawdamper_toggle),  # Yaw damper toggle
            (TYPE_CC, KNOB_01, baro_incdec),  # Barometer knobs
            # ALT
            (TYPE_CC, KNOB_14, ap_alt_incdec),  # AP ALT inc/dec
            (TYPE_NOTE, PAD_06, ap_alt_toggle),  # AP ALT toggle
            # FLC
            (TYPE_NOTE, PAD_05, ap_flc_toggle),
            (TYPE_CC, KNOB_13, ap_flc_incdec),  #
            # VS
            (TYPE_NOTE, PAD_04, ap_vs_toggle),  # AP VS toggle
            (TYPE_CC, KNOB_12, ap_vs_incdec),  # AP VS increment/decrement
            # HDG
            (TYPE_NOTE, PAD_01, ap_hdg_toggle),  # AP heading mode toggle
            (TYPE_NOTE, KNOB_09_SWITCH, ap_hdg_set),  # AP heading mode toggle
            (TYPE_CC, KNOB_09, ap_hdg_incdec),  # AP VS increment/decrement
            # Navigation
            (TYPE_NOTE, PAD_09, ap_lnav_toggle),  # LNAV
            (TYPE_NOTE, PAD_10, ap_vnav_toggle),  # VNAV
            (TYPE_NOTE, PAD_11, ap_appr_toggle),  # Approach mode
            # Lights section
            # ----------------------
            # Master lights
            (TYPE_CC, KNOB_08, lights_panel_incdec),  # Lights (panel)
            (TYPE_CC, KNOB_07, lights_cabin_incdec),  # Lights (cabin)
            (TYPE_CC, KNOB_06, lights_flood_incdec),  # Lights (flood lights)
            (TYPE_CC, KNOB_05, lights_displays_incdec),  # Lights (PFD and MFD)
        ]
    )
