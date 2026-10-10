"""OpenCode capture plugin: node suite green, hook entry never blocks."""

from __future__ import annotations

import io
import json
import pathlib
import subprocess
import sys

from agent_memory.adapters import hook_entry

PLUGIN_DIR = pathlib.Path(__file__).resolve().parents[2] / "plugins" / "opencode"


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
