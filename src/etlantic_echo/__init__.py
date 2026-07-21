"""Minimal in-memory ``echo`` dataframe plugin for ETLantic protocol ``/1``.

This package is the out-of-monorepo reference plugin for the 0.22 Plugin SDK.
It uses only public ETLantic APIs and is tested solely via
``etlantic.testing`` plus ``etlantic plugin compatibility``.
"""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from typing import Any

from etlantic.capabilities import PluginCapabilities
from etlantic.dataframe.protocol import (
    DATAFRAME_PROTOCOL_VERSION,
    ArtifactOwnership,
    DataframeExecutionContext,
    DataframeOutputBundle,
    DataframePluginInfo,
    ValidationDecision,
)

__version__ = "0.22.0"

__all__ = ["EchoDataframePlugin", "__version__", "create_plugin"]


def create_plugin() -> EchoDataframePlugin:
    """Entry-point factory for ``etlantic.dataframe_plugins``."""
    return EchoDataframePlugin()


def _as_records(value: Any, *, contract_type: type[Any] | None) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, list):
        rows: list[dict[str, Any]] = []
        for item in value:
            if hasattr(item, "model_dump"):
                rows.append(dict(item.model_dump()))
            elif isinstance(item, Mapping):
                rows.append(dict(item))
            else:
                rows.append({"value": item})
        return rows
    if hasattr(value, "model_dump"):
        return [dict(value.model_dump())]
    if isinstance(value, Mapping):
        return [dict(value)]
    raise TypeError(f"echo plugin cannot materialize {type(value)!r}")


class EchoDataframePlugin:
    """Tiny list-of-dicts engine named ``echo`` (no optional dependencies)."""

    def __init__(self) -> None:
        self._info = DataframePluginInfo(
            name="etlantic-plugin-echo",
            engine="echo",
            version=__version__,
            protocol_version=DATAFRAME_PROTOCOL_VERSION,
            capabilities=PluginCapabilities(
                engine="echo",
                dataframe=True,
                eager=True,
                lazy=False,
                schema_inspection=True,
                invalid_row_separation=False,
            ),
        )

    @property
    def info(self) -> DataframePluginInfo:
        return self._info

    def materialize_input(
        self,
        value: Any,
        *,
        contract_type: type[Any] | None,
        context: DataframeExecutionContext,
        port_name: str,
    ) -> list[dict[str, Any]]:
        return _as_records(value, contract_type=contract_type)

    def invoke(
        self,
        *,
        callable_: Any,
        inputs: Mapping[str, Any],
        parameters: Mapping[str, Any],
        context: DataframeExecutionContext,
    ) -> Any:
        return callable_(**dict(inputs), **dict(parameters))

    def normalize_output(
        self,
        result: Any,
        *,
        output_ports: tuple[str, ...],
        context: DataframeExecutionContext,
    ) -> DataframeOutputBundle:
        port = output_ports[0] if output_ports else "result"
        records = _as_records(result, contract_type=None)
        return DataframeOutputBundle(valid={port: records})

    def validate_frame(
        self,
        value: Any,
        *,
        contract_type: type[Any] | None,
        context: DataframeExecutionContext,
        boundary: str,
        port_name: str | None = None,
    ) -> tuple[Any, ValidationDecision, list[dict[str, Any]], Any | None]:
        if contract_type is None:
            return value, ValidationDecision.SKIPPED, [], None
        records = _as_records(value, contract_type=contract_type)
        validated: list[Any] = []
        for row in records:
            validated.append(contract_type.model_validate(row))
        return validated, ValidationDecision.PASSED, [], None

    def inspect_schema(self, value: Any, *, identity: str) -> dict[str, Any] | None:
        records = _as_records(value, contract_type=None)
        fields: list[dict[str, Any]] = []
        if records:
            for key, sample in records[0].items():
                fields.append(
                    {
                        "name": str(key),
                        "logical_type": type(sample).__name__,
                    }
                )
        return {"identity": identity, "fields": fields, "engine": "echo"}

    def ensure_ownership(
        self,
        value: Any,
        *,
        ownership: ArtifactOwnership,
        context: DataframeExecutionContext,
    ) -> Any:
        if ownership is ArtifactOwnership.COPIED:
            return deepcopy(value)
        return value

    def collect_if_needed(
        self,
        value: Any,
        *,
        context: DataframeExecutionContext,
    ) -> Any:
        return value

    def to_records(
        self,
        value: Any,
        *,
        contract_type: type[Any] | None = None,
    ) -> list[Any]:
        records = _as_records(value, contract_type=contract_type)
        if contract_type is None:
            return records
        return [contract_type.model_validate(row) for row in records]

    def row_count(self, value: Any) -> int:
        return len(_as_records(value, contract_type=None))
