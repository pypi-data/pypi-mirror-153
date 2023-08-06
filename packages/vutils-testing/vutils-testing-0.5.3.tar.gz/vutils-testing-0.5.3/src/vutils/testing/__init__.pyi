#                                                         -*- coding: utf-8 -*-
# File:    ./src/vutils/testing/__init__.pyi
# Author:  Jiří Kučera <sanczes AT gmail.com>
# Date:    2021-09-17 14:14:50 +0200
# Project: vutils-testing: Auxiliary library for writing tests
#
# SPDX-License-Identifier: MIT
#

from collections.abc import Callable
from unittest.mock import Mock, _patch

from typing_extensions import TypeAlias

_ArgsType: TypeAlias = tuple[object, ...]
_KwArgsType: TypeAlias = dict[str, object]
_ExcType: TypeAlias = type[Exception]
_MockableType: TypeAlias = Mock | object

_ReturnsType: TypeAlias = object | Callable[[object], object] | None
_SetupFuncType: TypeAlias = Callable[[_MockableType], None] | None
_BasesType: TypeAlias = type | tuple[type, ...] | None
_MembersType: TypeAlias = _KwArgsType | None
_ExcSpecType: TypeAlias = _ExcType | tuple[_ExcType, ...]
_PatchType: TypeAlias = _patch[_MockableType]

class _TypeType:
    def __call__(self, *args: object, **kwargs: object) -> object: ...

class _FuncType:
    def __call__(self, *args: object, **kwargs: object) -> object: ...

def _make_patch(
    target: object, mock: _MockableType, **kwargs: object
) -> _PatchType: ...
