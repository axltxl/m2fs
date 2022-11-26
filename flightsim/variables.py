# -*- coding: utf-8 -*-

import SimConnect
import log
from .sim import connect

class SimVarException(Exception):
    pass

class SimVar:
    def __init__(self, *, name: str, description: str, value: any):
        self.name = name
        self.description = description
        self.value = value

    def __str__(self) -> str:
        return f'SimVar(name={self.name}, description={self.description}, value={self.value}'


# FIXME: doc me
def get_variable(name: str) -> (SimVar|None):
    v = SimConnect.AircraftRequests(connect(), _time=500).find(name)
    if v is not None:
        value = v.get()
        log.info(f'SimVar GET {name} => {value}')
        return SimVar(name=name, description=v.description, value=value)
    log.warn(f'SimVar GET {name}: undefined')
    return None


# FIXME: doc me and implement me
def set_variable(name: str, value: any):
    log.info(f'SimVar SET {name} => {value}')
    v = SimConnect.AircraftRequests(connect()).find(name)
    if v is not None:
        v.set(value)
    else:
        raise SimVarException(f'SimVar SET {name}: couldn\'t find it. SimVar does not exist or likely not supported by PySimConnect library! :(')

