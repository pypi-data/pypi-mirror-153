"""Tests for the metaman package."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Callable

from _pytest.monkeypatch import MonkeyPatch
from pytest import mark

from metaman import Inspector, register_function_factory


params = mark.parametrize


def test_inspector__SYS_PATH_BUG(monkeypatch: MonkeyPatch) -> None:
    """Regression test for bug in Inspector.

    This bug occurs when sys.path contains Path objects instead of strings.
    """
    monkeypatch.setattr("sys.path", [Path(p) for p in sys.path])
    inspector = Inspector()
    assert hasattr(inspector, "module_name")


def test_register_function_factory() -> None:
    """Tests the register_function_factory() function."""

    registry: list[Callable[[], int]] = []
    register = register_function_factory(registry)

    @register
    def foo() -> int:
        return 1

    @register
    def bar() -> int:
        return 2

    assert sum(func() for func in registry) == 3

    @register  # type: ignore[arg-type]
    def baz() -> str:
        return "baz"
