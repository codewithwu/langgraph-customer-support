# langgraph-customer-support

基于 LangGraph 的智能客服分流 Agent，支持问题分类、情感分析和自动路由，负面情绪自动转人工处理。

## 功能特性

- **意图识别**：LLM 自动将客户问题分类为技术支持、账单问题、一般咨询
- **情感分析**：实时判断客户情绪（积极/中性/消极），负面情绪自动升级人工客服
- **智能路由**：根据分类和情感结果，将请求分发至对应的专业处理节点
- **多模型支持**：工厂模式统一管理 8 种 LLM 提供商（LongCat、DeepSeek、智谱、百灵、硅基流动、魔搭、Ollama、NVIDIA），一键切换
- **Web 聊天界面**：内置 FastAPI 后端 + 现代化聊天 UI，开箱即用

## 工作流架构

```
START → categorize → analyze_sentiment → route_query
                                              │
                          ┌───────────────────┼───────────────────┐
                          │                   │                   │
                   sentiment==消极       category==技术支持    category==账单问题
                          │                   │                   │
                          ▼                   ▼                   ▼
                     escalate           handle_technical     handle_billing
                     (转人工)             (技术支持回复)         (账单回复)
                          │                   │                   │
                          ▼                   ▼                   ▼
                        END          (category==一般咨询) → handle_general → END
```

- 情感判断优先级最高：消极情绪直接升级人工，无论问题类别
- 每次请求经过 3 个节点：分类 → 情感分析 → 专业处理

## 快速开始

### 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装

```bash
# 克隆项目
git clone <repo-url>
cd langgraph-customer-support

# 安装依赖
uv sync
```

### 配置

创建 `.env` 文件，填入 LLM 提供商的 API 配置（至少配置一个）：

```env
# 以 LongCat 为例
LONGCAT_API_KEY=sk-your-api-key
LONGCAT_BASEURL=https://api.longcat.chat/openai
LONGCAT_MODEL_NAME=LongCat-Flash-Lite
```

其他提供商的环境变量格式相同，前缀分别为：`DEEPSEEK`、`ZHIPU`、`LING`、`SILICONFLOW`、`MODELSCOPE`、`NVIDIA`、`OLLAMA`。

### 启动

```bash
uv run python main.py
```

- 聊天页面：http://localhost:8000
- API 文档：http://localhost:8000/docs

## API 接口

### POST /chat

提交客户问题，执行 LangGraph 工作流并返回结果。

**请求：**

```json
{
  "query": "我的网络一直断线，能帮我看看吗？"
}
```

**响应：**

```json
{
  "query": "我的网络一直断线，能帮我看看吗？",
  "category": "技术支持",
  "sentiment": "消极",
  "response": "该问题因情感消极已被升级转交人工客服处理。"
}
```

**使用 curl 测试：**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "我的网络一直断线，能帮我看看吗？"}'
```

## 项目结构

```
langgraph-customer-support/
├── langgraph_customer_support/     # LangGraph 工作流核心
│   ├── state.py                    # 状态定义 (TypedDict)
│   ├── nodes.py                    # 6 个工作流节点
│   ├── routes.py                   # 条件路由逻辑
│   ├── graph.py                    # 图构建与编译
│   ├── prompts.py                  # 系统提示词
│   ├── llm.py                      # LLM 单例初始化
│   └── config.py                   # 配置常量
├── langchain_agent/                # LLM 基础设施
│   ├── agents/                     # 单例客户端 & JSON Agent
│   ├── middleware/                  # 中间件系统
│   └── utils/                      # LLM 工厂 & 输出格式化
├── src/                            # Web 服务
│   ├── main.py                     # FastAPI 应用
│   └── static/index.html           # 聊天前端
├── main.py                         # 启动入口
└── pyproject.toml                  # 项目配置
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 工作流引擎 | LangGraph |
| LLM 框架 | LangChain |
| 后端框架 | FastAPI |
| ASGI 服务器 | Uvicorn |
| 包管理 | uv |
| 代码质量 | Ruff, mypy |

## 开发

```bash
# 格式化 & Lint
uv run ruff format . && uv run ruff check --fix .

# 类型检查
uv run mypy src/

# 运行测试
uv run pytest -v
```

## 许可证

MIT License
