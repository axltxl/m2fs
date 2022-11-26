
# -*- coding: utf-8 -*-

import SimConnect
import log
from .sim import connect

class SimEventException(Exception):
    pass

# FIXME: doc me
def send_event(name: str):
    # Creat a function to call the MobiFlight AS1000_MFD_SOFTKEYS_3 event.
    log.info(f'SimEvent => {name}')
    SimConnect.Event(name.encode('utf-8'), connect())()
