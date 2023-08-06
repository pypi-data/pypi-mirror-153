#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_testcase.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-11 08:30:17 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.testing.testcase` module."""

from vutils.testing.mock import make_mock
from vutils.testing.testcase import TestCase


class TestCaseTestCase(TestCase):
    """Test case for `TestCase`."""

    __slots__ = ()

    def test_assert_called_with(self):
        """Test `TestCase.assert_called_with` method."""
        mock = make_mock(["foo"])

        mock.foo()
        self.assert_called_with(mock.foo)

        mock.foo(1, 2)
        self.assert_called_with(mock.foo, 1, 2)

        mock.foo(bar=3, baz=4)
        self.assert_called_with(mock.foo, bar=3, baz=4)

        mock.foo(5, quux=6)
        self.assert_called_with(mock.foo, 5, quux=6)

    def test_assert_not_called(self):
        """Test `TestCase.assert_not_called` method."""
        mock = make_mock(["foo"])

        self.assert_not_called(mock.foo)
