# -*- coding: utf-8 -*-

import mido

from .log import log
from .exceptions import MIDIException


# FIXME
# __in_port = None
__in_ports = {}
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


def list_available_ports() -> dict:
    """List all available MIDI ports"""

    return {
        "input": mido.get_input_names(),
        "output": mido.get_output_names(),
    }


def connect_input_port(*, name) -> None:
    """Connect and/or setup MIDI input port"""

    global __in_ports

    if not name in __in_ports:
        inp = mido.open_input(name)
        if inp is None:
            raise MIDIException(f"{name}: invalid MIDI input port")
        inp.reset()
        __in_ports[name] = inp
        log.info(f"input port connected: {name}")


def get_input_port(*, name) -> (mido.ports.BaseInput | None):
    """Get currently connected input port"""

    try:
        return __in_ports[name]
    except KeyError:
        return None


# FIXME
def get_all_input_ports() -> list[mido.ports.BaseInput]:
    return [v for _, v in __in_ports.items()]


# FIXME
# def get_input_port_name() -> str:
#     """Get currently connected MIDI input port name"""

#     global __in_port

#     if __in_port is not None:
#         return __in_port.name
#     return "NO_MIDI_IN_CONNECTED"


# FIXME
def connect_output_port(*, name) -> None:
    global __out_ports

    log.debug(f"opening output port: {name} ...")

    if name not in __out_ports:
        out = mido.open_output(name=name, autoreset=True)
        if out is None:
            raise MIDIException(f"{name}: invalid MIDI output port")
        out.reset()
        __out_ports[name] = out


def get_output_port(*, name) -> (mido.ports.BaseOutput | None):
    """Get MIDI output port by name"""

    try:
        return __out_ports[name]
    except KeyError:
        return None


def cleanup() -> None:
    """Close all MIDI ports and do housekeeping"""

    # Close currently opened MIDI input port
    for name, port in __in_ports.items():
        log.info(f"closing input port: {name}")
        __close_port(port)

    # Close all opened MIDI output ports
    for name, port in __out_ports.items():
        log.info(f"closing output port: {name}")
        __close_port(port)


def __close_port(port: mido.ports.BasePort) -> None:
    """Close a MIDI port"""

    if port is not None and not port.closed:
        port.close()
