from prompts import get_prompt
from skills.web_search import get_search_prompt, get_skill_prompt


def test_get_prompt_returns_english_for_english_topic():
    prompt = get_prompt("EXPERT_ROUND1", "How should we design a cache invalidation strategy?")
    assert "independently state your initial views" in prompt
    assert "你是圆桌会议" not in prompt


def test_get_prompt_returns_chinese_for_chinese_topic():
    prompt = get_prompt("EXPERT_ROUND1", "如何设计缓存失效策略？")
    assert "你是圆桌会议中的一位专家" in prompt


def test_get_prompt_defaults_to_english_for_empty_topic():
    prompt = get_prompt("MODERATOR_OPENING")
    assert "arbiter and host" in prompt


def test_get_prompt_keeps_json_format_placeholders():
    en = get_prompt("EXPERT_ROUND2", "Test topic")
    zh = get_prompt("EXPERT_ROUND2", "测试议题")
    for text in (en, zh):
        assert '"target_agent"' in text
        assert "{round1_summary}" in text


def test_search_prompts_are_bilingual():
    assert "搜索提醒" in get_search_prompt("DUPLICATE", "测试议题")
    assert "Search reminder" in get_search_prompt("DUPLICATE", "Test topic")


def test_skill_prompt_is_bilingual():
    assert "可用技能" in get_skill_prompt("测试议题")
    assert "Available skill" in get_skill_prompt("Test topic")

