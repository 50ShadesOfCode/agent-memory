"""OpenCode host: plugin triggers are a dialect, not a branch."""

import json
import stat

import pytest
from agent_memory.adapters import doctor, moments, setup
from agent_memory.core.errors import ValidationError
from agent_memory.core.store import Store


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

