import streamlit as st
from graph.workflow import run_langgraph_product_manager_workflow
from utils.storage import load_history, save_record, delete_record
from utils.export import build_markdown, save_outputs

st.set_page_config(page_title="AI 产品经理 Agent", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.stApp { background: #0b0f14; color: #f4f4f5; }
.hero { padding: 34px; border-radius: 22px; background: linear-gradient(135deg,#351b24,#111827); border:1px solid #263244; }
.card { padding: 18px; border-radius: 16px; background:#111820; border:1px solid #263244; margin-bottom:14px; }
.badge { display:inline-block; padding:7px 11px; border-radius:999px; background:#6b2632; color:#fff; margin-right:7px; font-size:13px; }
.small { color:#a1a1aa; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("产品输入")
    product_idea = st.text_area("产品创意", placeholder="例如：一个帮助大学生自动规划留学申请时间线、文书和材料的 AI Agent。", height=130)
    target_users = st.text_input("目标用户", placeholder="例如：准备申请海外研究生的大学生")
    platform = st.selectbox("平台", ["Web应用程序", "iOS App", "Android App", "SaaS", "小程序"])
    competitors = st.text_area("竞争对手/参考资料（可选）", placeholder="例如：Notion, ChatGPT, Grammarly, Google Calendar", height=90)
    run_btn = st.button("运行多 Agent 工作流", use_container_width=True)

    st.divider()
    st.subheader("历史记录")
    history = load_history()
    if history:
        for item in history[:8]:
            with st.expander(f"{item['created_at']}｜{item['product_idea'][:12]}"):
                if st.button("加载", key=f"load_{item['id']}"):
                    st.session_state["loaded_result"] = item
                    st.rerun()
                if st.button("删除", key=f"del_{item['id']}"):
                    delete_record(item["id"])
                    st.rerun()
    else:
        st.caption("暂无历史记录。生成后会自动保存。")

st.markdown("""
<div class='hero'>
<h1>🤖 AI 产品经理 Agent</h1>
<p>把一个产品想法自动转化为产品简介、用户画像、PRD、用户故事、路线图、指标与风险。</p>
<span class='badge'>Idea Agent</span><span class='badge'>Persona Agent</span><span class='badge'>PRD Agent</span><span class='badge'>User Story Agent</span><span class='badge'>Roadmap Agent</span><span class='badge'>Metrics Agent</span>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown("<div class='card'><b>6 个 Agent</b><br><span class='small'>多步运行，不是一次性输出</span></div>", unsafe_allow_html=True)
with c2: st.markdown("<div class='card'><b>自动保存历史</b><br><span class='small'>展示项目管理能力</span></div>", unsafe_allow_html=True)
with c3: st.markdown("<div class='card'><b>可下载报告</b><br><span class='small'>Markdown / HTML / 可转 PDF</span></div>", unsafe_allow_html=True)

results = None
tool_outputs = None
source_meta = None

if "loaded_result" in st.session_state:
    item = st.session_state["loaded_result"]
    results = item["results"]
    tool_outputs = item.get("tool_outputs")
    source_meta = item
    st.info(f"已加载历史记录：{item['created_at']}")

if run_btn:
    if not product_idea.strip() or not target_users.strip():
        st.warning("请至少填写产品创意和目标用户。")
    else:
        progress = st.progress(0)
        status_box = st.empty()
        def progress_callback(i, total, name):
            status_box.info(f"正在运行第 {i}/{total} 步：{name}")
            progress.progress(i / total)
        try:
            results, tool_outputs = run_langgraph_product_manager_workflow(product_idea, target_users, platform, competitors, progress_callback)
            source_meta = save_record(product_idea, target_users, platform, competitors, results, tool_outputs)
            status_box.success("多 Agent 工作流完成，结果已保存到历史记录。")
        except Exception as e:
            status_box.error(f"生成失败：{e}")
            st.stop()

if results:
    if tool_outputs:
        with st.expander("查看工具调用结果：竞品分析工具 + 指标计算工具", expanded=False):
            for tool_name, tool_content in tool_outputs.items():
                st.markdown(f"### {tool_name}")
                st.markdown(tool_content)

    tabs = st.tabs(list(results.keys()))
    for tab, (name, content) in zip(tabs, results.items()):
        with tab:
            st.markdown(f"<div class='card'>", unsafe_allow_html=True)
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)

    meta_product_idea = source_meta.get("product_idea", product_idea)
    meta_target_users = source_meta.get("target_users", target_users)
    meta_platform = source_meta.get("platform", platform)
    meta_competitors = source_meta.get("competitors", competitors)
    md_text = build_markdown(meta_product_idea, meta_target_users, meta_platform, meta_competitors, results)
    md_path, html_path = save_outputs(md_text)
    st.subheader("下载报告")
    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button("下载 Markdown", md_text, file_name="ai_product_manager_report.md", mime="text/markdown", use_container_width=True)
    with col_b:
        with open(html_path, "r", encoding="utf-8") as f:
            html_text = f.read()
        st.download_button("下载 HTML", html_text, file_name="ai_product_manager_report.html", mime="text/html", use_container_width=True)
else:
    st.info("在左侧输入产品创意，然后点击“运行多 Agent 工作流”。")
    st.subheader("推荐测试输入")
    st.code("""产品创意：一个帮助大学生自动规划留学申请时间线、文书和材料的 AI Agent。
目标用户：准备申请海外研究生的大学生
平台：Web应用程序
竞品：Notion, ChatGPT, Grammarly, Google Calendar""")
