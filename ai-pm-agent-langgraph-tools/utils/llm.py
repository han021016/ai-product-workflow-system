import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
MODEL_NAME = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash").strip()
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").strip().rstrip("/")


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.6) -> str:
    """Call DeepSeek using plain HTTP requests, avoiding OpenAI SDK/httpx version conflicts."""
    if not API_KEY:
        raise ValueError("DEEPSEEK_API_KEY is missing. Please add it to your .env file.")

    url = f"{BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "stream": False,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=120)
    except requests.exceptions.Timeout:
        raise RuntimeError("DeepSeek request timed out. Try a shorter input or run again.")
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Network/API request failed: {exc}")

    if resp.status_code >= 400:
        raise RuntimeError(f"DeepSeek API error {resp.status_code}: {resp.text}")

    data = resp.json()
    return data["choices"][0]["message"]["content"]
