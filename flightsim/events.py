
# -*- coding: utf-8 -*-

import SimConnect
import log
from .sim import connect

class SimEventException(Exception):
    """SimConnect Event exception"""
    pass


def send_event(name: str, value=0):
    """Send event to flight sim"""

    log.info(f'SimEvent: {name} => {value}')
    SimConnect.Event(name.encode('utf-8'), connect())(value)
