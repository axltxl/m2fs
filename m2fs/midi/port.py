# -*- coding: utf-8 -*-

import threading
import mido

from .log import log
from .exceptions import MIDIException


__in_ports = {}
__out_ports = {}

# Mutexes for parallel access
__in_ports_mutex = threading.Lock()
__out_ports_mutex = threading.Lock()


def send_note_message(*, dest_port, note, channel=0, on=True, velocity=64, time=0):
    """Send note message to an output MIDI port"""

    global __out_ports, __out_ports_mutex

    note_press = "note_on" if on else "note_off"

    with __out_ports_mutex:
        if dest_port not in __out_ports:
            connect_output_port(name=dest_port)

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

    global __out_ports, __out_ports_mutex

    with __out_ports_mutex:
        if dest_port not in __out_ports:
            connect_output_port(name=dest_port)

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

    global __in_ports, __in_ports_mutex

    with __in_ports_mutex:
        if not name in __in_ports:
            inp = mido.open_input(name)
            if inp is None:
                raise MIDIException(f"{name}: invalid MIDI input port")
            __in_ports[name] = inp
            log.info(f"input port connected: {name}")


def get_input_port(*, name) -> mido.ports.BaseInput:
    """Get currently connected input port"""

    global __in_ports, __in_ports_mutex
    with __in_ports_mutex:
        try:
            return __in_ports[name]
        except KeyError:
            return None


def get_all_input_ports() -> list[mido.ports.BaseInput]:
    """Get all currently connected input ports"""

    global __in_ports, __in_ports_mutex
    with __in_ports_mutex:
        return [v for _, v in __in_ports.items()]


def connect_output_port(*, name) -> None:
    """Connect an output port"""

    global __out_ports, __out_ports_mutex

    log.debug(f"opening output port: {name} ...")

    with __out_ports_mutex:
        if name not in __out_ports:
            out = mido.open_output(name=name, autoreset=True)
            if out is None:
                raise MIDIException(f"{name}: invalid MIDI output port")
            out.reset()
            __out_ports[name] = out


def get_output_port(*, name) -> mido.ports.BaseOutput:
    """Get MIDI output port by name"""

    global __out_ports, __out_ports_mutex
    with __out_ports_mutex:
        try:
            return __out_ports[name]
        except KeyError:
            return None


def cleanup() -> None:
    """Close all MIDI ports and do housekeeping"""

    global __out_ports, __out_ports_mutex
    global __in_ports, __in_ports_mutex

    # Close currently opened MIDI input port
    with __in_ports_mutex:
        for name, port in __in_ports.items():
            log.info(f"closing input port: {name}")
            __close_port(port)
        __in_ports = {}  # vanish all traces of MIDI ports

    # Close all opened MIDI output ports
    with __out_ports_mutex:
        for name, port in __out_ports.items():
            log.info(f"closing output port: {name}")
            __close_port(port)
        __out_ports = {}  # vanish all traces of MIDI ports


def __close_port(port: mido.ports.BasePort) -> None:
    """Close a MIDI port"""

    if port is not None and not port.closed:
        port.close()
