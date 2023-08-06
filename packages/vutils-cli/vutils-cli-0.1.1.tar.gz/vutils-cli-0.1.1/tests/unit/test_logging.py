#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_logging.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-12 20:09:34 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.cli.logging` module."""

from vutils.testing.testcase import TestCase
from vutils.testing.utils import LazyInstance

from vutils.cli.io import brown
from vutils.cli.logging import LogFormatter

from .common import (
    CF_BLUE,
    CF_LIGHTYELLOW_EX,
    CF_RED,
    CF_RESET,
    CF_YELLOW,
    CS_BRIGHT,
    CS_RESET_ALL,
    LOGFILE,
    MESSAGE,
    UKEY,
    LoggerB,
    ModulePatcher,
)


class LogFormatterTestCase(TestCase):
    """Test case for `LogFormatter`."""

    __slots__ = ("patcher",)

    def setUp(self):
        """Set up the test."""
        self.patcher = ModulePatcher()

    def test_log_formatting(self):
        """Test log formatting."""
        formatter = LogFormatter()

        self.assertEqual(
            self.do_colorize(formatter, LogFormatter.INFO, MESSAGE, True),
            MESSAGE,
        )
        self.assertEqual(
            self.do_colorize(formatter, LogFormatter.INFO, MESSAGE),
            f"{CS_BRIGHT}{CF_BLUE}{MESSAGE}{CS_RESET_ALL}",
        )
        self.assertEqual(
            self.do_colorize(formatter, LogFormatter.WARNING, MESSAGE),
            f"{CS_BRIGHT}{CF_LIGHTYELLOW_EX}{MESSAGE}{CS_RESET_ALL}",
        )
        self.assertEqual(
            self.do_colorize(formatter, LogFormatter.ERROR, MESSAGE),
            f"{CS_BRIGHT}{CF_RED}{MESSAGE}{CS_RESET_ALL}",
        )
        self.assertEqual(
            self.do_colorize(formatter, LogFormatter.DEBUG, MESSAGE),
            f"{CF_YELLOW}{MESSAGE}{CF_RESET}",
        )
        self.assertEqual(self.do_colorize(formatter, UKEY, MESSAGE), MESSAGE)

        formatter.set_style(UKEY, brown)

        self.assertEqual(
            self.do_colorize(formatter, UKEY, MESSAGE),
            f"{CF_YELLOW}{MESSAGE}{CF_RESET}",
        )

        self.assertEqual(
            formatter.format(UKEY, MESSAGE), f"{UKEY.upper()}: {MESSAGE}"
        )

    def do_colorize(self, formatter, *args):
        """
        Call `LogFormatter.colorize` within the patched context.

        :param args: Arguments to be passed to `LogFormatter.colorize`
        :return: the colorized text
        """
        with self.patcher.patch():
            return formatter.colorize(*args)


class LoggerMixinTestCase(TestCase):
    """Test case for `LoggerMixin`."""

    COLOR_START = {
        LogFormatter.INFO: f"{CS_BRIGHT}{CF_BLUE}",
        LogFormatter.WARNING: f"{CS_BRIGHT}{CF_LIGHTYELLOW_EX}",
        LogFormatter.ERROR: f"{CS_BRIGHT}{CF_RED}",
        LogFormatter.DEBUG: CF_YELLOW,
    }
    COLOR_END = {
        LogFormatter.INFO: CS_RESET_ALL,
        LogFormatter.WARNING: CS_RESET_ALL,
        LogFormatter.ERROR: CS_RESET_ALL,
        LogFormatter.DEBUG: CF_RESET,
    }
    __slots__ = ("patcher", "logger")

    def setUp(self):
        """Set up the test."""
        self.patcher = ModulePatcher()
        self.logger = LazyInstance(LoggerB, True).create()

    def test_set_log_style(self):
        """Test `LoggerMixin.set_log_style` method."""
        with self.patcher.patch():
            self.logger.set_log_style(LogFormatter.INFO, brown)
            self.logger.linfo(MESSAGE)
        self.assert_called_with(
            self.patcher.sys_stderr.write,
            f"{CF_YELLOW}{LogFormatter.INFO.upper()}: {MESSAGE}{CF_RESET}",
        )

    def test_set_formatter(self):
        """Test setting the formatter."""
        formatter = LogFormatter()
        formatter.set_style(LogFormatter.INFO, brown)

        with self.patcher.patch():
            self.logger.linfo(MESSAGE)
        self.assert_called_with(
            self.patcher.sys_stderr.write,
            (
                f"{CS_BRIGHT}{CF_BLUE}"
                f"{LogFormatter.INFO.upper()}: {MESSAGE}"
                f"{CS_RESET_ALL}"
            ),
        )

        self.logger.set_logger_props(formatter=formatter)

        with self.patcher.patch():
            self.logger.linfo(MESSAGE)
        self.assert_called_with(
            self.patcher.sys_stderr.write,
            f"{CF_YELLOW}{LogFormatter.INFO.upper()}: {MESSAGE}{CF_RESET}",
        )

    def test_wlog(self):
        """Test writing to the log file."""
        with self.patcher.patch():
            self.logger.linfo(MESSAGE)
        self.assert_not_called(self.patcher.mock_open)

        self.logger.set_logger_props(logpath=LOGFILE)

        with self.patcher.patch():
            self.logger.linfo(MESSAGE)
        self.patcher.mock_open.assert_called_once_with(
            LOGFILE,
            mode="a",
            encoding="utf-8",
            errors="backslashreplace",
        )
        self.assert_called_with(
            self.patcher.mock_open().write,
            f"{LogFormatter.INFO.upper()}: {MESSAGE}",
        )
        self.patcher.mock_open.reset_mock()

    def test_linfo(self):
        """Test logging info messages."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE)
            self.logger.linfo(MESSAGE)
        self.verify_logged(LogFormatter.INFO)

    def test_linfo_vlevel(self):
        """Test logging info messages with verbosity level."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE)
            self.logger.linfo(MESSAGE, 2)
        self.verify_not_logged()

    def test_set_vlevel(self):
        """Test setting the verbosity level."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE, vlevel=2)
            self.logger.linfo(MESSAGE, 2)
        self.verify_logged(LogFormatter.INFO)

    def test_lwarn(self):
        """Test logging warning messages."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE)
            self.logger.lwarn(MESSAGE)
        self.verify_logged(LogFormatter.WARNING)

    def test_lerror(self):
        """Test logging error messages."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE)
            self.logger.lerror(MESSAGE)
        self.verify_logged(LogFormatter.ERROR)

    def test_ldebug(self):
        """Test logging debug messages."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE)
            self.logger.ldebug(MESSAGE)
        self.verify_not_logged()

    def test_set_dlevel(self):
        """Test setting the debug level."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE, dlevel=1)
            self.logger.ldebug(MESSAGE)
        self.verify_logged(LogFormatter.DEBUG)

    def test_ldebug_dlevel(self):
        """Test logging debug messages with debug level."""
        with self.patcher.patch():
            self.logger.set_logger_props(logpath=LOGFILE, dlevel=1)
            self.logger.ldebug(MESSAGE, 2)
        self.verify_not_logged()

    def verify_logged(self, name):
        """
        Verify `MESSAGE` is logged.

        :param name: The name of the message type
        :raises AssertionError: when verification fails
        """
        msg = f"{name.upper()}: {MESSAGE}"
        self.assert_called_with(self.patcher.mock_open().write, msg)
        self.patcher.mock_open.reset_mock()
        self.assert_not_called(self.patcher.sys_stdout.write)
        cls = type(self)
        msg = f"{cls.COLOR_START[name]}{msg}{cls.COLOR_END[name]}"
        self.assert_called_with(self.patcher.sys_stderr.write, msg)

    def verify_not_logged(self):
        """
        Verify `MESSAGE` is not logged.

        :raises AssertionError: when verification fails
        """
        self.assert_not_called(self.patcher.mock_open)
        self.assert_not_called(self.patcher.sys_stdout.write)
        self.assert_not_called(self.patcher.sys_stderr.write)
