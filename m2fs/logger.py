# -*- coding: utf-8 -*-
from colorama import just_fix_windows_console
from colorama import Fore, Back, Style

just_fix_windows_console()

LOG_LVL_VERBOSE = -1
LOG_LVL_DEBUG = 0
LOG_LVL_INFO = 1
LOG_LVL_WARN = 2
LOG_LVL_FATAL = 3

LOG_COLOR_FG_RED = 0
LOG_COLOR_FG_GREEN = 1
LOG_COLOR_FG_YELLOW = 2
LOG_COLOR_FG_MAGENTA = 3
LOG_COLOR_FG_BLUE = 4

LOG_COLOR_BG_RED = 5
LOG_COLOR_BG_GREEN = 6
LOG_COLOR_BG_YELLOW = 7
LOG_COLOR_BG_MAGENTA = 8
LOG_COLOR_BG_BLUE = 9

__color_map = {
    LOG_COLOR_FG_RED: Fore.RED,
    LOG_COLOR_FG_GREEN: Fore.GREEN,
    LOG_COLOR_FG_YELLOW: Fore.YELLOW,
    LOG_COLOR_FG_MAGENTA: Fore.MAGENTA,
    LOG_COLOR_FG_BLUE: Fore.BLUE,
    LOG_COLOR_BG_RED: Back.RED,
    LOG_COLOR_BG_GREEN: Back.GREEN,
    LOG_COLOR_BG_YELLOW: Back.YELLOW,
    LOG_COLOR_BG_MAGENTA: Back.MAGENTA,
    LOG_COLOR_BG_BLUE: Back.BLUE,
}

__log_level = LOG_LVL_INFO

LEVEL_STR = {
    LOG_LVL_VERBOSE: "VERBOSE",
    LOG_LVL_DEBUG: "DEBUG",
    LOG_LVL_INFO: "INFO",
    LOG_LVL_WARN: "WARN",
    LOG_LVL_FATAL: "FATAL",
}


def set_log_level(lvl: int) -> None:
    global __log_level
    __log_level = lvl


def __paint(msg, *, fg_color, bg_color):
    try:
        msg = __color_map[fg_color] + msg
    except (KeyError, TypeError):
        pass

    try:
        msg = __color_map[bg_color] + msg
    except (KeyError, TypeError):
        pass

    return msg + Style.RESET_ALL


def print_to_stdout(msg, *, fg_color=None, bg_color=None):
    """Print straight to stdout (with color)"""

    print(__paint(msg, fg_color=fg_color, bg_color=bg_color))


def log(level: int, msg: str, fg_color=None, bg_color=None) -> None:
    msg = __paint(
        f"[{LEVEL_STR[level]}] - {msg}", fg_color=fg_color, bg_color=bg_color
    )  # format message
    if level >= __log_level:
        print(msg)


def verbose(msg: str):
    log(LOG_LVL_VERBOSE, msg, fg_color=LOG_COLOR_FG_MAGENTA)


def debug(msg: str):
    log(LOG_LVL_DEBUG, msg, fg_color=LOG_COLOR_FG_BLUE)


def info(msg: str) -> None:
    log(LOG_LVL_INFO, msg, fg_color=LOG_COLOR_FG_GREEN)


def warn(msg: str) -> None:
    log(LOG_LVL_WARN, msg, fg_color=LOG_COLOR_FG_YELLOW)


def error(msg: str) -> None:
    log(LOG_LVL_FATAL, msg, fg_color=LOG_COLOR_FG_RED)


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

    def set_level(lvl: int):
        set_log_level(lvl)
