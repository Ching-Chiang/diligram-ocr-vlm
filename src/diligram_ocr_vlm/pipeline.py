"""Parsing entry points.

v0.1 fixes the interface and the output contract; engine wiring is not done yet.
``parse_document`` raises ``NotImplementedError`` on purpose so that callers fail
loudly instead of receiving a half-parsed document.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

SCHEMA_VERSION = "0.1"

_SCHEMA_PATH = Path(__file__).resolve().parents[2] / "schema" / "doc.schema.json"


def load_schema() -> dict[str, Any]:
    """Load the authoritative contract shipped with the repository."""
    return json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_document(doc: Mapping[str, Any]) -> None:
    """Validate a parsed document against the contract.

    Raises:
        jsonschema.ValidationError: if ``doc`` violates the contract.
    """
    import jsonschema

    jsonschema.validate(dict(doc), load_schema())


def parse_document(
    path: str | Path,
    *,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Parse one file into a contract-conforming document dict.

    Args:
        path: PDF or image to parse.
        config: Optional overrides for layout/OCR/VLM engines.

    Returns:
        A dict conforming to ``schema/doc.schema.json``.

    Raises:
        NotImplementedError: always, until the pipelines land in v0.2.
    """
    raise NotImplementedError(
        "engine wiring lands in v0.2; the output contract is already frozen in "
        "schema/doc.schema.json"
    )
