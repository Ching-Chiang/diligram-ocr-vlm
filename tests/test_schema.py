import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema" / "doc.schema.json").read_text(encoding="utf-8"))
EXAMPLES = sorted((ROOT / "examples").glob("*.doc.json"))


def test_schema_declares_version():
    assert SCHEMA["properties"]["schema_version"]["const"] == "0.1"


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_conform_to_schema(path):
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(json.loads(path.read_text(encoding="utf-8")), SCHEMA)


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_examples_keep_consumer_invariants(path):
    doc = json.loads(path.read_text(encoding="utf-8"))

    page_nos = [p["page_no"] for p in doc["pages"]]
    assert page_nos == list(range(1, len(page_nos) + 1)), "pages must be 1..n ascending"

    for page in doc["pages"]:
        seen = set()
        for block in page["blocks"]:
            assert block["block_id"] not in seen, f"duplicate block_id {block['block_id']}"
            seen.add(block["block_id"])
            if "bbox" in block:
                x0, y0, x1, y1 = block["bbox"]
                assert x0 < x1 and y0 < y1, "bbox must be a non-empty box"
