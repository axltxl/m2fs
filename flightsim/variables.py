# -*- coding: utf-8 -*-

import SimConnect
import log
from .sim import connect

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
        return SimVar(name=name, description=v.description, value=v.get())
    log.warn('SimVar GET {name}: undefined')
    return None


# FIXME: doc me and implement me
def set_variable(name: str, value: any):
    v = SimConnect.AircraftRequests(connect(), _time=500).find(name)
    if v is not None:
        v.set(value)
    else:
        log.warn('SimVar SET {name}: SimVar undefined')

