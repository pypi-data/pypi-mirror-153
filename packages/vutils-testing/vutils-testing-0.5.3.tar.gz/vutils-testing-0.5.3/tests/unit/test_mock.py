#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_mock.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-16 22:48:07 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.testing.mock` module."""

import unittest.mock

from vutils.testing.mock import (
    PatcherFactory,
    PatchingContextManager,
    PatchSpec,
    make_callable,
    make_mock,
)
from vutils.testing.testcase import TestCase
from vutils.testing.utils import make_type


class MakeMockTestCase(TestCase):
    """Test case for `make_mock`."""

    __slots__ = ()

    def test_make_mock(self):
        """
        Test `make_mock`.

        Test whether `make_mock` returns the instance of `unittest.mock.Mock`.
        """
        self.assertIsInstance(make_mock(), unittest.mock.Mock)

    def test_make_mock_with_args(self):
        """
        Test `make_mock` with arguments.

        Test whether arguments are passed to `unittest.mock.Mock`.
        """
        text = "abc"
        mock = make_mock(["write"])

        with self.assertRaises(AttributeError):
            mock.write_()

        mock.write(text)
        self.assert_called_with(mock.write, text)


class MakeCallableTestCase(TestCase):
    """Test case for `make_callable`."""

    __slots__ = ()

    def test_make_callable_with_no_args(self):
        """
        Test `make_callable` with no arguments.

        With no arguments, `make_callable` will produce callable
        `unittest.mock.Mock` object returning `None`.
        """
        func = make_callable()

        self.assertIsNone(func())

    def test_make_callable_with_non_callable(self):
        """
        Test `make_callable` with non-callable.

        This will produce `unittest.mock.Mock` object that returns the
        non-callable object as its value.
        """
        func = make_callable(3)

        self.assertEqual(func(), 3)

    def test_make_callable_with_callable(self):
        """
        Test `make_callable` with callable.

        This will produce `unittest.mock.Mock` object that uses callable to
        perform the side-effect.
        """
        func = make_callable(lambda x: x + 1)

        self.assertEqual(func(3), 4)


class PatchXTestCaseBase(TestCase):
    """Base class for `PatchSpecTestCase` and `PatcherFactoryTestCase`."""

    __slots__ = ("mock", "patch", "patcher", "target")

    def setUp(self):
        """Set up the test."""
        self.mock = make_mock()
        mock_mock = make_callable(lambda *x: self.mock)
        self.patch = make_callable(lambda *x, **y: make_mock())
        self.patcher = (
            PatcherFactory()
            .add_spec("vutils.testing.mock._make_patch", new=self.patch)
            .add_spec("unittest.mock.Mock", new=mock_mock)
        )
        self.target = "__main__.print"


class PatchSpecTestCase(PatchXTestCaseBase):
    """Test case for `PatchSpec`."""

    __slots__ = ()

    def test_patch_spec_without_setupfunc(self):
        """Test `PatchSpec` with *setupfunc* set to `None`."""
        with self.patcher.patch():
            PatchSpec(self.target, None)()

        self.assert_called_with(self.patch, self.target, self.mock)

    def test_patch_spec_with_setupfunc(self):
        """Test `PatchSpec` with *setupfunc* given."""
        setupfunc = make_callable()

        with self.patcher.patch():
            PatchSpec(self.target, setupfunc)()

        self.assert_called_with(setupfunc, self.mock)
        self.assert_called_with(self.patch, self.target, self.mock)

    def test_patch_spec_with_all_args(self):
        """Test `PatchSpec` with all arguments given."""
        setupfunc = make_callable()
        new = 1

        with self.patcher.patch():
            PatchSpec(self.target, setupfunc, new=new, create=True)()

        self.assert_called_with(setupfunc, new)
        self.assert_called_with(self.patch, self.target, new, create=True)

    def test_patch_spec_for_side_effects(self):
        """Test `PatchSpec` for side effects."""
        new = 1
        patchspec = PatchSpec(self.target, None, new=new)

        with self.patcher.patch():
            patchspec()

        self.assert_called_with(self.patch, self.target, new)

        with self.patcher.patch():
            patchspec()

        self.assert_called_with(self.patch, self.target, new)


class PatchingContextManagerTestCase(TestCase):
    """Test case for `PatchingContextManager`."""

    __slots__ = ()

    def test_patching_context_manager(self):
        """Test `PatchingContextManager`."""
        func = make_callable()

        mock_a = make_mock()
        mock_a.start = make_callable(lambda *x: func(1))
        mock_a.stop = make_callable(lambda *x: func(2))

        mock_b = make_mock()
        mock_b.start = make_callable(lambda *x: func(3))
        mock_b.stop = make_callable(lambda *x: func(4))

        with PatchingContextManager([mock_a, mock_b]):
            pass

        self.assertEqual(
            func.mock_calls,
            [
                unittest.mock.call(1),
                unittest.mock.call(3),
                unittest.mock.call(4),
                unittest.mock.call(2),
            ],
        )


class PatcherFactoryTestCase(PatchXTestCaseBase):
    """Test case for `PatcherFactory`."""

    __slots__ = ()

    def test_patcher_factory(self):
        """Test `PatcherFactory`."""
        setupfunc_a = make_callable()
        setupfunc_b = make_callable()
        patcher_klass = make_type(
            "FooPatcher", PatcherFactory, {"setup": setupfunc_a}
        )

        new = 42
        patcher = patcher_klass()
        patcher.add_spec(self.target, setupfunc_b, new=new, create=True)

        with self.patcher.patch():
            with patcher.patch():
                pass

        self.assert_called_with(setupfunc_a)
        self.assert_called_with(setupfunc_b, new)
        self.assert_called_with(self.patch, self.target, new, create=True)
