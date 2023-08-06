#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_application.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-08-29 12:15:57 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.cli.application` module."""

from vutils.testing.testcase import TestCase

from vutils.cli.application import ApplicationMixin

from .common import (
    ERR_TEST,
    MESSAGE,
    ApplicationA,
    ErrorA,
    ErrorB,
    ModulePatcher,
    on_error_log,
    on_exit_log,
)


class ApplicationMixinTestCase(TestCase):
    """Test case for `ApplicationMixin`."""

    __slots__ = ()

    def test_application_start(self):
        """Test `ApplicationMixin.start`."""
        patcher = ModulePatcher()

        with patcher.patch():
            ApplicationMixin.start()
        self.assert_called_with(
            patcher.sys_exit, ApplicationMixin.EXIT_SUCCESS
        )

        with patcher.patch():
            ApplicationMixin.start("foo")
        self.assert_not_called(patcher.sys_exit)

    def test_error_management(self):
        """Test `ApplicationMixin` error management."""
        app = ApplicationA()

        result = app.run([ApplicationA.CMD_EXIT])
        self.assertEqual(result, ERR_TEST)
        self.assertEqual(app.stream, [on_exit_log(ERR_TEST)])
        app.stream.clear()

        result = app.run([ApplicationA.CMD_ERROR])
        self.assertEqual(result, 1)
        self.assertEqual(app.stream, [(MESSAGE,), on_exit_log(1)])
        app.stream.clear()

        result = app.run([ApplicationA.CMD_XERROR])
        self.assertEqual(result, ERR_TEST)
        self.assertEqual(app.stream, [(MESSAGE,), on_exit_log(ERR_TEST)])
        app.stream.clear()

        result = app.run([ApplicationA.CMD_RAISE_A])
        self.assertEqual(result, ApplicationA.EXIT_FAILURE)
        self.assertEqual(app.stream, [on_error_log(ErrorA())])
        app.stream.clear()

        self.assertRaises(ErrorB, app.run, [ApplicationA.CMD_RAISE_B])
        self.assertEqual(app.stream, [])

        app.catch(ErrorB)

        result = app.run([ApplicationA.CMD_RAISE_B])
        self.assertEqual(result, ApplicationA.EXIT_FAILURE)
        self.assertEqual(app.stream, [on_error_log(ErrorB())])
        app.stream.clear()
