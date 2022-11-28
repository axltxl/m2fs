# -*- coding: utf-8 -*-

import mido

from .log import log
from .exceptions import MIDIException


__in_port = None
__out_ports = {}


def send_note_message(*, dest_port, note, channel=0, on=True, velocity=64, time=0):
    """Send note message to an output MIDI port"""

    note_press = "note_on" if on else "note_off"
    get_output_port(name=dest_port).send(
        mido.Message(
            note_press, channel=channel, note=note, velocity=velocity, time=time
        )
    )
    log.debug(
        f'send_note_message(dest_port="{dest_port}", note={note}, channel={channel}, on={on}, velocity={velocity}, time={time})'
    )


def send_cc_message(*, dest_port, value, channel=0):
    """Send CC message to an output MIDI port"""

    get_output_port(name=dest_port).send(
        mido.Message("control_change", channel=channel, value=value)
    )
    log.debug(
        f'send_note_message(dest_port="{dest_port}", channel={channel}, value={value})'
    )


def list_ports() -> dict:
    """List all physical MIDI ports (devices)"""

    return {
        "input": mido.get_input_names(),
        "output": mido.get_output_names(),
        "io": mido.get_ioport_names(),
    }


def connect_input_port(*, name) -> None:
    """Connect and/or setup MIDI input port"""

    global __in_port

    __in_port = mido.open_input(name)
    log.info(f"input port connected: {__in_port.name}")


def get_input_port() -> (mido.ports.BaseInput | None):
    """Get currently connected input port"""

    return __in_port


def get_input_port_name() -> str:
    """Get currently connected MIDI input port name"""

    global __in_port

    if __in_port is not None:
        return __in_port.name
    return "NO_MIDI_IN_CONNECTED"


def get_output_port(*, name) -> mido.ports.BaseOutput:
    """Get MIDI output port by name"""

    global __out_ports

    log.debug(f"opening output port: {name} ...")

    if name not in __out_ports:
        out = mido.open_output(name=name, autoreset=True)
        if out is None:
            raise MIDIException(f"{name}: invalid MIDI output port")
        out.reset()
        __out_ports[name] = out

    return __out_ports[name]


def cleanup() -> None:
    """Close all MIDI ports and do housekeeping"""

    # Close currently opened MIDI input port
    __close_port(__in_port)

    # Close all opened MIDI output ports
    for name, port in __out_ports.items():
        log.info("closing port: {name}")
        __close_port(port)


def __close_port(port: mido.ports.BasePort) -> None:
    """Close a MIDI port"""

    if port is not None and not port.closed:
        port.close()
