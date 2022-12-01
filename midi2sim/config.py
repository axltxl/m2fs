# -*- coding: utf-8 -*-
# FIXME: doc me

from .midi import (
    subscribe_to_cc as midi_subscribe_to_cc,
    subscribe_to_note as midi_subscribe_to_note,
    subscribe_to_pitchwheel as midi_subscribe_to_pitchwheel,
    connect_input_port as midi_connect_input_port,
)
from .simc import connect as simc_connect
from .simc import SIMCONNECT_BACKEND_DEFAULT

# FIXME: doc me
def ___batch_assign_cc_handlers(h_map: list[tuple[int, callable]]):
    for handle_pair in h_map:
        cc, handler = handle_pair
        midi_subscribe_to_cc(cc=cc, handler=handler)


def ___batch_assign_note_handlers(h_map: list[tuple[int, callable]]):
    for handle_pair in h_map:
        note, handler = handle_pair
        midi_subscribe_to_note(note=note, handler=handler)


# FIXME
def setup(
    *,
    simconnect_backend: int = SIMCONNECT_BACKEND_DEFAULT,
    midi_input_port: str,
    midi_cc_handlers: list[tuple[int, callable]] = None,
    midi_note_handlers: list[tuple[int, callable]] = None,
    pitchwheel_handler: callable = None,
):
    #
    midi_connect_input_port(name=midi_input_port)

    #
    simc_connect(backend=simconnect_backend)

    #
    if midi_cc_handlers is not None:
        ___batch_assign_cc_handlers(midi_cc_handlers)

    if midi_note_handlers is not None:
        ___batch_assign_note_handlers(midi_note_handlers)

    if pitchwheel_handler is not None:
        midi_subscribe_to_pitchwheel(handler=pitchwheel_handler)
