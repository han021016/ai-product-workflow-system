from graph.workflow import run_langgraph_product_manager_workflow


def run_product_manager_workflow(product_idea, target_users, platform, competitors, progress_callback=None):
    results, _tool_outputs = run_langgraph_product_manager_workflow(
        product_idea, target_users, platform, competitors, progress_callback
    )
    return results
