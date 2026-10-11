"""Frontmatter dialect: parse and render round-trip, including inline arrays."""

import pathlib

import pytest
from agent_memory.core import frontmatter
from agent_memory.core.errors import ValidationError
from agent_memory.core.record import MemoryRecord


def _round_trip(fields, body):
    text = frontmatter.render(fields, body)
    parsed_fields, parsed_body = frontmatter.parse(text)
    return parsed_fields, parsed_body


def test_parse_returns_empty_dict_when_no_frontmatter():
    fields, body = frontmatter.parse("just body text\n")
    assert fields == {}
    assert body == "just body text\n"


def test_parse_round_trip_preserves_scalar_fields():
    fields = {"name": "test-entry", "status": "active", "weight": 1.5}
    parsed, _ = _round_trip(fields, "body content")
    assert parsed["name"] == "test-entry"
    assert parsed["status"] == "active"
    assert parsed["weight"] == 1.5


def test_inline_array_of_quoted_strings_round_trips():
    fields = {"links": ["slug-one", "slug-two"]}
    parsed, _ = _round_trip(fields, "body")
    assert parsed["links"] == ["slug-one", "slug-two"]


def test_inline_array_with_unquoted_value_containing_apostrophe():
    """An unquoted value with a quote character mid-value must not enter quote mode.

    Before the fix, the apostrophe in 'it's' toggled quote tracking on,
    which prevented the comma from splitting the next item correctly.
    """
    text = "---\nlinks: [it's, done]\n---\nbody\n"
    fields, body = frontmatter.parse(text)
    assert fields["links"] == ["it's", "done"]


def test_inline_array_with_quoted_value_containing_other_quote_type():
    """A double-quoted value containing a single quote must round-trip."""
    text = '---\nlinks: ["it\'s done", "hello"]\n---\nbody\n'
    fields, body = frontmatter.parse(text)
    assert fields["links"] == ["it's done", "hello"]


def test_inline_array_single_unquoted_value_with_apostrophe():
    text = "---\ntags: [it's]\n---\nbody\n"
    fields, body = frontmatter.parse(text)
    assert fields["tags"] == ["it's"]


def test_empty_inline_array():
    fields = {"links": []}
    parsed, _ = _round_trip(fields, "body")
    assert parsed["links"] == []


def test_render_wraps_strings_needing_quoting():
    rendered = frontmatter._render_scalar("hello: world")
    assert rendered == '"hello: world"'


def test_render_scalar_boolean_and_null():
    assert frontmatter._render_scalar(True) == "true"
    assert frontmatter._render_scalar(False) == "false"
    assert frontmatter._render_scalar(None) == "null"


def test_split_document_with_no_closing_delimiter_returns_none_header():
    header, body = frontmatter.split_document("---\nname: test\nno closing marker\n")
    assert header is None


def test_parse_rejects_colon_less_line():

    with pytest.raises(ValidationError, match="frontmatter"):
        frontmatter.parse("---\nname: x\nthis line has no colon\n---\nbody\n")


def test_parse_rejects_duplicate_key():

    with pytest.raises(ValidationError, match="frontmatter"):
        frontmatter.parse("---\nname: x\nname: y\n---\nbody\n")


def test_from_text_rejects_garbage_weight():
    text = "---\nname: x\nabstract: y\ntype: decision\nweight: heavy\n---\nbody\n"
    with pytest.raises(ValidationError, match="weight"):
        MemoryRecord.from_text(text, pathlib.Path("x.md"))


def test_from_text_rejects_list_valued_custom_field():
    text = "---\nname: x\nabstract: y\ntype: decision\nproject:\n- a\n- b\n---\nbody\n"
    with pytest.raises(ValidationError, match="project"):
        MemoryRecord.from_text(text, pathlib.Path("x.md"))
