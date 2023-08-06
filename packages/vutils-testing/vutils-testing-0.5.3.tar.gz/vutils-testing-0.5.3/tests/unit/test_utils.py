#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_utils.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-16 21:22:45 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.testing.utils` module."""

import sys

from vutils.testing.mock import make_mock
from vutils.testing.testcase import TestCase
from vutils.testing.utils import AssertRaises, LazyInstance, make_type

from .common import (
    FOO_CONSTANT,
    FooError,
    StderrPatcher,
    StderrWriter,
    func_a,
    func_b,
)


class MakeTypeTestCase(TestCase):
    """Test case for `make_type`."""

    __slots__ = ()

    def verify_bases(self, klass, bases):
        """
        Verify that *klass* has same bases as listed in *bases*.

        :param klass: The class
        :param bases: The list of base classes
        """
        self.assertCountEqual(klass.__bases__, bases)
        for i, base in enumerate(bases):
            self.assertIs(klass.__bases__[i], base)

    def test_make_type_with_no_bases(self):
        """Test `make_type` when called with no bases."""
        new_type = make_type("NewType")

        self.verify_bases(new_type, [object])

    def test_make_type_with_one_base(self):
        """Test `make_type` when called with one base."""
        error_a = make_type("ErrorA", Exception)
        error_b = make_type("ErrorB", (Exception,))

        self.verify_bases(error_a, [Exception])
        self.verify_bases(error_b, [Exception])

    def test_make_type_with_more_bases(self):
        """Test `make_type` when called with more bases."""
        type_one = make_type("TypeOne")
        type_two = make_type("TypeTwo")
        type_three = make_type("TypeThree", (type_one, type_two))

        self.verify_bases(type_three, [type_one, type_two])

    def test_make_type_with_members(self):
        """Test `make_type` when called with *members*."""
        type_a = make_type("TypeA", members={"a": 1})
        type_b = make_type("TypeB", type_a, {"b": 2})

        self.verify_bases(type_a, [object])
        self.verify_bases(type_b, [type_a])

        self.assertEqual(type_a.a, 1)
        self.assertEqual(type_b.a, 1)
        self.assertEqual(type_b.b, 2)


class LazyInstanceTestCase(TestCase):
    """Test case for `LazyInstance`."""

    __slots__ = ()

    def test_lazy_initialization(self):
        """Test lazy initialization."""
        code = 42
        label = "LABEL"
        message = "Hello!"
        patcher = StderrPatcher()
        writer = LazyInstance(StderrWriter).create(code, label=label)
        write_func = writer.write

        with patcher.patch():
            write_func(message)

        self.assertIs(writer.stream, sys.stderr)
        self.assertEqual(
            patcher.stream.getvalue(),
            StderrWriter.format(code, label, message),
        )
        self.assertIsNot(writer.get_instance(), writer.get_instance())

    def test_instance_caching(self):
        """Test instance caching."""
        writer = LazyInstance(StderrWriter, initialize_once=True).create(
            1, "FOO"
        )

        self.assertIs(writer.get_instance(), writer.get_instance())


class AssertRaisesTestCase(TestCase):
    """Test case for `AssertRaises`."""

    __slots__ = ()

    def run_and_verify(self, func):
        """
        Run *func* and verify results.

        :param func: The function to run
        """
        mock = make_mock()
        func(mock)
        self.assertEqual(mock.foo, FOO_CONSTANT)

    def test_assert_raises(self):
        """Test `AssertRaises` works as expected."""
        wfunc_b = AssertRaises(self, func_b, FooError)

        self.run_and_verify(func_a)
        self.run_and_verify(wfunc_b)
        self.assertEqual(wfunc_b.get_exception().detail, FOO_CONSTANT)
        self.assertIsNone(wfunc_b.get_exception())
