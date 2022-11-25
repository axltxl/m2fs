#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from log import log
import midi

CMD_LS = "ls"


def __log_ports(ports: list[str]) -> None:
    if len(ports):
        for port in ports:
            log(log.LOG_LVL_INFO, f'\t+ {port}')
    else:
        log(log.LOG_LVL_WARN, "No device found :(")


def __cmd_ls() -> None:
    ports = midi.ls_ports()
    log(log.LOG_LVL_INFO, "List of MIDI input ports found:")
    __log_ports(ports['input'])
    log(log.LOG_LVL_INFO, "List of MIDI output ports found:")
    __log_ports(ports['output'])
    log(log.LOG_LVL_INFO, "List of MIDI I/O ports found:")
    __log_ports(ports['io'])


def __parse_args(argv: list[str]) -> dict:
    """Parse arguments"""

    options = {
        "command": None
    }

    try:
        options["command"] = argv[0]
    except IndexError:
        pass
    return options


def do_something(msg):
    print("HOLAAA")


def main(options: dict):
    """Main entrypoint"""

    try:
        command = options['command']
        if command is not None:
            if command == CMD_LS:
                __cmd_ls()
        else:
            return midi.message_pump(do_something)

    except Exception as e:
        log(LOG_LVL_FATAL, f'Error: {e}')
        return -1


if __name__ == "__main__":
    sys.exit(main(__parse_args(sys.argv[1:])))
