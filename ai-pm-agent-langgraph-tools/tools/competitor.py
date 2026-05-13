from typing import List


def analyze_competitors(competitors: str, product_idea: str) -> str:
    """A lightweight competitor-analysis tool.

    It does not browse the web by default, so it is stable for interviews.
    It transforms user-provided competitor names into a structured analysis
    that downstream agents can use.
    """
    names: List[str] = [c.strip() for c in competitors.replace("，", ",").split(",") if c.strip()]
    if not names:
        return "用户未提供明确竞品。请基于产品创意推断间接竞品、替代方案和差异化机会。"

    lines = ["# Competitor Tool Output", "", f"产品创意：{product_idea}", "", "## 用户提供的竞品/参考"]
    for idx, name in enumerate(names, start=1):
        lines.append(f"{idx}. {name}")
    lines.extend([
        "",
        "## 建议分析维度",
        "- 核心定位：它主要解决什么问题？",
        "- 目标用户：它主要服务哪类用户？",
        "- 关键功能：用户最常使用的功能是什么？",
        "- 可能短板：用户在效率、价格、学习成本、自动化程度上的痛点是什么？",
        "- 差异化机会：本产品可以如何做得更专注、更自动化、更适合目标用户？",
    ])
    return "\n".join(lines)
