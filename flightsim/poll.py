# -*- coding: utf-8 -*-

import threading
import time

import log
from .variables import get_variable, SimVar, SIMCONNECT_CACHE_TTL_MS

# Poll thread tick period is ms
# (or many times a second is it gonna run a survey)
# (it cannot be shorter than the SimVar cached data from Python-SimConnect)
POLL_TICK_PERIOD = SIMCONNECT_CACHE_TTL_MS / 1000.0


class SubSimVar:
    """Subscription to SimVar change"""

    def __init__(self, *, simvar: SimVar, handler: callable):
        self.simvar = simvar
        self.handler = handler


__poll_simvar_subs = []  # poll subscribers
__poll_quit = False


def __poll():
    """
    The poll itself

    This will go across all subscribers
    and invoke their handlers should their
    associated SimVars have changed since
    last survey
    """

    global __poll_quit
    while not __poll_quit:
        log.verbose("SimVar: Polling for changes ...")
        for sub in __poll_simvar_subs:
            __poll_notify_on_change(sub)
        time.sleep(POLL_TICK_PERIOD)  # do not be so aggresive


# Poll thread implementation
__poll_thread = threading.Thread(target=__poll)


def subscribe_to_simvar(name: str, *, handler: callable) -> None:
    """
    Subscribe a handler function to SimVar changes

    Upon a SimVar change, handler will be called
    """

    log.info(f"SimVar: sub: {name} => {handler.__name__}")
    __poll_simvar_subs.append(SubSimVar(simvar=get_variable(name), handler=handler))


def __poll_notify_on_change(sub: SubSimVar) -> None:
    """Check for change on a SimVar and notify its subscriber upon change"""

    simvar = get_variable(sub.simvar.name)

    if simvar.value != sub.simvar.value:
        log.debug(f"SimVar: {simvar.name} ({sub.simvar.value} => {simvar.value})")
        sub.simvar = simvar
        sub.handler(simvar)


def poll_start() -> None:
    """Start poll thread"""

    global __poll_thread

    log.debug("SimConnect: start polling for SimVar changes ...")
    __poll_thread.start()


def poll_stop() -> None:
    """Stop poll thread"""

    global __poll_thread
    global __poll_quit

    log.debug("SimConnect: stop polling for SimVar changes ...")

    __poll_quit = True
    __poll_thread.join()
