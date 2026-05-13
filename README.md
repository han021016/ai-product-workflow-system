# AI Product Manager Agent - DeepSeek + LangGraph + Tools

这是一个更真实的 AI 产品经理 Agent 工作流版本。

它不再是一次 API 调用生成所有内容，而是使用 LangGraph 把任务拆成多个节点：

```text
Tool Node：竞品分析工具 + 指标计算工具
↓
Idea Agent
↓
Persona Agent
↓
PRD Agent
↓
User Story Agent
↓
Roadmap Agent
↓
Metrics Agent
```

## 功能

- DeepSeek API 调用，不依赖 OpenAI SDK
- LangGraph 多节点工作流
- 工具调用：竞品分析工具、指标公式工具
- 每个 Agent 真正单独调用一次模型
- 上一步 Agent 输出会传给下一步 Agent
- 自动保存历史记录
- UI Tabs 展示结果
- Markdown / HTML 下载

## 运行方式

```bash
pip3 install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

`.env` 示例：

```env
DEEPSEEK_API_KEY=你的DeepSeek API Key
DEEPSEEK_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_URL=https://api.deepseek.com
```

## 面试讲法

这个项目实现了一个 AI Product Manager Workflow。系统使用 LangGraph 编排多个 Agent，每个 Agent 负责产品经理流程中的一个阶段，并通过状态传递实现上下文共享。工具节点会先对竞品和指标公式做结构化处理，然后后续 Agent 基于这些工具输出和前序 Agent 结果继续生成 PRD、User Stories、Roadmap 和 Metrics。
