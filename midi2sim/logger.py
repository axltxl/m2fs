# -*- coding: utf-8 -*-

LOG_LVL_VERBOSE = -1
LOG_LVL_DEBUG = 0
LOG_LVL_INFO = 1
LOG_LVL_WARN = 2
LOG_LVL_FATAL = 3
# LOG_LVL = LOG_LVL_VERBOSE  # FIXME: hardcoded (for now)
LOG_LVL = LOG_LVL_DEBUG  # FIXME: hardcoded (for now)

LEVEL_STR = {
    LOG_LVL_VERBOSE: "VERBOSE",
    LOG_LVL_DEBUG: "DEBUG",
    LOG_LVL_INFO: "INFO",
    LOG_LVL_WARN: "WARN",
    LOG_LVL_FATAL: "FATAL",
}


class Logger:
    """Logger class utility"""

    def __init__(self, *, prefix):
        self.__prefix = prefix

    def __fmt_msg(self, msg):
        return f"{self.__prefix} {msg}"

    def verbose(self, msg):
        log.verbose(self.__fmt_msg(msg))

    def debug(self, msg):
        log.debug(self.__fmt_msg(msg))

    def info(self, msg):
        log.info(self.__fmt_msg(msg))

    def warn(self, msg):
        log.warn(self.__fmt_msg(msg))

    def error(self, msg):
        log.error(self.__fmt_msg(msg))


def log(level: int, msg: str) -> None:
    if level >= LOG_LVL:
        print(f"[{LEVEL_STR[level]}] - {msg}")


def verbose(msg: str):
    log(LOG_LVL_VERBOSE, msg)


def debug(msg: str):
    log(LOG_LVL_DEBUG, msg)


def info(msg: str) -> None:
    log(LOG_LVL_INFO, msg)


def warn(msg: str) -> None:
    log(LOG_LVL_WARN, msg)


def error(msg: str) -> None:
    log(LOG_LVL_FATAL, msg)


class Logger:
    """Logger class utility"""

    def __init__(self, *, prefix):
        self.__prefix = prefix

    def __fmt_msg(self, msg):
        return f"{self.__prefix} {msg}"

    def verbose(self, msg):
        verbose(self.__fmt_msg(msg))

    def debug(self, msg):
        debug(self.__fmt_msg(msg))

    def info(self, msg):
        info(self.__fmt_msg(msg))

    def warn(self, msg):
        warn(self.__fmt_msg(msg))

    def error(self, msg):
        error(self.__fmt_msg(msg))
