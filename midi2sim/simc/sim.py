# -*- coding: utf-8 -*-

import time

import SimConnect

from .log import log

# This client will try for up to 5 minutes
# before giving up in connect to the flight sim
CONNECTION_TIME_MAX = 300

# SimConnect client
_sm_client = None


def connect() -> SimConnect.SimConnect:
    """Connect to flight sim via SimConnect library"""

    global _sm_client
    if _sm_client is None:
        log.info("Connecting to simulator using SimConnect ...")

        for i in range(0, CONNECTION_TIME_MAX):
            try:
                _sm_client = SimConnect.SimConnect()
                break
            except ConnectionError:
                if i == CONNECTION_TIME_MAX - 1:
                    raise
                time.sleep(1)
        log.info("Connected to simulator!")

    return _sm_client


def disconnect() -> None:
    """Disconnect from flight sim"""

    global _sm_client
    if _sm_client is not None:
        _sm_client.exit()
        log.info("Disconnected from simulator ...")
