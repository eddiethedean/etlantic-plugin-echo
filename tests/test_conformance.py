"""Public-suite-only conformance for etlantic-plugin-echo."""

from __future__ import annotations

from etlantic.testing import run_conformance_suite
from etlantic_echo import create_plugin


def test_echo_dataframe_conformance() -> None:
    rows = [{"customer_id": 1, "name": "Ada"}]
    run_conformance_suite(create_plugin(), engine="echo", sample_rows=rows)


def test_echo_empty_roundtrip() -> None:
    run_conformance_suite(create_plugin(), engine="echo", sample_rows=[])
