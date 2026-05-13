from typing import Dict
from utils.llm import call_llm
from tools.competitor import analyze_competitors
from tools.calculator import calculate_basic_metrics
from graph.state import ProductManagerState


def _base_context(state: ProductManagerState) -> str:
    tool_outputs = state.get("tool_outputs", {})
    results = state.get("results", {})
    previous = "\n\n".join([f"## {k}\n{v[:1800]}" for k, v in results.items()])
    tools = "\n\n".join([f"## {k}\n{v}" for k, v in tool_outputs.items()])
    return f"""
产品创意：{state.get('product_idea', '')}
目标用户：{state.get('target_users', '')}
平台：{state.get('platform', '')}
竞品/参考：{state.get('competitors', '')}

工具输出：
{tools if tools else '暂无'}

前面 Agent 输出：
{previous if previous else '暂无'}
""".strip()


def _save_result(state: ProductManagerState, name: str, content: str) -> ProductManagerState:
    results: Dict[str, str] = dict(state.get("results", {}))
    results[name] = content
    state["results"] = results
    state["current_step"] = name
    return state


def tool_node(state: ProductManagerState) -> ProductManagerState:
    state["tool_outputs"] = {
        "Competitor Analysis Tool": analyze_competitors(state.get("competitors", ""), state.get("product_idea", "")),
        "Metrics Calculator Tool": calculate_basic_metrics(state.get("target_users", "")),
    }
    state["current_step"] = "Tool Node"
    return state


def idea_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 Idea Agent，资深产品策略专家。你的任务是先判断产品方向是否成立。只输出中文 Markdown。包含：一句话定位、目标问题、核心用户场景、价值主张、差异化机会、MVP 功能建议。"""
    content = call_llm(system, _base_context(state), temperature=0.4)
    return _save_result(state, "Idea Agent", content)


def persona_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 Persona Agent，用户研究专家。你必须基于 Idea Agent 的输出生成 2-3 个真实感用户画像。只输出中文 Markdown。包含：背景、目标、痛点、行为习惯、触发场景、反对理由、成功体验。"""
    content = call_llm(system, _base_context(state), temperature=0.5)
    return _save_result(state, "Persona Agent", content)


def prd_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 PRD Agent，高级产品经理。你必须基于 Idea Agent、Persona Agent 和竞品工具输出生成 PRD。只输出中文 Markdown。包含：背景、目标、用户流程、功能需求、非功能需求、MVP 范围、验收标准、边界条件。"""
    content = call_llm(system, _base_context(state), temperature=0.35)
    return _save_result(state, "PRD Agent", content)


def user_story_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 User Story Agent，敏捷产品负责人。你必须基于 PRD 拆解用户故事。只输出中文 Markdown 表格，列包括：Epic、User Story、优先级、验收标准、依赖。"""
    content = call_llm(system, _base_context(state), temperature=0.35)
    return _save_result(state, "User Story Agent", content)


def roadmap_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 Roadmap Agent，产品规划负责人。你必须基于 PRD 和 User Stories 规划版本路线图。只输出中文 Markdown。包含：MVP、V1、V2、未来版本；每阶段写目标、功能、时间估算、关键风险。"""
    content = call_llm(system, _base_context(state), temperature=0.4)
    return _save_result(state, "Roadmap Agent", content)


def metrics_agent(state: ProductManagerState) -> ProductManagerState:
    system = """你是 Metrics Agent，增长产品经理。你必须基于前面所有 Agent 输出和指标工具输出，设计指标体系。只输出中文 Markdown。包含：北极星指标、激活指标、留存指标、转化指标、风险、缓解策略、A/B 测试方案。"""
    content = call_llm(system, _base_context(state), temperature=0.35)
    return _save_result(state, "Metrics Agent", content)
