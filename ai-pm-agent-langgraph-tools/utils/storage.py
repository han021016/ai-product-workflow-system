import json
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "history.json")


def load_history():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_record(product_idea, target_users, platform, competitors, results, tool_outputs=None):
    os.makedirs("data", exist_ok=True)
    history = load_history()
    record = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "product_idea": product_idea,
        "target_users": target_users,
        "platform": platform,
        "competitors": competitors,
        "results": results,
        "tool_outputs": tool_outputs or {},
    }
    history.insert(0, record)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return record


def delete_record(record_id):
    history = load_history()
    history = [r for r in history if r.get("id") != record_id]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
