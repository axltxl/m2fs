# -*- coding: utf-8 -*-
"""
m2fs configuration file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MIDI controller(s):
    - Behringer X-Touch Mini
Aircraft: Airbus A320neo (FlyByWire A32nx)
Preset files for MIDI controller:
    - Layer A -> LayerA.bin
    - Layer B -> LayerB.bin
See: https://github.com/flybywiresim/aircraft/blob/master/fbw-a32nx/docs/a320-events.md
"""

from m2fs import midi, simc

from m2fs.utils import behringer
from m2fs import config

# MIDI device for this configuration
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MIDI_PORTS_IN = ["X-TOUCH MINI 0"]
MIDI_PORT_CHANNEL = 10  # 0-based, so actually 11

# Some basics  for making life easier
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Knobs section
# ----------------

# Layer A
# -------

# knobs
KNOB_A_01 = midi.CC_001
KNOB_A_02 = midi.CC_002
KNOB_A_03 = midi.CC_003
KNOB_A_04 = midi.CC_004
KNOB_A_05 = midi.CC_005
KNOB_A_06 = midi.CC_006
KNOB_A_07 = midi.CC_007
KNOB_A_08 = midi.CC_008

# knob buttons
KNOB_A_BT01 = midi.NOTE_000
KNOB_A_BT02 = midi.NOTE_001
KNOB_A_BT03 = midi.NOTE_002
KNOB_A_BT04 = midi.NOTE_003
KNOB_A_BT05 = midi.NOTE_004
KNOB_A_BT06 = midi.NOTE_005
KNOB_A_BT07 = midi.NOTE_006
KNOB_A_BT08 = midi.NOTE_007

# Buttons panel
BT_A_01 = midi.NOTE_008
BT_A_02 = midi.NOTE_009
BT_A_03 = midi.NOTE_010
BT_A_04 = midi.NOTE_011
BT_A_05 = midi.NOTE_012
BT_A_06 = midi.NOTE_013
BT_A_07 = midi.NOTE_014
BT_A_08 = midi.NOTE_015
BT_A_09 = midi.NOTE_016
BT_A_10 = midi.NOTE_017
BT_A_11 = midi.NOTE_018
BT_A_12 = midi.NOTE_019
BT_A_13 = midi.NOTE_020
BT_A_14 = midi.NOTE_021
BT_A_15 = midi.NOTE_022
BT_A_16 = midi.NOTE_023

# slider
SLIDER_A = midi.CC_009

# Layer B
# -------

# knobs
KNOB_B_01 = midi.CC_011
KNOB_B_02 = midi.CC_012
KNOB_B_03 = midi.CC_013
KNOB_B_04 = midi.CC_014
KNOB_B_05 = midi.CC_015
KNOB_B_06 = midi.CC_016
KNOB_B_07 = midi.CC_017
KNOB_B_08 = midi.CC_018

# knob buttons (when pressed down)
KNOB_B_BT01 = midi.CC_031
KNOB_B_BT02 = midi.CC_032
KNOB_B_BT03 = midi.CC_033
KNOB_B_BT04 = midi.CC_034
KNOB_B_BT05 = midi.CC_035
KNOB_B_BT06 = midi.CC_036
KNOB_B_BT07 = midi.CC_037
KNOB_B_BT08 = midi.CC_038

# Buttons panel
BT_B_01 = midi.NOTE_032
BT_B_02 = midi.NOTE_033
BT_B_03 = midi.NOTE_034
BT_B_04 = midi.NOTE_035
BT_B_05 = midi.NOTE_036
BT_B_06 = midi.NOTE_037
BT_B_07 = midi.NOTE_038
BT_B_08 = midi.NOTE_039
BT_B_09 = midi.NOTE_040
BT_B_10 = midi.NOTE_041
BT_B_11 = midi.NOTE_042
BT_B_12 = midi.NOTE_043
BT_B_13 = midi.NOTE_044
BT_B_14 = midi.NOTE_045
BT_B_15 = midi.NOTE_046
BT_B_16 = midi.NOTE_047

# slider
SLIDER_B = midi.CC_010

#############################
# Easy logical bindings
# so I don't have to hardcode
# CCs/notes into config.setup
#############################
# Master button for hot reload (Layer B)
CONFIG_RELOAD_BT = BT_B_16

# Main knob mode (I have chosen Relative 1 for all of my knobs)
KNOB_MODE = behringer.ENC_MODE_REL_1

# Autopilot master
AP1_MASTER_BT = BT_A_09

# Heading bug (HDG)
AP_HDG_INCDEC_KNOB = KNOB_A_03
AP_HDG_PUSH_BT = KNOB_A_BT03  # heading mode (AP, push)
AP_HDG_PULL_BT = BT_A_03  # heading mode (AP, pull)

# Altitude hold bug (ALT)
AP_ALT_INCDEC_KNOB = KNOB_A_02
AP_ALT_INC_TOGGLE_BT = BT_A_10
AP_ALT_PUSH_BT = KNOB_A_BT02
AP_ALT_PULL_BT = BT_A_02

# NAV button (it doesn't exists in this aircraft)
# it's just a commodity and only imitates what
# AP_HDG_PUSH_BT does
AP_NAV_BT = BT_A_11

# Vertical speed (VS)
AP_VS_INCDEC_KNOB = KNOB_A_04
AP_VS_PUSH_BT = KNOB_A_BT04
AP_VS_PULL_BT = BT_A_04

# Flight Level Control (SPD)
AP_SPD_INCDEC_KNOB = KNOB_A_05
AP_SPD_PUSH_BT = KNOB_A_BT05
AP_SPD_PULL_BT = BT_A_05

# APPROACH
AP_APPR_BT = BT_A_16

# Barometer bug (BARO)
BARO_INCDEC_KNOB = KNOB_A_01
BARO_STD_BT = KNOB_A_BT01
ap_baro_switch = False


# MIDI CC and NOTE handlers used on this aircraft
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def ap_hdg_incdec(m):
    """Heading bug (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        evt_cw="HEADING_BUG_INC",
        evt_ccw="HEADING_BUG_DEC",
        mode=KNOB_MODE,
    )


def ap_hdg_pull(m):
    """Heading mode (pull)"""

    if m.on:
        simc.send_event("MobiFlight.HDG_Pull")


def ap_hdg_push(m):
    """Heading mode (push)"""

    if m.on:
        simc.send_event("MobiFlight.HDG_Push")


def ap_alt_incdec(m):
    """AP Altitude bug (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        evt_cw="MobiFlight.A32NX_FCU_ALT_INC",
        evt_ccw="MobiFlight.A32NX_FCU_ALT_DEC",
        mode=KNOB_MODE,
    )


def ap_alt_inc_toggle(m):
    """Toggle ALT increment mode"""

    # FIXME: this one is not working correctly
    if m.on:
        simc.send_event("MobiFlight.A32NX_FCU_ALT_INCREMENT_TOGGLE")


# FIXME
def ap_alt_push(m):
    """Push ALT knob"""
    if m.on:
        simc.send_event("MobiFlight.A32NX_FCU_ALT_PUSH")


# FIXME
def ap_alt_pull(m):
    """Pull SPEED knob"""
    if m.on:
        simc.send_event("MobiFlight.A32NX_FCU_ALT_PULL")


def ap_spd_pull(m):
    """Pull SPEED knob"""

    # FIXME
    if m.on:
        simc.send_event("MobiFlight.A320_Neo_FCU_SPEED_PULL")


def ap_spd_push(m):
    """Push SPEED knob"""

    # FIXME
    if m.on:
        simc.send_event("MobiFlight.A320_Neo_FCU_SPEED_PUSH")


def ap_spd_incdec(m):
    """SPD Mode knob (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.A320_Neo_FCU_SPEED_INC",
        evt_ccw="MobiFlight.A320_Neo_FCU_SPEED_DEC",
    )


def ap_vs_incdec(m):
    """VS Mode knob (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.A32NX_FCU_VS_INC",
        evt_ccw="MobiFlight.A32NX_FCU_VS_DEC",
    )


def ap_vs_push(m):
    """Push VS knob"""

    # FIXME
    if m.on:
        simc.send_event("MobiFlight.A320_Neo_FCU_VS_PUSH")


def ap_vs_pull(m):
    """Pull VS knob"""

    # FIXME
    if m.on:
        simc.send_event("MobiFlight.A320_Neo_FCU_VS_PULL")


def ap1_master_toggle(m):
    """Toggle autopilot"""

    if m.on:
        simc.send_event("MobiFlight.Autopilot_1_Push")


def ap_appr_toggle(m):
    """Toggle APPROACH mode"""

    if m.on:
        simc.send_event("AP_APR_HOLD")


def baro_std_push(m):
    """Barometer 1 push (set to STD)"""

    global ap_baro_switch
    if m.on:
        ap_baro_switch = not ap_baro_switch
        evt = (
            "MobiFlight.A32NX_BARO1_KNOB_PULL"
            if ap_baro_switch
            else "MobiFlight.A32NX_BARO1_KNOB_PUSH"
        )
        simc.send_event(evt)


def baro_incdec(m):
    """Barometer 1 knob (+/-)"""

    behringer.send_event_on_encoder_rotation(
        m.value,
        mode=KNOB_MODE,
        evt_cw="MobiFlight.AUTOPILOT_BARO_INC",
        evt_ccw="MobiFlight.AUTOPILOT_BARO_DEC",
    )


def config_reload(m):
    """Hot configuration reload"""

    config.reload()


# Proceed to start up the engines
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
config.setup(
    simconnect_backend=simc.SIMCONNECT_BACKEND_MOBIFLIGHT,
    midi_input_ports=MIDI_PORTS_IN,
    midi_cc_handlers=[
        # AP Panel handlers
        # ----------------------
        # BARO
        (BARO_INCDEC_KNOB, baro_incdec),  # PFD barometer
        # HDG
        (AP_HDG_INCDEC_KNOB, ap_hdg_incdec),  # HDG bug
        # ALT
        (AP_ALT_INCDEC_KNOB, ap_alt_incdec),
        # VS
        (AP_VS_INCDEC_KNOB, ap_vs_incdec),
        # SPD
        (AP_SPD_INCDEC_KNOB, ap_spd_incdec),
    ],
    midi_note_handlers=[
        # AP Panel handlers
        # ----------------------
        # AP master
        (AP1_MASTER_BT, ap1_master_toggle),
        # Barometers
        (BARO_STD_BT, baro_std_push),  # Barometer 1 STD switch
        # HDG
        (AP_HDG_PUSH_BT, ap_hdg_push),  # AP HDG push
        (AP_HDG_PULL_BT, ap_hdg_pull),  # AP HDG pull
        # NAV
        (AP_NAV_BT, ap_hdg_push),  # AP HDG pull
        # ALT
        (AP_ALT_INC_TOGGLE_BT, ap_alt_inc_toggle),
        (AP_ALT_PUSH_BT, ap_alt_push),
        (AP_ALT_PULL_BT, ap_alt_pull),
        # VS
        (AP_VS_PUSH_BT, ap_vs_push),
        (AP_VS_PULL_BT, ap_vs_pull),
        # SPD
        (AP_SPD_PUSH_BT, ap_spd_push),
        (AP_SPD_PULL_BT, ap_spd_pull),
        # APPROACH
        (AP_APPR_BT, ap_appr_toggle),
        # Reload config
        # ----------------------
        (CONFIG_RELOAD_BT, config_reload),
    ],
)
