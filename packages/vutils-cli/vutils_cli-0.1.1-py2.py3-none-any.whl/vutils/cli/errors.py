#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/cli/errors.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-07-09 22:37:01 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""Definitions of errors."""


class ApplicationError(Exception):
    """Base class for all application errors."""

    DEFAULT_DETAIL: str = ""
    __slots__ = ()

    def __init__(self) -> None:
        """Initialize the error object."""
        Exception.__init__(self)

    def detail(self) -> str:
        """
        Get the error detail.

        :return: the error detail
        """
        return type(self).DEFAULT_DETAIL

    def __repr__(self) -> str:
        """
        Get the error representation.

        :return: the error representation
        """
        return f"{type(self).__name__}({self.detail()})"

    def __str__(self) -> str:
        """
        Get the error representation (`str` alias).

        :return: the error representation
        """
        return repr(self)


class AppExitError(ApplicationError):
    """Used to signal the exit."""

    __slots__ = ("ecode",)

    def __init__(self, ecode: int = 1) -> None:
        """
        Initialize the error object.

        :param ecode: The exit code (default 1)
        """
        ApplicationError.__init__(self)
        self.ecode: int = ecode

    def detail(self) -> str:
        """
        Get the error detail.

        :return: the error detail
        """
        return f"exit_code={self.ecode}"
