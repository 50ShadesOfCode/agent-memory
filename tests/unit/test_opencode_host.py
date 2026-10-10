"""OpenCode host: plugin triggers are a dialect, not a branch."""

from agent_memory.adapters import moments


def test_prompt_admission_is_the_inject_moment():
    assert moments.moment_for("opencode", "prompt") == moments.MOMENT_INJECT


def test_compaction_is_the_evict_moment():
    assert moments.moment_for("opencode", "compaction") == moments.MOMENT_EVICT


def test_tool_and_timer_captures_are_pause_moments():
    assert moments.moment_for("opencode", "tool") == moments.MOMENT_PAUSE
    assert moments.moment_for("opencode", "timer") == moments.MOMENT_PAUSE
