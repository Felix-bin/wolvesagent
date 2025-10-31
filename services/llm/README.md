# LLM 服务模块

此模块提供了与各种 LLM 提供商（如 DashScope、OpenAI、Anthropic）交互的统一接口，基于 [AgentScope](https://github.com/modelscope/agentscope) 框架实现。

## 功能特性

- 🔌 **多提供商支持**：统一接口支持 DashScope、OpenAI、Anthropic 等多个 LLM 提供商
- ⚙️ **灵活配置**：从环境变量和配置文件读取模型参数（temperature、max_tokens 等）
- 🛠️ **工具调用**：支持函数调用（Function Calling）功能
- 💭 **思维链**：支持启用模型思维模式（如 DeepSeek-R1、QwQ 等）
- 📝 **历史管理**：内置聊天历史管理功能
- 🔄 **流式输出**：支持流式响应输出

## 快速开始

### 配置环境变量

创建`.env`文件或设置环境变量：

```env
# DashScope 配置
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_MODEL_NAME=qwen3-max

# 模型参数
MODEL_TEMPERATURE=0.7
MODEL_STREAM=false  # 兼容现有项目
```

### 基本使用

```python
import asyncio
from agentscope.message import Msg
from config.models import create_llm_client

async def main():
    # 从环境变量创建客户端
    client = create_llm_client()
    
    # 创建消息
    messages = [
        Msg(name="user", content="你好，请介绍一下自己", role="user")
    ]
    
    # 发送聊天请求
    response = await client.chat(messages)
    
    # 处理响应
    for block in response.content:
        if block.get("type") == "text":
            print(block.get("text"))

asyncio.run(main())
```

## 架构设计

```
services/llm/
├── __init__.py          # 模块导出
├── base.py              # BaseLLMClient 基类
├── client.py            # LLMClient 主客户端和 LLMProvider 枚举
├── dashscope.py         # DashScope 客户端实现
└── README.md            # 本文档
```

### 类关系

```
BaseLLMClient (抽象基类)
    ↑
    │ 继承
    │
DashScopeClient (具体实现)
    ↑
    │ 使用
    │
LLMClient (门面模式)
```

## API 参考

### create_llm_client()

创建LLM客户端的便捷函数（推荐使用）

**参数：**
- `provider`: 提供商名称（默认"dashscope"）
- `model_name`: 模型名称（默认从环境变量读取）
- `from_env`: 是否从环境变量读取配置（默认True）

**返回：**
- `LLMClient`: 配置好的客户端实例

**示例：**
```python
# 使用默认配置
client = create_llm_client()

# 指定模型
client = create_llm_client(model_name="deepseek-v3")
```

### LLMClient.chat()

发送聊天消息

**参数：**
- `messages`: Msg 对象列表
- `model_config`: 可选的配置覆盖
- `tools`: 可选的工具 JSON schemas 列表
- `reuse_history`: 是否重用历史（默认True）

**返回：**
- `ChatResponse`: 模型响应

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DASHSCOPE_API_KEY` | DashScope API 密钥 | 必填 |
| `DASHSCOPE_MODEL_NAME` | DashScope 模型名称 | qwen-max |
| `MODEL_TEMPERATURE` | 温度参数 | 0.7 |
| `MODEL_MAX_TOKENS` | 最大 token 数 | 可选 |
| `MODEL_STREAM` | 启用流式输出 | false |

## 更多信息

详见：
- [LLM服务集成文档](../../docs/LLM_SERVICE_INTEGRATION.md)
- [AgentScope 文档](https://agentscope.io/)
- [DashScope API 文档](https://help.aliyun.com/zh/dashscope/)




