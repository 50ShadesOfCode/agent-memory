"""OpenCode capture plugin: node suite green, hook entry never blocks."""

from __future__ import annotations

import io
import json
import os
import pathlib
import subprocess
import sys

from agent_memory.adapters import hook_entry
from agent_memory.core.recall import Recall
from agent_memory.core.store import Store

PLUGIN_DIR = pathlib.Path(__file__).resolve().parents[2] / "plugins" / "opencode"


def _mem(*args, store, input=None):
    env = {**os.environ, "AGENT_MEMORY_STORE": str(store)}
    return subprocess.run(
        ["uv", "run", *args],
        input=input,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
        env=env,
    )


def _archive_text(store):
    return "".join(
        path.read_text(encoding="utf-8")
        for path in (store / "archive").rglob("*")
        if path.is_file()
    )


def test_kill_drill_archive_survives_and_dedupes(tmp_path):
    store = tmp_path / "store"
    assert _mem("mem", "init", store=store).returncode == 0
    hook = ["mem-hook", "--host", "opencode"]
    first = {"session_id": "s1", "event": "tool", "items": ["user: hello", "assistant: hi"]}
    grown = {
        "session_id": "s1",
        "event": "timer",
        "items": ["user: hello", "assistant: hi", "user: again"],
    }

    assert _mem(*hook, store=store, input=json.dumps(first)).returncode == 0
    # "kill": the next pipe is a brand-new process lifetime.
    assert _mem(*hook, store=store, input=json.dumps(first)).returncode == 0
    assert _mem(*hook, store=store, input=json.dumps(grown)).returncode == 0

    archived = _archive_text(store)
    assert archived.count('"text": "hello"') == 1
    assert '"text": "hi"' in archived
    assert '"text": "again"' in archived


def test_opencode_written_memory_recalled_by_plain_core(tmp_path):
    store = tmp_path / "store"
    assert _mem("mem", "init", store=store).returncode == 0
    assert (
        _mem(
            "mem",
            "record",
            "--type",
            "decision",
            "--field",
            "project=opencode",
            "--name",
            "via-opencode",
            "--abstract",
            "OpenCode writes through the same core",
            "--body",
            "Adapters carry zero algorithm.",
            store=store,
        ).returncode
        == 0
    )

    assert "via-opencode" in [hit.name for hit in Recall(Store(store)).recall("same core")]



def test_plugin_node_suite_passes():
    assert PLUGIN_DIR.is_dir(), "plugins/opencode not implemented yet"
    completed = subprocess.run(
        ["node", "--test", "src/"],
        cwd=PLUGIN_DIR,
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_hook_entry_never_fails_loudly(tmp_path, monkeypatch, capsys):
    def _boom(store, event):
        raise RuntimeError("distillation exploded")

    monkeypatch.setattr(hook_entry, "handle", _boom)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"event": "tool"})))

    code = hook_entry.main(["--host", "opencode", "--store", str(tmp_path / "store")])

    assert code == hook_entry.EXIT_OK
    assert capsys.readouterr().out == ""
    assert (tmp_path / "store" / ".state" / hook_entry.LOG_FILENAME).is_file()
