# -*- coding: utf-8 -*-

import random
import threading
import time

from .log import log
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


# Poll thread subscriptions mutex for parallel access
__poll_simvar_subs_mutex = threading.Lock()

__poll_simvar_subs = []  # poll subscribers
__poll_quit = False

# Poll thread implementation
__poll_thread = None


def __get_thread_name() -> str:
    id = random.randint(0, 1000)
    return f"simc:poll:{id:05}"


def __poll():
    """
    The poll itself

    This will go across all subscribers
    and invoke their handlers should their
    associated SimVars have changed since
    last survey
    """

    global __poll_quit, __poll_simvar_subs, __poll_simvar_subs_mutex

    while not __poll_quit:
        with __poll_simvar_subs_mutex:
            for sub in __poll_simvar_subs:
                __poll_notify_on_change(sub)
        time.sleep(POLL_TICK_PERIOD)  # do not be so aggresive


def subscribe_to_simvar(name: str, *, handler: callable) -> None:
    """
    Subscribe a handler function to SimVar changes

    Upon a SimVar change, handler will be called
    """

    with __poll_simvar_subs_mutex:
        log.info(f"SimVar: sub: {name} => {handler.__name__}")
        __poll_simvar_subs.append(SubSimVar(simvar=get_variable(name), handler=handler))


def __poll_notify_on_change(sub: SubSimVar) -> None:
    """Check for change on a SimVar and notify its subscriber upon change"""

    simvar = get_variable(sub.simvar.name)

    if simvar.value != sub.simvar.value:
        log.debug(f"SimVar: {simvar.name} ({sub.simvar.value} => {simvar.value})")
        sub.simvar = simvar
        sub.handler(simvar)


def poll_reset() -> None:
    """Reset poll thread"""

    global __poll_simvar_subs, __poll_simvar_subs_mutex

    # get rid of any subs
    with __poll_simvar_subs_mutex:
        __poll_simvar_subs = []

    # restart poll thread
    poll_stop()
    poll_start()


def poll_start() -> None:
    """Start poll thread"""

    global __poll_thread, __poll_quit

    # Reset quit flag
    __poll_quit = False

    # Regardless of how this function is called, we have to make sure
    # we're not attempting to recreate the thread
    if __poll_thread is None:
        log.debug("poll: SimConnect: start polling for SimVar changes ...")
        __poll_thread = threading.Thread(target=__poll, name=__get_thread_name())
        __poll_thread.start()
    else:
        log.debug(f"poll: thread already started ({__poll_thread.getName()})")


def poll_stop() -> None:
    """Stop poll thread"""

    global __poll_thread
    global __poll_quit

    log.debug("SimConnect: stop polling for SimVar changes ...")

    # kill the poll thread
    if __poll_thread is not None:
        if __poll_thread.is_alive():
            __poll_quit = True
            __poll_thread.join()

        __poll_thread = None
