#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_version.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-06-21 23:58:43 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Test `vutils.testing.version` module."""

from vutils.testing.testcase import TestCase
from vutils.testing.version import __version__


class VersionTestCase(TestCase):
    """Test case for version."""

    __slots__ = ()

    def test_version(self):
        """Test if version is defined properly."""
        self.assertIsInstance(__version__, str)
