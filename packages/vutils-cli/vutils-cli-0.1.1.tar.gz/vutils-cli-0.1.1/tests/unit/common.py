#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/common.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-12 10:54:19 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Shared test code and data."""

import unittest.mock

from vutils.testing.mock import PatcherFactory, make_mock

from vutils.cli.application import ApplicationMixin
from vutils.cli.errors import ApplicationError
from vutils.cli.io import StreamsProxyMixin
from vutils.cli.logging import LoggerMixin

SYMBOLS = (
    "_ExcType",
    "_ExitExcType",
    "_ColorFuncType",
    "_StreamsProtocol",
    "_LoggerProtocol",
    "_ApplicationProtocol",
)

LOGFILE = "log.txt"
ERR_TEST = 2
MESSAGE = "test message"
UKEY = "foo"
CS_RESET_ALL = "</color:all>"
CS_BRIGHT = "<color:bright>"
CF_RESET = "</color>"
CF_RED = "<color:red>"
CF_GREEN = "<color:green>"
CF_YELLOW = "<color:yellow>"
CF_LIGHTYELLOW_EX = "<color:light_yellow_ex>"
CF_BLUE = "<color:blue>"


def make_io_mock():
    """
    Make input/output mocking object.

    :return: the mocking object

    The returned mocking object accepts only calls to ``write`` method.
    """
    return make_mock(["write"])


def on_exit_log(ecode):
    """
    Make a log item issued by `ApplicationMixin.on_exit`.

    :param ecode: The exit code
    :return: the log item
    """
    return (f"Application exited with exit code {ecode}\n", 2)


def on_error_log(exc):
    """
    Make a log item issued by `ApplicationMixin.on_error`.

    :param exc: The exception object
    :return: the log item
    """
    return (f"Exception caught: {exc}\n",)


class ModulePatcher(PatcherFactory):
    """Patcher for builtin, `sys` and `colorama` modules."""

    __slots__ = (
        "mock_open",
        "sys_argv",
        "sys_exit",
        "sys_stdout",
        "sys_stderr",
        "colorama_style",
        "colorama_fore",
    )

    @staticmethod
    def setup_colorama_style(style):
        """
        Set up `colorama.Style` mock.

        :param style: The mock of `colorama.Style`.
        """
        style.RESET_ALL = CS_RESET_ALL
        style.BRIGHT = CS_BRIGHT

    @staticmethod
    def setup_colorama_fore(fore):
        """
        Set up `colorama.Fore` mock.

        :param fore: The mock of `colorama.Fore`
        """
        fore.RESET = CF_RESET
        fore.RED = CF_RED
        fore.GREEN = CF_GREEN
        fore.YELLOW = CF_YELLOW
        fore.LIGHTYELLOW_EX = CF_LIGHTYELLOW_EX
        fore.BLUE = CF_BLUE

    def setup(self):
        """Set up the patcher."""
        self.mock_open = unittest.mock.mock_open()
        self.sys_argv = make_mock()
        self.sys_exit = make_mock()
        self.sys_stdout = make_io_mock()
        self.sys_stderr = make_io_mock()
        self.colorama_style = make_mock(["RESET_ALL", "BRIGHT"])
        self.colorama_fore = make_mock(
            ["RESET", "RED", "GREEN", "YELLOW", "LIGHTYELLOW_EX", "BLUE"]
        )

        self.add_spec("builtins.open", new=self.mock_open)
        self.add_spec("sys.argv", new=self.sys_argv)
        self.add_spec("sys.exit", new=self.sys_exit)
        self.add_spec("sys.stdout", new=self.sys_stdout)
        self.add_spec("sys.stderr", new=self.sys_stderr)
        self.add_spec(
            "colorama.Style",
            self.setup_colorama_style,
            new=self.colorama_style,
        )
        self.add_spec(
            "colorama.Fore", self.setup_colorama_fore, new=self.colorama_fore
        )


class ErrorA(ApplicationError):
    """Test error."""

    __slots__ = ()

    def __init__(self):
        """Initialize the error."""
        ApplicationError.__init__(self)


class ErrorB(Exception):
    """Test error."""

    __slots__ = ()

    def __init__(self):
        """Initialize the error."""
        Exception.__init__(self)

    def __repr__(self):
        """
        Get the error representation.

        :retutn: the error representation
        """
        return f"{type(self).__name__}()"

    def __str__(self):
        """
        Get the error representation.

        :retutn: the error representation
        """
        return repr(self)


class LoggerA:
    """Test logger mixin."""

    __slots__ = ("stream",)

    def __init__(self):
        """Initialize the logger."""
        self.stream = []

    def linfo(self, *args):
        """
        Implement dummy `LoggerMixin.linfo` that records its arguments.

        :param args: Arguments
        """
        self.stream.append(args)

    def lerror(self, *args):
        """
        Implement dummy `LoggerMixin.lerror` that records its arguments.

        :param args: Arguments
        """
        self.stream.append(args)


class LoggerB(LoggerMixin, StreamsProxyMixin):
    """Test logger."""

    __slots__ = ()

    def __init__(self):
        """Initialize the logger."""
        LoggerMixin.__init__(self)
        StreamsProxyMixin.__init__(self)


class ApplicationA(ApplicationMixin, LoggerA):
    """Test application."""

    CMD_EXIT = "test-exit"
    CMD_ERROR = "test-error"
    CMD_XERROR = "test-error-extra"
    CMD_RAISE_A = "test-raise-a"
    CMD_RAISE_B = "test-raise-b"
    __slots__ = ()

    def __init__(self):
        """Initialize the application."""
        ApplicationMixin.__init__(self)
        LoggerA.__init__(self)

    def main(self, argv):
        """
        Provide application entry point.

        :param argv: The list of arguments
        :return: the exit code
        :raises ErrorA: when 0th argument is set ot ``test-raise-a``
        :raises ErrorB: when 0th argument is set ot ``test-raise-b``

        The application behaves like follows:
        - with no argument return 0
        - with unknown argument return 1
        - with 0th argument set to ``test-exit`` calls `ApplicationMixin.exit`
          with ``ERR_TEST``
        - with 0th argument set to ``test-error`` calls
          `ApplicationMixin.error`
          with ``MESSAGE``
        - with 0th argument set to ``test-error-extra`` calls
          `ApplicationMixin.error` with ``MESSAGE`` and ``ERR_TEST``
        - with 0th argument set to ``test-raise-a`` raises `ErrorA`
        - with 0th argument set to ``test-raise-b`` raises `ErrorB`
        """
        cls = type(self)

        if not argv:
            return cls.EXIT_SUCCESS
        cmd = argv[0]

        if cmd == cls.CMD_EXIT:
            self.exit(ERR_TEST)
        elif cmd == cls.CMD_ERROR:
            self.error(MESSAGE)
        elif cmd == cls.CMD_XERROR:
            self.error(MESSAGE, ERR_TEST)
        elif cmd == cls.CMD_RAISE_A:
            raise ErrorA()
        elif cmd == cls.CMD_RAISE_B:
            raise ErrorB()

        return cls.EXIT_FAILURE
