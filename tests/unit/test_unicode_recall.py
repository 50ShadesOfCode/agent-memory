"""Non-Latin queries must reach the FTS index, not vanish silently."""

from agent_memory.core import search_index
from agent_memory.core.recall import Recall


def test_to_match_query_keeps_cjk_and_arabic_tokens():
    expression = search_index.to_match_query("中文 اختبار hello")

    assert '"中文"*' in expression
    assert '"اختبار"*' in expression
    assert '"hello"' in expression and '"hello"*' not in expression


def test_cjk_query_retrieves_cjk_record(store):
    store.record(
        abstract="中文记忆测试",
        type="fact",
        body="索引可重建",
        name="zhongwen-ji-yi",
    )

    hits = Recall(store).recall("中文记忆")

    assert "zhongwen-ji-yi" in [hit.name for hit in hits]
