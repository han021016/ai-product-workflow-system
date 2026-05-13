from typing import TypedDict, Dict, Any


class ProductManagerState(TypedDict, total=False):
    product_idea: str
    target_users: str
    platform: str
    competitors: str
    tool_outputs: Dict[str, str]
    results: Dict[str, str]
    current_step: str
