# -*- coding: utf-8 -*-

import mido

import log
from .exceptions import MIDIException

# FIXME: doc me
__in_port = None
__out_ports = {}

# FIXME: doc me
# CONTINUEHERE: implement send_cc_change and wrap this up :)
def send_note_change(*, port_name, note, channel=0, on=True, velocity=64, time=0):
    note_press = "note_on" if on else "note_off"
    get_output_port(name=port_name).send(
        mido.Message(
            note_press, channel=channel, note=note, velocity=velocity, time=time
        )
    )
    log.debug(
        f'MIDI: send_note_change(port_name="{port_name}", note={note}, channel={channel}, on={on}, velocity={velocity}, time={time})'
    )


def list_ports() -> dict:
    """List all physical MIDI ports (devices)"""

    return {
        "input": mido.get_input_names(),
        "output": mido.get_output_names(),
        "io": mido.get_ioport_names(),
    }


# FIXME: doc me
def connect_input_port(*, name) -> None:
    global __in_port
    __in_port = mido.open_input(name)
    log.info(f"MIDI input connected: {__in_port.name}")


# FIXME: doc me
def get_input_port() -> (mido.ports.BaseInput | None):
    return __in_port


# FIXME: doc me
def get_input_port_name() -> str:
    global __in_port
    if __in_port is not None:
        return __in_port.name
    return "NO_MIDI_IN_CONNECTED"


# FIXME: doc me
def get_output_port(*, name) -> mido.ports.BaseOutput:

    global __out_ports
    if name not in __out_ports:
        log.debug(f"MIDI: opening output port: {name} ...")
        out = mido.open_output(name=name, autoreset=True)
        if out is None:
            raise MIDIException(f"{name}: invalid MIDI output port")
        out.reset()
        __out_ports[name] = out
    return __out_ports[name]


# FIXME: doc me
def cleanup() -> None:
    __close_port(__in_port)
    for name, port in __out_ports.items():
        __close_port(port)


# FIXME: doc me
def __close_port(port: mido.ports.BasePort) -> None:
    if port is not None and not port.closed:
        port.close()
