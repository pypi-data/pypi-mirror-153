#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/cli/logging.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-07-09 16:31:58 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Logging support."""

from typing import TYPE_CHECKING

from vutils.cli.io import blue, brown, red, yellow

if TYPE_CHECKING:
    import pathlib

    from vutils.cli import _ColorFuncType, _LoggerProtocol


class LogFormatter:
    """Define how to format log messages."""

    INFO: str = "info"
    WARNING: str = "warning"
    ERROR: str = "error"
    DEBUG: str = "debug"
    FORMAT: str = "{label}: {message}"
    __slots__ = ("__colormap",)

    def __init__(self) -> None:
        """Initialize the formatter."""
        self.__colormap: "dict[str, _ColorFuncType]" = {}
        cls = type(self)
        self.set_style(cls.INFO, blue)
        self.set_style(cls.WARNING, yellow)
        self.set_style(cls.ERROR, red)
        self.set_style(cls.DEBUG, brown)

    def set_style(self, name: str, color: "_ColorFuncType") -> None:
        """
        Set the style for a given type of log messages.

        :param name: The name of the message type
        :param color: The message color

        The supported types of log messages are:
        - `~LogFormatter.INFO` for info messages
        - `~LogFormatter.WARNING` for warning messages
        - `~LogFormatter.ERROR` for error messages
        - `~LogFormatter.DEBUG` for debug messages
        """
        self.__colormap[name] = color

    def colorize(self, name: str, msg: str, nocolor: bool = False) -> str:
        """
        Colorize the log message.

        :param name: The name of the message type
        :param msg: The message to be colorized
        :param nocolor: The no color flag (default `False`)
        :return: the colorized message

        The color of a given log message type is set by
        `~LogFormatter.set_style`. When *nocolor* is `True`, the message is not
        colorized.
        """
        if nocolor:
            return msg
        color: "_ColorFuncType | None" = self.__colormap.get(name, None)
        if color is None:
            return msg
        return color(msg)

    def format(self, name: str, msg: str) -> str:
        """
        Format the log message.

        :param name: The name of the message type
        :param msg: The message to be formatted
        :return: the formatted message
        """
        return type(self).FORMAT.format(label=name.upper(), message=msg)


class LoggerMixin:
    """
    Logging facility mixin.

    Should be used together with `StreamsProxyMixin`, which provides
    `StreamsProxyMixin.werr` method.
    """

    def __init__(self: "_LoggerProtocol") -> None:
        """
        Initialize the logger.

        The default formatter is an instance of `LogFormatter`, the default
        verbosity level is 1, and the default debug level is 0.
        """
        self.__logpath: "pathlib.Path | None" = None
        self.__formatter: LogFormatter = LogFormatter()
        self.__vlevel: int = 1
        self.__dlevel: int = 0

    def set_logger_props(
        self: "_LoggerProtocol",
        logpath: "pathlib.Path | None" = None,
        formatter: "LogFormatter | None" = None,
        vlevel: "int | None" = None,
        dlevel: "int | None" = None,
    ) -> None:
        """
        Set logger properties.

        :param logpath: The path to the log file
        :param formatter: The log formatter
        :param vlevel: The verbosity level
        :param dlevel: The debug level

        The property is set only if it is not `None`.
        """
        if logpath is not None:
            self.__logpath = logpath
        if formatter is not None:
            self.__formatter = formatter
        if vlevel is not None:
            self.__vlevel = vlevel
        if dlevel is not None:
            self.__dlevel = dlevel

    def set_log_style(
        self: "_LoggerProtocol", name: str, color: "_ColorFuncType"
    ) -> None:
        """
        Set the style of log messages.

        :param name: The name of the message type
        :param color: The message color

        This method changes the formatter object set by
        `~LoggerMixin.set_log_formatter`. Therefore, it is recommended to use
        this method after `~LoggerMixin.set_log_formatter`.
        """
        self.__formatter.set_style(name, color)

    def wlog(self: "_LoggerProtocol", msg: str) -> None:
        """
        Write the message to the log file.

        :param msg: The message
        """
        if self.__logpath is not None:
            with open(
                self.__logpath,
                mode="a",
                encoding="utf-8",
                errors="backslashreplace",
            ) as log:
                log.write(msg)

    def linfo(self: "_LoggerProtocol", msg: str, vlevel: int = 1) -> None:
        """
        Issue the info message.

        :param msg: The message
        :param vlevel: The verbosity level (default 1)

        The message is issued when the verbosity level is less or equal to the
        verbosity level treshold set by `set_verbosity_level` (default 1).
        """
        if vlevel <= self.__vlevel:
            self.__do_log(LogFormatter.INFO, msg)

    def lwarn(self: "_LoggerProtocol", msg: str) -> None:
        """
        Issue the warning message.

        :param msg: The message
        """
        self.__do_log(LogFormatter.WARNING, msg)

    def lerror(self: "_LoggerProtocol", msg: str) -> None:
        """
        Issue the error message.

        :param msg: The message
        """
        self.__do_log(LogFormatter.ERROR, msg)

    def ldebug(self: "_LoggerProtocol", msg: str, dlevel: int = 1) -> None:
        """
        Issue the debug message.

        :param msg: The message
        :param dlevel: The debug level (default 1)

        The message is issued when the debug level is less or equal to the
        debug level treshold set by `set_debug_level` (default 0).
        """
        if dlevel <= self.__dlevel:
            self.__do_log(LogFormatter.DEBUG, msg)

    def __do_log(self: "_LoggerProtocol", name: str, msg: str) -> None:
        """
        Write the message to both log file and error output stream.

        :param name: The name of message type
        :param msg: The message

        Format the message and write it to the log file (non-colorized) and to
        the error output stream (colorized).
        """
        msg = self.__formatter.format(name, msg)
        self.wlog(msg)
        self.werr(self.__formatter.colorize(name, msg))
