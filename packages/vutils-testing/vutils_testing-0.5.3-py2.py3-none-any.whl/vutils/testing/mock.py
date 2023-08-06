#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/mock.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-13 17:04:14 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Mocking utilities."""

import unittest.mock
from typing import TYPE_CHECKING, Iterable, List

if TYPE_CHECKING:
    from unittest.mock import Mock

    from vutils.testing import (
        _KwArgsType,
        _make_patch,
        _MockableType,
        _PatchType,
        _ReturnsType,
        _SetupFuncType,
    )
else:
    _make_patch = unittest.mock.patch


def make_mock(*args: object, **kwargs: object) -> "Mock":
    """
    Make the `unittest.mock.Mock` object.

    :param args: Positional arguments to be passed to the `unittest.mock.Mock`
        constructor
    :param kwargs: Key-value arguments to be passed to the `unittest.mock.Mock`
        constructor
    :return: the `unittest.mock.Mock` object
    """
    return unittest.mock.Mock(*args, **kwargs)


def make_callable(returns: "_ReturnsType" = None) -> "Mock":
    """
    Make the `unittest.mock.Mock` object that serves as a callable.

    :param returns: If callable, *returns* is treated as the *side_effect*
        parameter to `unittest.mock.Mock`. Otherwise, it is treated as the
        *return_value* parameter
    :return: the `unittest.mock.Mock` object representing the callable
    """
    if callable(returns):
        return unittest.mock.Mock(side_effect=returns)
    return unittest.mock.Mock(return_value=returns)


class PatchSpec:
    """Holds the patch specification."""

    __slots__ = ("__target", "__setupfunc", "__kwargs")

    def __init__(
        self, target: object, setupfunc: "_SetupFuncType", **kwargs: object
    ) -> None:
        """
        Initialize the patch specification.

        :param target: The target to be patched
        :param setupfunc: The function used to setup the patch
        :param kwargs: Additional arguments passed to `unittest.mock.patch`
        """
        self.__target: object = target
        self.__setupfunc: "_SetupFuncType" = setupfunc
        self.__kwargs: "_KwArgsType" = kwargs

    def __call__(self) -> "_PatchType":
        """
        Create the patcher from the specification.

        :return: the patcher

        The patcher is created in four steps:

        #. `unittest.mock.Mock` object is created
        #. if *new* is in *kwargs*, the mock object becomes *new*
        #. if *setupfunc* is not `None`, the mock object is passed to it; the
           *setupfunc* can then adjust the object
        #. the patcher is created by calling `unittest.mock.patch` with
           *target*, the mock object, and additional arguments given by
           *kwargs*, respectively
        """
        kwargs: "_KwArgsType" = self.__kwargs.copy()
        mock: "_MockableType" = kwargs.pop("new", make_mock())
        if self.__setupfunc is not None:
            self.__setupfunc(mock)
        return _make_patch(self.__target, mock, **kwargs)


class PatchingContextManager:
    """Context manager that handles the patching."""

    __slots__ = ("__patchers",)

    def __init__(self, patchers: Iterable["_PatchType"]) -> None:
        """
        Initialize the context manager.

        :param patchers: The list of patchers
        """
        self.__patchers: List["_PatchType"] = list(patchers)

    def __enter__(self) -> "PatchingContextManager":
        """
        Apply patches.

        :return: *self*
        """
        for patcher in self.__patchers:
            patcher.start()
        return self

    def __exit__(self, *args: object) -> None:
        """
        Revert applied patches in reverse order.

        :param args: Unused arguments
        """
        for patcher in reversed(self.__patchers):
            patcher.stop()


class PatcherFactory:
    r"""
    Factory for creating patchers.

    This factory allows to create and apply the set of patches simultaneously,
    omitting the nested ``with`` statements for every patch. In the following
    example, it is demonstrated how this class can be used to test the sending
    colored text to the standard output. First, define the factory that patch
    the `colorama` and `sys` modules::

        import colorama
        import io
        import sys


        class MyPatcher(PatcherFactory):

            def setup_sys(self, mock):
                self.stream = io.StringIO()
                mock.stdout = self.stream

            @staticmethod
            def setup_colorama(mock):
                mock.Fore.RESET = "</c>"
                mock.Fore.RED = "<c:red>"

            def setup(self):
                self.add_spec("__main__.colorama", self.setup_colorama)
                self.add_spec("__main__.sys", self.setup_sys)

    Next, use the factory in the test::

        def echo_red(text):
            sys.stdout.write(
                f"{colorama.Fore.RED}{text}{colorama.Fore.RESET}\n"
            )


        def test_echo_red():
            patcher = MyPatcher()
            message = "Alert!"

            with patcher.patch():
                echo_red(message)

            assert patcher.stream.getvalue() == f"<c:red>{message}</c>\n"

    The patches are applied in order as their specifications were added by
    `add_spec`.
    """

    __slots__ = ("__specs",)

    def __init__(self) -> None:
        """Initialize the factory."""
        self.__specs: List[PatchSpec] = []
        self.setup()

    def add_spec(
        self,
        target: object,
        setupfunc: "_SetupFuncType" = None,
        **kwargs: object,
    ) -> "PatcherFactory":
        """
        Add the patch specification to the factory.

        :param target: The target to be patched
        :param setupfunc: The function used to setup the patch, see `PatchSpec`
        :param kwargs: Additional arguments to `unittest.mock.patch`
        :return: *self*
        """
        self.__specs.append(PatchSpec(target, setupfunc, **kwargs))
        return self

    def setup(self) -> None:
        """Set up the factory."""

    def patch(self) -> PatchingContextManager:
        """
        Create the context manager that perform the patching.

        :return: the context manager used for patching
        """
        return PatchingContextManager([spec() for spec in self.__specs])
