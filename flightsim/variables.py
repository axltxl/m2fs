# -*- coding: utf-8 -*-

import SimConnect
import log
from .sim import connect

class SimVarException(Exception):
    """SimVar error"""
    pass

class SimVar:
    """SimVar with class ;)"""

    def __init__(self, *, name: str, description: str, value: any):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self) -> str:
        return f'SimVar(name={self.name}, description={self.description}, value={self.value}'


def get_variable(name: str) -> (SimVar|None):
    """Get SimVar from flight sim"""

    v = SimConnect.AircraftRequests(connect(), _time=500).find(name)
    if v is not None:
        value = v.get()
        log.info(f'SimVar GET {name} => {value}')
        return SimVar(name=name, description=v.description, value=value)

    # NOTE: Unfortunately, not all SimVars are supported out of the box
    # Only the ones supported by PySimConnect, which are a lot indeed and
    # will do much for you, but still, do not expect to get just any SimVar
    raise SimVarException(f'SimVar GET {name}: couldn\'t find it. SimVar does not exist or likely not supported by PySimConnect library! :(')


def set_variable(name: str, value: any):
    """Set SimVar on flight sim :)"""

    log.info(f'SimVar SET {name} => {value}')
    v = SimConnect.AircraftRequests(connect()).find(name)
    if v is not None:
        v.set(value)
    else:
        # NOTE: Unfortunately, not all SimVars are supported out of the box
        # Only the ones supported by PySimConnect, which are a lot indeed and
        # will do much for you, but still, do not expect to get just any SimVar
        raise SimVarException(f'SimVar SET {name}: couldn\'t find it. SimVar does not exist or likely not supported by PySimConnect library! :(')

