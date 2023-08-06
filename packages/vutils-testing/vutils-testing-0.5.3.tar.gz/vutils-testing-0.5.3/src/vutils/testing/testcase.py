#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/testcase.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-02 00:59:53 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Extended `unittest.TestCase`."""

import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unittest.mock import Mock


class TestCase(unittest.TestCase):
    """Extended `unittest.TestCase`."""

    __slots__ = ()

    @staticmethod
    def assert_called_with(
        mock: "Mock", *args: object, **kwargs: object
    ) -> None:
        """
        Check and reset the mock call.

        :param mock: The mock object
        :param args: Expected arguments
        :param kwargs: Expected key-value arguments

        Check whether the mock object has been called with given arguments and
        reset it.
        """
        mock.assert_called_once_with(*args, **kwargs)
        mock.reset_mock()

    @staticmethod
    def assert_not_called(mock: "Mock") -> None:
        """
        Check that *mock* has not been called.

        :param mock: The mock object

        Check whether the mock object has not been called and reset it.
        """
        mock.assert_not_called()
        mock.reset_mock()
