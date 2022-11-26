# -*- coding: utf-8 -*-

import SimConnect
from .sim import connect

# FIXME: doc me
def watch(*, events=True, variables=False):
    sm = connect()
    ar = SimConnect.AircraftEvents(sm)
    # FIXME: doc me
    while True:
        # ar.list()
        pass


