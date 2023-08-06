#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/cli/application.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-07-07 02:34:26 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Command-line interface application classes."""

import sys
from typing import TYPE_CHECKING, NoReturn

from vutils.cli.errors import AppExitError, ApplicationError

if TYPE_CHECKING:
    from vutils.cli import _ApplicationProtocol, _ExcType, _ExitExcType


class ApplicationMixin:
    """
    Mixin for creating CLI applications.

    Should be used together with `LoggerMixin` and `StreamsProxyMixin`.
    """

    EXIT_SUCCESS: int = 0
    EXIT_FAILURE: int = 1
    EXIT_EXCEPTION: "_ExitExcType" = AppExitError

    def __init__(self: "_ApplicationProtocol") -> None:
        """Initialize the mixin."""
        self.__elist: "list[_ExcType]" = []
        self.catch(ApplicationError)

    def catch(self: "_ApplicationProtocol", exc: "_ExcType") -> None:
        """
        Register an exception to be caught.

        :param exc: The exception class

        Registered exceptions that are raised by `main` are caught and passed
        to `on_error` to be further processed. `ApplicationError` is registered
        by default.
        """
        if exc not in self.__elist:
            self.__elist.append(exc)

    def error(
        self: "_ApplicationProtocol", msg: str, ecode: int = 1
    ) -> NoReturn:
        """
        Issue an error and exit.

        :param msg: The error message
        :param ecode: The exit code (default 1)
        :raises AppExitError: when invoked
        """
        self.lerror(msg)
        self.exit(ecode)

    def exit(self: "_ApplicationProtocol", ecode: int) -> NoReturn:
        """
        Exit the application by raising `AppExitError`.

        :param ecode: The exit code
        :raises AppExitError: when invoked
        """
        raise type(self).EXIT_EXCEPTION(ecode)

    def main(self: "_ApplicationProtocol", unused_argv: "list[str]") -> int:
        """
        Provide the application entry point.

        :param unused_argv: The list of application arguments
        :return: the exit code
        """
        return type(self).EXIT_SUCCESS

    def run(self: "_ApplicationProtocol", argv: "list[str]") -> int:
        """
        Run the application.

        :param argv: The list of application arguments
        :return: the exit code
        :raises Exception: if the exception raised by `main` is not handled

        Invoke the `main`, handle the error, and either return the exit code
        returned by `main` or the exit code returned by `on_error` error
        handler.
        """
        try:
            ecode = self.main(argv)
        except AppExitError as exc:
            ecode = exc.ecode
            self.on_exit(ecode)
        except tuple(self.__elist) as exc:
            ecode = self.on_error(exc)
        return ecode

    def on_exit(self: "_ApplicationProtocol", ecode: int) -> None:
        """
        Specify what to do on `exit`.

        :param ecode: The exit code

        By default, log the exit code if the verbosity level is set to 2 or
        higher.
        """
        self.linfo(f"Application exited with exit code {ecode}\n", 2)

    def on_error(self: "_ApplicationProtocol", exc: Exception) -> int:
        """
        Specify what to do on error.

        :param exc: The caught exception
        :return: the exit code

        Default implementation logs the error and returns 1.
        """
        self.lerror(f"Exception caught: {exc}\n")
        return type(self).EXIT_FAILURE

    @classmethod
    def start(
        cls: "type[_ApplicationProtocol]", modname: str = "__main__"
    ) -> None:
        """
        Start the application.

        :param modname: The module name (default ``__main__``)

        If the module name is ``__main__``, run the application.
        """
        if modname == "__main__":
            sys.exit(cls().run(sys.argv))
