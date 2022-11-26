# -*- coding: utf-8 -*-

import SimConnect
from .sim import connect

# FIXME: doc me
def get_variable(name: str) -> any:
    sm = connect()
    ar = SimConnect.AircraftEvents(sm)
    # FIXME: doc me
    # while True:
    #     # ar.list()
    #     pass


# FIXME: doc me and implement me
def set_variable(name: str, value: any):
    pass
