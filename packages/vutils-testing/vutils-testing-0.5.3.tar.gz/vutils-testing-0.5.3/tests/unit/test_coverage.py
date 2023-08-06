#                                                         -*- coding: utf-8 -*-
# File:    ./tests/unit/test_coverage.py
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2022-06-03 21:49:58 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#
"""Coverage tests."""

import pytest

from vutils.testing.utils import cover_typing

from .common import SYMBOLS


@pytest.mark.order("last")
def test_typing_code_is_covered():
    """
    Ensure typing code coverage.

    This is a dummy test that executes `cover_typing` to ensure that the code
    under ``if TYPE_CHECKING:`` branch is covered. Since `cover_typing` reloads
    the module, run this test as last to prevent mangling of yet imported
    modules.
    """
    cover_typing("vutils.testing.mock", SYMBOLS)
    cover_typing("vutils.testing.testcase", SYMBOLS)
    cover_typing("vutils.testing.utils", SYMBOLS)
