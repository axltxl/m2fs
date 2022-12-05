# -*- coding: utf-8 -*-

import threading
import time

import SimConnect

from .variables import (
    update_client as variables_update_client,
    cleanup as variables_cleanup,
)
from .log import log
from .const import SIMCONNECT_TIMEOUT_SECONDS
from .backend import (
    set_backend,
    get_backend,
    get_backend_name,
    SIMCONNECT_BACKEND_DEFAULT,
    SIMCONNECT_BACKEND_MOBIFLIGHT,
)
from .mobiflight import SimConnectMobiFlight
from .poll import poll_reset

# SimConnect client mutex for parallel access
__smc_client_mutex = threading.Lock()

# SimConnect client
__smc_client = None


def reset():
    """Reset SimConnect client and data to defaults"""

    # reset SimVar poll
    poll_reset()

    # disconnect from Simulator
    disconnect()


def get_client() -> SimConnect.SimConnect:
    global __smc_client
    with __smc_client_mutex:
        return __smc_client


def connect(
    *,
    timeout: int = SIMCONNECT_TIMEOUT_SECONDS,
    backend: int = SIMCONNECT_BACKEND_DEFAULT,
) -> None:
    """Connect to flight sim via SimConnect library"""

    global __smc_client

    with __smc_client_mutex:
        # Set backend type
        set_backend(backend)

        # What if already connected?
        # get_client() would be the appropriate method
        # for getting current connected client
        # if connect() is called in this situation, it'll
        # attempt a new connection
        if __smc_client is not None:
            disconnect()

        log.info(
            f"Connecting to simulator using SimConnect: backend: { get_backend_name()} ..."
        )

        for i in range(0, timeout):
            try:
                if get_backend() == SIMCONNECT_BACKEND_MOBIFLIGHT:
                    __smc_client = SimConnectMobiFlight()
                else:
                    __smc_client = SimConnect.SimConnect()
                break
            except ConnectionError:
                if i == timeout - 1:
                    raise
                time.sleep(1)

        # Set current client on the variables module
        # (this is to avoid a circular dependency problem)
        variables_update_client(__smc_client)
        log.info("Connected to simulator!")


def __cleanup():
    """Do housekeeping (at shutdown normally)"""

    # called indirectly by disconnect only
    # doesn't need mutex
    global __smc_client
    __smc_client = None

    # Make sure any variables-related things have been taken care of
    variables_cleanup()


def disconnect() -> None:
    """Disconnect from flight sim"""

    global __smc_client
    with __smc_client_mutex:
        if __smc_client is not None:
            __smc_client.exit()
            log.info("Disconnected from simulator ...")
    __cleanup()  # do housekeeping afterwards
