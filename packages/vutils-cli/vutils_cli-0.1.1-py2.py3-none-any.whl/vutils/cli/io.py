#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/cli/io.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-07-11 16:17:41 +0200
# Project: vutils-cli: Auxiliary library for writing CLI applications
#
# SPDX-License-Identifier: MIT
#
"""CLI input/output."""

import sys
from typing import TextIO

import colorama


def nocolor(text: str) -> str:
    """
    Make the text as it is.

    :param text: The text
    :return: the unchanged text
    """
    return text


def red(text: str) -> str:
    """
    Make the text red.

    :param text: The text
    :return: the text colored to red
    """
    return (
        f"{colorama.Style.BRIGHT}{colorama.Fore.RED}"
        f"{text}"
        f"{colorama.Style.RESET_ALL}"
    )


def green(text: str) -> str:
    """
    Make the text green.

    :param text: The text
    :return: the text colored to green
    """
    return (
        f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}"
        f"{text}"
        f"{colorama.Style.RESET_ALL}"
    )


def brown(text: str) -> str:
    """
    Make the text brown.

    :param text: The text
    :return: the text colored to brown
    """
    return f"{colorama.Fore.YELLOW}{text}{colorama.Fore.RESET}"


def yellow(text: str) -> str:
    """
    Make the text yellow.

    :param text: The text
    :return: the text colored to yellow
    """
    return (
        f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTYELLOW_EX}"
        f"{text}"
        f"{colorama.Style.RESET_ALL}"
    )


def blue(text: str) -> str:
    """
    Make the text blue.

    :param text: The text
    :return: the text colored to blue
    """
    return (
        f"{colorama.Style.BRIGHT}{colorama.Fore.BLUE}"
        f"{text}"
        f"{colorama.Style.RESET_ALL}"
    )


class StreamsProxyMixin:
    """
    I/O streams proxy mixin.

    Mixin that provides interface to manipulating streams. Can be used with
    `ApplicationMixin` and `LoggerMixin`.
    """

    def __init__(self) -> None:
        """
        Initialize streams.

        Default streams are `sys.stdout` for the output stream and `sys.stderr`
        for the error output stream.
        """
        self.__output: TextIO = sys.stdout
        self.__errout: TextIO = sys.stderr

    def set_streams(
        self,
        ostream: "TextIO | None" = None,
        estream: "TextIO | None" = None,
    ) -> None:
        """
        Set output and error output streams.

        :param ostream: The output stream
        :param estream: The error output stream

        Output stream and error output stream is not set if *ostream* and
        *estream* is `None`, respectively.
        """
        if ostream is not None:
            self.__output = ostream
        if estream is not None:
            self.__errout = estream

    def wout(self, text: str) -> None:
        """
        Write *text* to the output stream.

        :param text: The text
        """
        self.__output.write(text)

    def werr(self, text: str) -> None:
        """
        Write *text* to the error output stream.

        :param text: The text
        """
        self.__errout.write(text)
