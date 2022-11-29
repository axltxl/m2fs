# -*- coding: utf-8 -*-

import time

import SimConnect

from . import mobiflight, variables, backend
from .log import log
from .const import SIMCONNECT_TIMEOUT_SECONDS


# SimConnect client
__smc_client = None


# FIXME: should I remain like this?
def get_client() -> SimConnect.SimConnect:
    global __smc_client
    connect()
    return __smc_client


def connect(*, timeout: int = SIMCONNECT_TIMEOUT_SECONDS) -> None:
    """Connect to flight sim via SimConnect library"""

    global __smc_client
    if __smc_client is None:
        log.info(
            f"Connecting to simulator using SimConnect: backend: { backend.get_backend_name()} ..."
        )

        for i in range(0, timeout):
            try:
                if backend.get_backend() == backend.SIMCONNECT_BACKEND_MOBIFLIGHT:
                    __smc_client = mobiflight.SimConnectMobiFlight()
                else:
                    __smc_client = SimConnect.SimConnect()
                break
            except ConnectionError:
                if i == timeout - 1:
                    raise
                time.sleep(1)

        # Set current client on the variables module
        # (this is to avoid a circular dependency problem)
        variables.update_client(__smc_client)
        log.info("Connected to simulator!")


def __cleanup():
    """Do housekeeping (at shutdown normally)"""

    global __smc_client
    __smc_client = None

    # Make sure any variables-related things have been taken care of
    variables.cleanup()


def disconnect() -> None:
    """Disconnect from flight sim"""

    global __smc_client
    if __smc_client is not None:
        __smc_client.exit()
        log.info("Disconnected from simulator ...")
    __cleanup()  # do housekeeping afterwards
