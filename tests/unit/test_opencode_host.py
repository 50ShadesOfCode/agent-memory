"""OpenCode host: plugin triggers are a dialect, not a branch."""

import json
import pathlib
import stat

import pytest
from agent_memory.adapters import doctor, moments, setup
from agent_memory.core.errors import ValidationError
from agent_memory.core.store import Store
from agent_memory.executor import hosts


@pytest.fixture(autouse=True)
def _stub_live_host_reasoner(monkeypatch):
    """No host process is launched by setup fixtures."""
    monkeypatch.setattr(
        doctor,
        "_live_reasoner_check",
        lambda _store, _host: doctor.Check(
            "REASONER_LIVE_OK", True, "fixture host reasoner completed"
        ),
    )


def test_prompt_admission_is_the_inject_moment():
    assert moments.moment_for("opencode", "prompt") == moments.MOMENT_INJECT


def test_compaction_is_the_evict_moment():
    assert moments.moment_for("opencode", "compaction") == moments.MOMENT_EVICT


def test_tool_and_timer_captures_are_pause_moments():
    assert moments.moment_for("opencode", "tool") == moments.MOMENT_PAUSE
    assert moments.moment_for("opencode", "timer") == moments.MOMENT_PAUSE


def test_install_registers_plugin_entry_and_preserves_existing(tmp_path):
    settings = tmp_path / "opencode.json"
    settings.write_text(
        json.dumps({"model": "keep-me", "plugins": ["other-plugin"]}), encoding="utf-8"
    )
    store_root = tmp_path / "store"

    target = setup.install("opencode", settings, store_root)

    parsed = json.loads(target.read_text(encoding="utf-8"))
    assert parsed["model"] == "keep-me"
    assert "other-plugin" in parsed["plugins"]
    managed = [entry for entry in parsed["plugins"] if setup.HOOK_COMMAND in json.dumps(entry)]
    assert len(managed) == 1
    rendered = json.dumps(managed[0])
    assert "--host opencode" in rendered
    assert str(store_root.resolve()) in rendered


def test_capture_period_defaults_to_ten_minutes_and_roundtrips(tmp_path):
    from agent_memory.core.config import Config

    assert Config.default().write.capture_period_seconds == 600.0
    config = Config.default()
    config.write.capture_period_seconds = 60.0
    config.save(tmp_path)

    assert Config.load(tmp_path).write.capture_period_seconds == 60.0


def test_install_projects_capture_period_into_plugin_options(tmp_path):
    from agent_memory.core.config import Config

    store = Store(tmp_path / "store")
    store.init()
    config = Config.load(store.root)
    config.write.capture_period_seconds = 60.0
    config.save(store.root)

    target = setup.install("opencode", tmp_path / "opencode.json", store.root)

    parsed = json.loads(target.read_text(encoding="utf-8"))
    managed = [entry for entry in parsed["plugins"] if setup._is_managed(entry)]
    assert managed[0]["options"]["periodMs"] == 60000


def test_install_replaces_only_its_own_entry(tmp_path):
    settings = tmp_path / "opencode.json"
    settings.write_text(
        json.dumps({"plugins": ["mem-hook-mentioning-impostor", "other-plugin"]}),
        encoding="utf-8",
    )

    target = setup.install("opencode", settings, tmp_path / "store")

    parsed = json.loads(target.read_text(encoding="utf-8"))
    assert "mem-hook-mentioning-impostor" in parsed["plugins"]
    assert "other-plugin" in parsed["plugins"]
    managed = [entry for entry in parsed["plugins"] if setup._is_managed(entry)]
    assert len(managed) == 1
    assert managed[0]["options"]["distillTitle"] == "agent-memory-distill"


def test_install_without_plugin_directory_fails_closed(tmp_path, monkeypatch):
    settings = tmp_path / "opencode.json"
    real_is_dir = pathlib.Path.is_dir
    monkeypatch.setattr(
        pathlib.Path,
        "is_dir",
        lambda self: False if self.name == "opencode" else real_is_dir(self),
    )

    with pytest.raises(ValidationError, match="plugin"):
        setup.install("opencode", settings, tmp_path / "store")


def test_install_without_store_root_fails_naming_the_store(tmp_path):
    settings = tmp_path / "opencode.json"
    with pytest.raises(ValidationError, match="store"):
        setup.install("opencode", settings, None)


def _fake_opencode(path):
    binary = path / "opencode"
    binary.write_text('#!/usr/bin/env bash\necho "opencode v2.0.26"\n', encoding="utf-8")
    binary.chmod(binary.stat().st_mode | stat.S_IEXEC)
    return binary


def test_doctor_reports_missing_opencode_binary(tmp_path, monkeypatch):
    monkeypatch.setenv("PATH", str(tmp_path))
    store = Store(tmp_path / "store")
    store.init()

    report = doctor.run(store, "opencode", settings_path=tmp_path / "opencode.json", live=False)

    assert report.status == doctor.FAILED
    missing = [check for check in report.checks if check.code == "HOST_BINARY_MISSING"]
    assert len(missing) == 1
    assert "opencode" in missing[0].detail


def test_doctor_ready_with_binary_settings_and_plugin(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _fake_opencode(bin_dir)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    store = Store(tmp_path / "store")
    store.init()
    target = setup.install("opencode", tmp_path / "opencode.json", store.root)

    report = doctor.run(store, "opencode", settings_path=target, live=True)

    assert report.status == doctor.READY
    assert any(check.code == "HOOK_OK" for check in report.checks)



def _espec():
    return hosts.HostSpec(name="opencode", binary="opencode", model="m")


def test_opencode_empty_answer_fails_like_codex_and_muse(tmp_path, monkeypatch):
    import subprocess

    from agent_memory.executor.hosts import Host

    spec = hosts.HostSpec(
        name="opencode", binary="opencode", model="m", attempts=1, retry_backoff_seconds=0
    )
    completed = type("Completed", (), {"returncode": 0, "stdout": "", "stderr": ""})()
    monkeypatch.setattr(subprocess, "run", lambda *args, **kwargs: completed)

    result = Host(spec).run("hi", store_root=None)

    assert not result.ok


def test_opencode_routes_through_headless_run_with_json_output(tmp_path):
    command = hosts.DIALECTS["opencode"].command(
        _espec(),
        tools_enabled=False,
        system_prompt="keeper",
        max_turns=7,
        store_root=None,
        answer_file=tmp_path / "a.txt",
    )

    assert command[:2] == ["opencode", "run"]
    assert "--format" in command and "json" in command
    assert "--title" in command and "agent-memory-distill" in command


def test_opencode_answer_keeps_only_the_last_message(tmp_path):
    stdout = "\n".join(
        [
            '{"type":"text","part":{"type":"text","text":"stale ","messageID":"m1"}}',
            '{"type":"text","part":{"type":"text","text":"final","messageID":"m2"}}',
        ]
    )

    assert hosts.DIALECTS["opencode"].answer(stdout, tmp_path / "a.txt") == "final"


def test_opencode_answer_joins_split_text_of_one_message(tmp_path):
    stdout = "\n".join(
        [
            '{"type":"text","part":{"type":"text","text":"AGENT_","messageID":"m1"}}',
            '{"type":"text","part":{"type":"text","text":"MEMORY_READY","messageID":"m1"}}',
        ]
    )

    assert hosts.DIALECTS["opencode"].answer(stdout, tmp_path / "a.txt") == "AGENT_MEMORY_READY"
