# -*- coding: utf-8 -*-

import time

import SimConnect

# FIXME: doc me
from . import mobiflight

from .log import log

# This client will try for up to 5 minutes
# before giving up in connect to the flight sim
CONNECTION_TIME_MAX = 300

# SimConnect client
__smc_client = None

# SimConnect client backends
SIMCONNECT_BACKEND_DEFAULT = 0
SIMCONNECT_BACKEND_MOBIFLIGHT = 1
SIMCONNECT_BACKEND_DEFAULT_NAME = "Python-SimConnect"
SIMCONNECT_BACKEND_MOBIFLIGHT_NAME = "MobiFlight"
__smc_backend = SIMCONNECT_BACKEND_DEFAULT


# FIXME: doc me
def get_backend() -> int:
    return __sm_backend


# FIXME: doc me
def set_backend(backend: int) -> None:
    global __sm_backend
    __sm_backend = backend


def __get_backend_name() -> str:
    global __sm_backend
    if __sm_backend == SIMCONNECT_BACKEND_MOBIFLIGHT:
        return SIMCONNECT_BACKEND_MOBIFLIGHT_NAME
    return SIMCONNECT_BACKEND_DEFAULT_NAME


# FIXME: doc me
def get_client() -> SimConnect.SimConnect:
    global __smc_client
    connect()
    return __smc_client


def connect() -> None:
    """Connect to flight sim via SimConnect library"""

    global __smc_client
    if __smc_client is None:
        log.info(
            f"Connecting to simulator using SimConnect: backend: { __get_backend_name()} ..."
        )

        for i in range(0, CONNECTION_TIME_MAX):
            try:
                if __sm_backend == SIMCONNECT_BACKEND_MOBIFLIGHT:
                    __smc_client = mobiflight.SimConnectMobiFlight()
                else:
                    __smc_client = SimConnect.SimConnect()
                break
            except ConnectionError:
                if i == CONNECTION_TIME_MAX - 1:
                    raise
                time.sleep(1)
        log.info("Connected to simulator!")


def disconnect() -> None:
    """Disconnect from flight sim"""

    global __sm_client
    if __sm_client is not None:
        __sm_client.exit()
        log.info("Disconnected from simulator ...")
