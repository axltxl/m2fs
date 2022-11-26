# -*- coding: utf-8 -*-

import time
import SimConnect

import log

# FIXME: doc me
CONNECTION_ATTEMPTS_MAX = 300

# FIXME: doc me
_sm_client = None

# FIXME: doc me
def connect() -> SimConnect.SimConnect:

    global _sm_client
    if _sm_client is None:
        log.info("Connecting to simulator using SimConnect ...")

        for i in range(0, CONNECTION_ATTEMPTS_MAX):
            try:
                _sm_client = SimConnect.SimConnect()
                break
            except ConnectionError:
                if i == CONNECTION_ATTEMPTS_MAX - 1:
                    raise
                time.sleep(1)
        log.info("Connected to simulator!")

    return _sm_client

# FIXME: doc me
def disconnect() -> None:
    global _sm_client
    if _sm_client is not None:
        _sm_client.exit()
        log.info("Disconnected from simulator ...")
