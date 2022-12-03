# -*- coding: utf-8 -*-

import SimConnect
from . import mobiflight
from .log import log
from .client import get_client


class SimEventException(Exception):
    """SimConnect Event exception"""

    pass


def send_event(name: str, value=0):
    """Send event to flight sim"""

    log.info(f"SimEvent: {name}({value})")
    # mobiflight.SimConnectMobiFlight.Event(name.encode("utf-8"), connect())(value)
    SimConnect.Event(name.encode("utf-8"), get_client())(value)
