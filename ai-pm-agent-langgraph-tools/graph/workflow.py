from langgraph.graph import StateGraph, END
from graph.state import ProductManagerState
from graph.nodes import (
    tool_node,
    idea_agent,
    persona_agent,
    prd_agent,
    user_story_agent,
    roadmap_agent,
    metrics_agent,
)


def build_product_manager_graph():
    graph = StateGraph(ProductManagerState)

    graph.add_node("tools", tool_node)
    graph.add_node("idea", idea_agent)
    graph.add_node("persona", persona_agent)
    graph.add_node("prd", prd_agent)
    graph.add_node("stories", user_story_agent)
    graph.add_node("roadmap", roadmap_agent)
    graph.add_node("metrics", metrics_agent)

    graph.set_entry_point("tools")
    graph.add_edge("tools", "idea")
    graph.add_edge("idea", "persona")
    graph.add_edge("persona", "prd")
    graph.add_edge("prd", "stories")
    graph.add_edge("stories", "roadmap")
    graph.add_edge("roadmap", "metrics")
    graph.add_edge("metrics", END)

    return graph.compile()


def run_langgraph_product_manager_workflow(product_idea, target_users, platform, competitors, progress_callback=None):
    app = build_product_manager_graph()
    initial_state = {
        "product_idea": product_idea,
        "target_users": target_users,
        "platform": platform,
        "competitors": competitors,
        "tool_outputs": {},
        "results": {},
        "current_step": "start",
    }

    step_names = {
        "tools": "Tool Node：竞品分析 + 指标公式",
        "idea": "Idea Agent",
        "persona": "Persona Agent",
        "prd": "PRD Agent",
        "stories": "User Story Agent",
        "roadmap": "Roadmap Agent",
        "metrics": "Metrics Agent",
    }
    total = len(step_names)
    final_state = initial_state

    for i, chunk in enumerate(app.stream(initial_state), start=1):
        node_name = list(chunk.keys())[0]
        final_state = chunk[node_name]
        if progress_callback:
            progress_callback(min(i, total), total, step_names.get(node_name, node_name))

    return final_state.get("results", {}), final_state.get("tool_outputs", {})
