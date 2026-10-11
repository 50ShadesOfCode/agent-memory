"""M1 — truth store and the file-boundary rules."""

import pytest
from agent_memory.core import frontmatter
from agent_memory.core import record as record_module
from agent_memory.core.archive import Archive
from agent_memory.core.errors import ValidationError
from agent_memory.core.record import STATUS_INVALID, MemoryRecord
from agent_memory.core.slug import is_valid_slug, slugify

DESTRUCTIVE_NAMES = ("delete", "remove", "purge", "unlink", "drop", "erase")


def test_init_creates_the_schema_set_and_the_archive_buckets(store):
    assert store.layout.schemas_dir.is_dir()
    assert store.schemas.load()
    for bucket in (store.layout.provenance, store.layout.sessions):
        assert bucket.is_dir()
    assert store.layout.memory_index.exists()


def test_recorded_file_round_trips_through_frontmatter(store):
    store.record(type="fact", name="file-truth-invariant", abstract="Files are truth")
    written = store.record(
        abstract="Deploys run from the release branch only",
        type="procedure",
        body="# Steps\nCut a tag, then run the pipeline.\n",
        name="release-branch-only",
        links=["file-truth-invariant"],
    )
    text = written.path.read_text(encoding="utf-8")
    fields, body = frontmatter.parse(text)
    assert fields["name"] == written.name
    assert fields["abstract"] == written.abstract
    assert fields["links"] == ["file-truth-invariant"]
    assert "Cut a tag" in body


@pytest.mark.parametrize(
    ("field", "value", "expected_field"),
    [
        ("abstract", "", "abstract"),
        ("type", "nonsense", "type"),
        ("name", "Not A Slug", "name"),
    ],
)
def test_invalid_frontmatter_is_rejected_with_a_structured_error(
    store, field, value, expected_field
):
    kwargs = {
        "abstract": "A perfectly ordinary preference",
        "type": "preference",
        "name": "ordinary-preference",
    }
    kwargs[field] = value
    with pytest.raises(ValidationError) as raised:
        store.record(**kwargs)
    assert expected_field in {error.field for error in raised.value.errors}


def test_bad_date_is_rejected(store, config):
    bad = MemoryRecord(
        name="bad-date",
        abstract="has an unparseable date",
        type="fact",
        author="test",
        created="not-a-date",
        updated="2026-01-15",
    )
    with pytest.raises(ValidationError) as raised:
        record_module.validate(bad, config)
    assert "created" in {error.field for error in raised.value.errors}


def test_rewriting_the_same_name_is_an_update_not_a_second_file(store):
    first = store.record(abstract="Queue timeout is 30 seconds", type="fact", name="queue-timeout")
    second = store.record(abstract="Queue timeout is 60 seconds", type="fact", name="queue-timeout")
    assert first.path == second.path
    assert len([path for path in store.layout.truth_files() if path.stem == "queue-timeout"]) == 1
    assert second.created == first.created
    assert "60 seconds" in second.path.read_text(encoding="utf-8")


def test_superseded_record_leaves_the_active_set_but_stays_on_disk(seeded):
    seeded.record(
        abstract="The staging deploy no longer drains the queue at all",
        type="experience",
        name="staging-deploy-no-drain",
    )
    old = seeded.correct("staging-deploy-e4021", supersede_with="staging-deploy-no-drain")
    assert old.path.exists()
    active = {record.name for record in seeded.records() if record.is_active()}
    assert "staging-deploy-e4021" not in active
    assert "staging-deploy-no-drain" in active


def test_archive_module_exposes_no_destructive_interface():
    public = [name for name in dir(Archive) if not name.startswith("_")]
    assert not [name for name in public if any(word in name for word in DESTRUCTIVE_NAMES)]


def test_provenance_excerpt_is_stored_and_retrievable_by_name(store):
    excerpt = "user said: the drain window must exceed the lease TTL"
    written = store.record(
        abstract="Drain window must exceed lease TTL",
        type="fact",
        name="drain-window-rule",
        provenance=[excerpt],
    )
    stored = store.archive.provenance_of("drain-window-rule")
    assert stored
    assert excerpt in stored[0].read_text(encoding="utf-8")
    assert written.provenance


def test_delete_marks_invalid_in_place_without_losing_the_file(seeded):
    removed = seeded.delete("file-truth-invariant")
    assert removed.status == STATUS_INVALID
    assert removed.path.exists()
    assert removed.path.parent == seeded.find("file-truth-invariant").path.parent
    assert "file-truth-invariant" not in {record.name for record in seeded.records()}
    assert "file-truth-invariant" in {
        record.name for record in seeded.records(include_invalid=True)
    }


def test_slug_is_stable_and_links_survive_a_move_across_directories(seeded):
    seeded.record(
        abstract="Link target for the move test",
        type="fact",
        name="link-target",
    )
    seeded.record(
        abstract="Holds a link to the target",
        type="fact",
        name="link-holder",
        links=["link-target"],
    )
    moved = seeded.record(
        abstract="Link target for the move test",
        type="fact",
        name="link-target",
        fields={"project": "deploys"},
    )
    assert moved.path.parent.name == "deploys"
    assert moved.name == "link-target"
    report = seeded.sync_index()
    assert report.dangling_links == ()


def test_a_group_value_cannot_add_a_level_of_its_own(store):
    written = store.record(
        abstract="Tries to nest two levels through a slash",
        type="fact",
        name="not-too-deep",
        fields={"project": "a/b"},
    )
    assert len(written.path.relative_to(store.root).parts) == len(("fact", "group", "file"))


def test_slugify_is_idempotent_and_produces_valid_slugs(config):
    for text in ("Deploy fails: error E4021!", "  Mixed   Case __ names  ", "重构 pipeline v2"):
        once = slugify(text, config.storage.slug_max_length)
        if once:
            assert is_valid_slug(once)
            assert slugify(once, config.storage.slug_max_length) == once


def test_a_derived_name_names_the_cause_and_the_way_out(store):
    with pytest.raises(ValidationError) as raised:
        store.record(abstract="重构后的部署流程记录", type="fact")
    (error,) = raised.value.errors
    assert error.field == "name"
    assert "ASCII" in error.reason
    assert "name" in error.reason


def test_a_non_ascii_abstract_is_written_under_an_explicit_name(store):
    written = store.record(
        abstract="重构后的部署流程记录", type="fact", name="deploy-rewrite-notes"
    )
    assert written.name == "deploy-rewrite-notes"
    assert written.path.name == "deploy-rewrite-notes.md"


def test_a_group_that_slugs_to_nothing_names_the_cause(store):
    with pytest.raises(ValidationError) as raised:
        store.record(
            abstract="Prefers short answers",
            type="preference",
            name="short-answers",
            fields={"topic": "沟通"},
        )
    assert "topic" in {error.field for error in raised.value.errors}
    assert "ASCII" in " ".join(error.reason for error in raised.value.errors)


def test_find_rejects_a_parseable_but_invalid_file_loudly(store):
    rogue = store.layout.type_dir("fact") / "Not A Slug.md"
    rogue.parent.mkdir(parents=True, exist_ok=True)
    rogue.write_text(
        "---\nname: Not A Slug\nabstract: rogue\ntype: fact\nweight: 1.0\n---\nbody\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationError, match="slug"):
        store.find("Not A Slug")
    assert "Not A Slug" not in [record.name for record in store.records()]


def test_read_serializes_access_log_append(seeded, monkeypatch):
    import contextlib

    import agent_memory.core.store as store_module

    held = []
    real = store_module.store_lock

    @contextlib.contextmanager
    def recording(layout):
        held.append(True)
        with real(layout):
            yield

    monkeypatch.setattr(store_module, "store_lock", recording)

    seeded.read("file-truth-invariant", level="abstract")

    assert held == [True]


def test_move_preserves_identity_provenance_and_links(store):
    from agent_memory.core import schema as schema_module

    item = schema_module.MemorySchema(
        type="widget",
        description="A widget",
        key=("topic", "subject"),
        group="topic",
        mode="add_only",
    )
    store.schemas.path_for("widget").write_text(schema_module.render(item), encoding="utf-8")
    pointer = store.archive.append_session("chat", ["user: the widget hums"])
    from agent_memory.core.sessions import render_pointer

    assert pointer is not None
    store.record(
        abstract="Base note", type="fact", name="base-note", body="See the widget."
    )
    rec = store.record(
        type="widget",
        fields={"topic": "apple", "subject": "hum"},
        abstract="The widget hums",
        body="It hums.",
        links=["base-note"],
        provenance=[render_pointer(pointer)],
        name="widget-hum",
        create_group=True,
    )
    old_path = rec.path

    moved = store.move("widget-hum", "topic", "apples")

    assert moved.name == "widget-hum"
    assert moved.fields["topic"] == "apples"
    assert moved.abstract == rec.abstract and moved.body == rec.body
    assert moved.provenance == rec.provenance
    assert moved.links == ["base-note"]
    assert store.find("base-note") is not None
    assert old_path is not None and not old_path.exists()
    assert moved.path is not None and moved.path.is_file()
    assert store.find("widget-hum").fields["topic"] == "apples"
