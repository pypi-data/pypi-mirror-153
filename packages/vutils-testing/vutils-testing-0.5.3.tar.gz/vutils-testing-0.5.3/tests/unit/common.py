#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/common.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-22 23:46:47 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Shared test code and data."""

import io
import sys

from vutils.testing.mock import PatcherFactory

SYMBOLS = (
    "_ArgsType",
    "_KwArgsType",
    "_ExcType",
    "_MockableType",
    "_ReturnsType",
    "_SetupFuncType",
    "_BasesType",
    "_MembersType",
    "_ExcSpecType",
    "_PatchType",
    "_TypeType",
    "_FuncType",
    "_make_patch",
)
FOO_CONSTANT = 42


class FooError(Exception):
    """Dummy exception."""

    __slots__ = ("detail",)

    def __init__(self, detail):
        """
        Initialize the exception object.

        :param detail: The error detail
        """
        Exception.__init__(self, detail)
        self.detail = detail


class StderrPatcher(PatcherFactory):
    """`sys.stderr` patcher."""

    __slots__ = ("stream",)

    def setup(self):
        """Set up the patcher."""
        self.stream = io.StringIO()
        self.add_spec("sys.stderr", new=self.stream)


class StderrWriter:
    """Dummy standard error output writer."""

    __slots__ = ("stream", "code", "label")

    def __init__(self, code, label=""):
        """
        Initialize the writer.

        :param code: The code
        :param label: The label
        """
        self.stream = sys.stderr
        self.code = code
        self.label = label

    @staticmethod
    def format(code, label, text):
        """
        Format the message.

        :param code: The code
        :param label: The label
        :param text: The text
        :return: formatted message
        """
        return f"({code})[{label}] {text}\n"

    def write(self, text):
        """
        Write *text* to stream.

        :param text: The text
        """
        self.stream.write(self.format(self.code, self.label, text))


def func_a(mock):
    """
    Modify *mock*.

    :param mock: The mock object
    """
    mock.foo = FOO_CONSTANT


def func_b(mock):
    """
    Modify *mock* and raise `FooError`.

    :param mock: The mock object
    :raises FooError: when called
    """
    func_a(mock)
    raise FooError(FOO_CONSTANT)
