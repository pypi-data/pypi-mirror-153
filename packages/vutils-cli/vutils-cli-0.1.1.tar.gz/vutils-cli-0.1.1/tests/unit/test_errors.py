#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_errors.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-08-28 21:14:57 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.cli.errors` module."""

from vutils.testing.testcase import TestCase

from vutils.cli.errors import AppExitError, ApplicationError


class ApplicationErrorTestCase(TestCase):
    """Test case for `ApplicationError`."""

    __slots__ = ()

    def test_application_error(self):
        """Test the `ApplicationError` basic usage."""
        with self.assertRaises(ApplicationError) as context_manager:
            raise ApplicationError()
        exception = context_manager.exception

        self.assertEqual(exception.detail(), "")
        self.assertEqual(repr(exception), "ApplicationError()")
        self.assertEqual(str(exception), repr(exception))


class AppExitErrorTestCase(TestCase):
    """Test case for `AppExitError`."""

    __slots__ = ()

    def test_app_exit_error(self):
        """Test the `AppExitError` basic usage."""
        ecode = 2
        self.do_test(1)
        self.do_test(ecode, ecode)

    def do_test(self, value, *args):
        """
        Do the `AppExitError` basic usage test.

        :param value: The expected value of exit code
        :param args: Arguments to be passed to the `AppExitError` constructor
        """
        with self.assertRaises(AppExitError) as context_manager:
            raise AppExitError(*args)
        exception = context_manager.exception

        self.assertEqual(exception.ecode, value)
        self.assertEqual(f"{exception}", f"AppExitError(exit_code={value})")
