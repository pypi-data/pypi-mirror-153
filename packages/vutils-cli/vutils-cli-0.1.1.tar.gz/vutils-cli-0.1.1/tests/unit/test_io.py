#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_io.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-30 08:31:15 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.cli.io` module."""

from vutils.testing.testcase import TestCase
from vutils.testing.utils import LazyInstance

from vutils.cli.io import (
    StreamsProxyMixin,
    blue,
    brown,
    green,
    nocolor,
    red,
    yellow,
)

from .common import (
    CF_BLUE,
    CF_GREEN,
    CF_LIGHTYELLOW_EX,
    CF_RED,
    CF_RESET,
    CF_YELLOW,
    CS_BRIGHT,
    CS_RESET_ALL,
    MESSAGE,
    ModulePatcher,
    make_io_mock,
)


class ColorOutputTestCase(TestCase):
    """Test case for color output."""

    __slots__ = ("patcher",)

    def setUp(self):
        """Set up the test."""
        self.patcher = ModulePatcher()

    def test_output_coloring(self):
        """Test the output coloring functions."""
        self.do_test(nocolor, MESSAGE, MESSAGE)
        self.do_test(
            red, MESSAGE, f"{CS_BRIGHT}{CF_RED}{MESSAGE}{CS_RESET_ALL}"
        )
        self.do_test(
            green, MESSAGE, f"{CS_BRIGHT}{CF_GREEN}{MESSAGE}{CS_RESET_ALL}"
        )
        self.do_test(brown, MESSAGE, f"{CF_YELLOW}{MESSAGE}{CF_RESET}")
        self.do_test(
            yellow,
            MESSAGE,
            f"{CS_BRIGHT}{CF_LIGHTYELLOW_EX}{MESSAGE}{CS_RESET_ALL}",
        )
        self.do_test(
            blue, MESSAGE, f"{CS_BRIGHT}{CF_BLUE}{MESSAGE}{CS_RESET_ALL}"
        )

    def do_test(self, colorfunc, text, result):
        """
        Do the coloring test.

        :param colorfunc: The coloring function
        :param text: The text to be colorized
        :param result: The expected result
        """
        value = ""
        with self.patcher.patch():
            value = colorfunc(text)
        self.assertEqual(value, result)


class StreamsProxyMixinTestCase(TestCase):
    """Test case for `StreamsProxyMixin`."""

    __slots__ = ("patcher", "proxy")

    def setUp(self):
        """Set up the test."""
        self.patcher = ModulePatcher()
        self.proxy = LazyInstance(StreamsProxyMixin, True).create()

    def test_default_streams(self):
        """Test `StreamsProxyMixin` with default streams."""
        with self.patcher.patch():
            self.proxy.wout(MESSAGE)
            self.proxy.werr(MESSAGE)

        self.assert_called_with(self.patcher.sys_stdout.write, MESSAGE)
        self.assert_called_with(self.patcher.sys_stderr.write, MESSAGE)

    def test_set_ostream(self):
        """Test setting the output stream."""
        stream = make_io_mock()

        with self.patcher.patch():
            self.proxy.set_streams(ostream=stream)
            self.proxy.wout(MESSAGE)
            self.proxy.werr(MESSAGE)

        self.assert_called_with(stream.write, MESSAGE)
        self.assert_not_called(self.patcher.sys_stdout.write)
        self.assert_called_with(self.patcher.sys_stderr.write, MESSAGE)

    def test_set_estream(self):
        """Test setting the error output stream."""
        stream = make_io_mock()

        with self.patcher.patch():
            self.proxy.set_streams(estream=stream)
            self.proxy.wout(MESSAGE)
            self.proxy.werr(MESSAGE)

        self.assert_called_with(stream.write, MESSAGE)
        self.assert_called_with(self.patcher.sys_stdout.write, MESSAGE)
        self.assert_not_called(self.patcher.sys_stderr.write)
