# -*- coding: utf-8 -*-

import time
import SimConnect

import log

CONNECTION_ATTEMPTS_MAX = 300

# FIXME: doc me
def connect() -> SimConnect.SimConnect:

    log.info("Connecting to simulator using SimConnect ...")

    for i in range(0, CONNECTION_ATTEMPTS_MAX):
        try:
            sm = SimConnect.SimConnect()
            break
        except ConnectionError:
            if i == CONNECTION_ATTEMPTS_MAX - 1:
                raise
            time.sleep(1)

    log.info("Connected to simulator!")
    return sm
