"""diligram-ocr-vlm: document and ID-card parsing into a traceable representation.

The output contract is frozen in ``schema/doc.schema.json``; this package only
implements producers of that contract.
"""

from __future__ import annotations

from .pipeline import SCHEMA_VERSION, parse_document, validate_document

__all__ = ["SCHEMA_VERSION", "parse_document", "validate_document"]
__version__ = "0.1.0"
