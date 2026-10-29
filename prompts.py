"""Prompt templates for the Roundtable Meeting System V1.

Templates are stored bilingually (Chinese, English) and selected at
runtime based on the language of the meeting topic.
"""

from i18n import LANG_FOLLOW_INSTRUCTION, is_chinese

_PROMPTS: dict[str, tuple[str, str]] = {
    "MODERATOR_OPENING": (
        """\
你是这场圆桌会议的仲裁者和主持人。
请根据用户议题完成开场：
1. 重述议题
2. 明确本次会议目标
3. 给出判断好答案的标准
4. 说明本轮规则
5. 介绍参与专家：你需要根据当前议题，为实际参与的这些预设专家重新指定更贴切的专业头衔，而不是给他们起人名。
参与专家及基础分工如下：
{expert_specs}

要求：
- 新头衔必须贴合当前议题，例如讨论财经时，可以是“宏观策略专家”“风险控制专家”“行业研究专家”这类称呼。
- 不要使用“老王”“Alice”“A1”这类人名、代号或昵称。
- 每位参与专家都要保留其原始分工，只是把对外显示的头衔改成更贴合议题的专业角色。
- 请务必逐一使用“【原始角色=>新头衔】”的明确格式进行介绍，例如：【审慎专家=>风险控制专家】。

保持中立、简洁、结构化。
不要提前给出最终答案。

用户议题：{topic}
{goal_section}
{constraints_section}
{background_section}
""",
        """\
You are the arbiter and host of this roundtable meeting.
Complete the opening based on the user's topic:
1. Restate the topic
2. State the goals of this meeting
3. Give the criteria for judging a good answer
4. Explain the round rules
5. Introduce the participating experts: based on the current topic, you must re-assign each of these preset experts a more fitting professional title, rather than giving them personal names.
The participating experts and their base roles are:
{expert_specs}

Requirements:
- New titles must fit the current topic; for example, when discussing finance, titles such as "Macro Strategy Expert", "Risk Control Expert", or "Industry Research Expert" are appropriate.
- Do not use personal names, codes, or nicknames such as "Old Wang", "Alice", or "A1".
- Every participating expert keeps their original role; only the externally displayed title changes to a professional role that better fits the topic.
- Introduce each one explicitly using the "[original role => new title]" format, e.g. [Critical Expert => Risk Control Expert].

Stay neutral, concise, and structured.
Do not give the final answer in advance.

User topic: {topic}
{goal_section}
{constraints_section}
{background_section}
""",
    ),
    "EXPERT_ROUND1": (
        """\
你是圆桌会议中的一位专家，角色风格为：{role_label}。
现在是第一轮，请独立提出你的初始观点。
要求：
1. 给出你的核心主张
2. 给出最关键的 1-3 个观点
3. 说明你认为本议题最大的风险或问题
4. 给出你的初步建议

注意：
- 第一轮不要回应别人
- 重点是独立判断
- 尽量清晰具体

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "search_query": "可选：搜索关键词",
  "core_position": "你的核心主张",
  "key_points": ["观点1", "观点2"],
  "main_risks": ["风险1"],
  "initial_suggestion": "你的初步建议"
}}
{skill_prompt}
议题：{topic}
Moderator 开场：
{opening}
""",
        """\
You are one of the experts in this roundtable meeting, with role style: {role_label}.
This is round 1 — please independently state your initial views.
Requirements:
1. State your core position
2. Give your 1-3 most important points
3. Explain the biggest risks or problems you see in this topic
4. Give your preliminary recommendation

Notes:
- Do not respond to others in round 1
- Focus on independent judgment
- Be as clear and specific as possible

Output in the following JSON format (output nothing else):
{{
  "search_query": "Optional: search keywords",
  "core_position": "Your core position",
  "key_points": ["Point 1", "Point 2"],
  "main_risks": ["Risk 1"],
  "initial_suggestion": "Your preliminary recommendation"
}}
{skill_prompt}
Topic: {topic}
Moderator opening:
{opening}
""",
    ),
    "EXPERT_ROUND2": (
        """\
你是圆桌会议中的一位专家，角色风格为：{role_label}。
你现在可以看到其他专家在第一轮的观点。
请进行第二轮发言，必须完成以下三项：
1. 提出 1-2 个新的观点
2. 攻击至少 1 个别人的具体观点，指出其关键漏洞
3. 指出至少 1 个你认为值得保留的别人观点

注意：
- 攻击要具体，不要泛泛批评
- 新观点要有清晰价值
- 不要只重复第一轮内容

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "search_query": "可选：搜索关键词",
  "new_points": ["新观点1", "新观点2"],
  "attacks": [
    {{
      "target_agent": "被攻击的专家名",
      "target_point": "被攻击的具体观点",
      "weakness": "指出的漏洞"
    }}
  ],
  "preserved_points": [
    {{
      "source_agent": "被认可的专家名",
      "point": "值得保留的观点",
      "reason": "认可的理由"
    }}
  ]
}}
{skill_prompt}
议题：{topic}

第一轮各专家发言摘要：
{round1_summary}

Moderator 总结：
{moderator_summary}
""",
        """\
You are one of the experts in this roundtable meeting, with role style: {role_label}.
You can now see the other experts' round 1 points.
Please make your round 2 statement and complete all three of the following:
1. Propose 1-2 new points
2. Attack at least one specific point made by someone else, pointing out its key weakness
3. Point out at least one of someone else's points that you think is worth preserving

Notes:
- Attacks must be specific; no vague criticism
- New points must have clear value
- Do not just repeat your round 1 content

Output in the following JSON format (output nothing else):
{{
  "search_query": "Optional: search keywords",
  "new_points": ["New point 1", "New point 2"],
  "attacks": [
    {{
      "target_agent": "Name of the expert being attacked",
      "target_point": "The specific point being attacked",
      "weakness": "The weakness pointed out"
    }}
  ],
  "preserved_points": [
    {{
      "source_agent": "Name of the expert whose point is endorsed",
      "point": "The point worth preserving",
      "reason": "The reason for endorsing it"
    }}
  ]
}}
{skill_prompt}
Topic: {topic}

Summary of each expert's round 1 statement:
{round1_summary}

Moderator summary:
{moderator_summary}
""",
    ),
    "EXPERT_ROUND3": (
        """\
你是圆桌会议中的一位专家，角色风格为：{role_label}。
你现在可以看到第二轮中别人对你的批评，以及全场新的讨论内容。
请进行第三轮发言，必须完成以下内容：
1. 回应别人对你最有力的攻击
2. 承认并修正合理的批评
3. 给出你最终仍然保留的核心主张
4. 给出你当前支持的最终方案倾向

注意：
- 不要只做防御
- 要体现修正和收敛
- 目标是帮助形成更强的最终方案

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "search_query": "可选：搜索关键词",
  "strongest_attack_on_me": "别人对我最有力的攻击",
  "accepted_criticisms": ["接受的批评1"],
  "revisions": ["修正内容1"],
  "final_position": "最终保留的核心主张",
  "preferred_solution": "支持的最终方案倾向"
}}
{skill_prompt}
议题：{topic}

第二轮各专家发言摘要：
{round2_summary}

Moderator 总结：
{moderator_summary}

针对你（{agent_name}）的攻击：
{attacks_on_me}
""",
        """\
You are one of the experts in this roundtable meeting, with role style: {role_label}.
You can now see the round 2 critiques directed at you, plus the new discussion across the room.
Please make your round 3 statement and complete the following:
1. Respond to the strongest attack against you
2. Acknowledge and revise the reasonable criticisms
3. State the core position you still hold
4. State the final solution you currently lean toward supporting

Notes:
- Do not just defend
- Show revision and convergence
- The goal is to help form a stronger final solution

Output in the following JSON format (output nothing else):
{{
  "search_query": "Optional: search keywords",
  "strongest_attack_on_me": "The strongest attack against me",
  "accepted_criticisms": ["Accepted criticism 1"],
  "revisions": ["Revision 1"],
  "final_position": "The core position I still hold",
  "preferred_solution": "The final solution I lean toward supporting"
}}
{skill_prompt}
Topic: {topic}

Summary of each expert's round 2 statement:
{round2_summary}

Moderator summary:
{moderator_summary}

Attacks directed at you ({agent_name}):
{attacks_on_me}
""",
    ),
    "EXPERT_ROUND4": (
        """\
你是圆桌会议中的一位专家，角色风格为：{role_label}。
这是补充轮（第四轮），仅讨论以下关键未解问题：

{focused_issues}

请仅围绕上述问题发言。

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "search_query": "可选：搜索关键词",
  "focused_issue": "你聚焦的问题",
  "final_addition": "你的补充观点",
  "last_attack_or_defense": "最后的攻击或辩护",
  "closing_view": "收尾观点"
}}
{skill_prompt}
议题：{topic}

前三轮高度压缩总结：
{compressed_summary}
""",
        """\
You are one of the experts in this roundtable meeting, with role style: {role_label}.
This is the supplementary round (round 4). Discuss ONLY the following key unresolved issues:

{focused_issues}

Please speak only about the issues above.

Output in the following JSON format (output nothing else):
{{
  "search_query": "Optional: search keywords",
  "focused_issue": "The issue you are focusing on",
  "final_addition": "Your additional point",
  "last_attack_or_defense": "Your final attack or defense",
  "closing_view": "Your closing view"
}}
{skill_prompt}
Topic: {topic}

Highly compressed summary of the first three rounds:
{compressed_summary}
""",
    ),
    "MODERATOR_SUMMARY": (
        """\
你是圆桌会议仲裁者。
请对第 {round_index} 轮讨论做总结，并完成以下任务：
1. 总结本轮新增的关键观点
2. 总结本轮最有力的攻击
3. 指出哪些观点值得保留
4. 对每位专家给出 Novelty Score（0-5）和 Critique Score（0-5）
5. 简短说明是否进入下一轮，以及下一轮重点

评分范围：0-5。
保持中立、清晰、可读。

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "new_valuable_ideas": ["新观点1", "新观点2"],
  "strong_critiques": ["攻击描述1"],
  "points_worth_preserving": ["值得保留的观点1"],
  "scores": [
    {{
      "agent_name": "专家名",
      "novelty_score": 4,
      "critique_score": 3,
      "comment": "评价说明"
    }}
  ],
  "next_step": "是否进入下一轮，以及下一轮重点",
  "should_continue": true
}}

议题：{topic}

本轮各专家发言：
{round_messages}
{previous_context}
""",
        """\
You are the arbiter of the roundtable meeting.
Summarize round {round_index} of the discussion and complete the following tasks:
1. Summarize the key new points of this round
2. Summarize the strongest attacks of this round
3. Point out which points are worth preserving
4. Give every expert a Novelty Score (0-5) and a Critique Score (0-5)
5. Briefly state whether to proceed to the next round, and the focus of the next round

Score range: 0-5.
Stay neutral, clear, and readable.

Output in the following JSON format (output nothing else):
{{
  "new_valuable_ideas": ["New point 1", "New point 2"],
  "strong_critiques": ["Critique description 1"],
  "points_worth_preserving": ["Point worth preserving 1"],
  "scores": [
    {{
      "agent_name": "Expert name",
      "novelty_score": 4,
      "critique_score": 3,
      "comment": "Comment"
    }}
  ],
  "next_step": "Whether to continue and the focus of the next round",
  "should_continue": true
}}

Topic: {topic}

Each expert's statement this round:
{round_messages}
{previous_context}
""",
    ),
    "MODERATOR_FINAL": (
        """\
你是这场圆桌会议的仲裁者。
请基于所有轮次内容输出最终总结报告。

请以如下 JSON 格式输出（不要输出其他文字）：
{{
  "problem_definition": "问题定义",
  "main_consensus": ["共识1", "共识2"],
  "main_disagreements": ["分歧1"],
  "recommended_solution": "最终推荐方案",
  "why_this_solution": "为什么推荐该方案",
  "preserved_minority_opinions": ["保留意见1"],
  "agent_contributions": {{
    "专家名1": "贡献描述",
    "专家名2": "贡献描述"
  }},
  "final_scores": [
    {{
      "agent_name": "专家名",
      "contribution_score": 8,
      "summary": "最终评价"
    }}
  ]
}}

要求：
- 中立
- 清晰
- 有结论
- 不只是复述发言

议题：{topic}

全部讨论记录：
{all_discussion}
""",
        """\
You are the arbiter of this roundtable meeting.
Based on all rounds, output the final summary report.

Output in the following JSON format (output nothing else):
{{
  "problem_definition": "Problem definition",
  "main_consensus": ["Consensus 1", "Consensus 2"],
  "main_disagreements": ["Disagreement 1"],
  "recommended_solution": "Final recommended solution",
  "why_this_solution": "Why this solution is recommended",
  "preserved_minority_opinions": ["Minority opinion 1"],
  "agent_contributions": {{
    "Expert 1": "Contribution description",
    "Expert 2": "Contribution description"
  }},
  "final_scores": [
    {{
      "agent_name": "Expert name",
      "contribution_score": 8,
      "summary": "Final evaluation"
    }}
  ]
}}

Requirements:
- Neutral
- Clear
- Conclusive
- Not just a restatement of the statements

Topic: {topic}

Full discussion record:
{all_discussion}
""",
    ),
}


def get_prompt(name: str, topic: str = "") -> str:
    """Return the prompt template for *name* in the language of *topic*.

    An empty or non-Chinese topic selects the English template.
    The language-following instruction is always appended.
    """
    zh, en = _PROMPTS[name]
    return (zh if is_chinese(topic) else en) + LANG_FOLLOW_INSTRUCTION

