import os
from datetime import datetime
import markdown


def build_markdown(product_idea, target_users, platform, competitors, results):
    parts = [
        "# AI 产品经理 Agent 报告",
        f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## 输入信息",
        f"- 产品创意：{product_idea}",
        f"- 目标用户：{target_users}",
        f"- 平台：{platform}",
        f"- 竞品/参考：{competitors}",
        "",
    ]
    for name, content in results.items():
        parts.append(f"## {name}")
        parts.append(content)
        parts.append("")
    return "\n".join(parts)


def save_outputs(markdown_text):
    os.makedirs("outputs", exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = os.path.join("outputs", f"product_plan_{ts}.md")
    html_path = os.path.join("outputs", f"product_plan_{ts}.html")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    html_body = markdown.markdown(markdown_text, extensions=["tables", "fenced_code"])
    html = f"""<!doctype html><html><head><meta charset='utf-8'><title>AI Product Manager Agent</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:900px;margin:40px auto;line-height:1.7;color:#111}} h1,h2{{border-bottom:1px solid #ddd;padding-bottom:8px}} code,pre{{background:#f6f6f6;padding:2px 4px;border-radius:4px}} table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px}}</style>
</head><body>{html_body}</body></html>"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return md_path, html_path
