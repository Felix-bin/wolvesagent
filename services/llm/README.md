# LLM 服务模块

此模块提供了与各种 LLM 提供商（如 DashScope、OpenAI、Anthropic）交互的统一接口，基于 [AgentScope](https://github.com/modelscope/agentscope) 框架实现。

## 功能特性

- 🔌 **多提供商支持**：统一接口支持 DashScope、OpenAI、Anthropic 等多个 LLM 提供商
- ⚙️ **灵活配置**：从环境变量和配置文件读取模型参数（temperature、max_tokens 等）
- 🛠️ **工具调用**：支持函数调用（Function Calling）功能
- 💭 **思维链**：支持启用模型思维模式（如 DeepSeek-R1、QwQ 等）
- 📝 **历史管理**：内置聊天历史管理功能
- 🔄 **流式输出**：支持流式响应输出

## 安装

确保已安装必要的依赖：

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install agentscope
```

## 快速开始

### 1. 配置环境变量

复制 `.env.example` 到 `.env` 并填写您的 API 密钥：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
# 选择提供商: dashscope, openai, anthropic
LLM_PROVIDER=dashscope

# DashScope 配置
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_MODEL_NAME=qwen3-max

# 模型参数
MODEL_TEMPERATURE=0.7
MODEL_STREAM=true
```

### 2. 基本使用

```python
import asyncio
from agentscope.message import Msg
from configs.config import ModelConfig
from services.llm import LLMClient

async def main():
    # 从环境变量创建配置
    config = ModelConfig.from_env(provider="dashscope")
    
    # 初始化客户端
    client = LLMClient(config)
    
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

### 3. 使用工具调用

```python
import asyncio
from agentscope.message import Msg
from agentscope.tool import Toolkit, ToolResponse
from configs.config import ModelConfig
from services.llm import LLMClient

# 定义工具函数（必须返回 ToolResponse）
async def get_weather(city: str) -> ToolResponse:
    """获取指定城市的天气信息
    
    Args:
        city: 城市名称
        
    Returns:
        包含天气信息的 ToolResponse
    """
    weather_info = f"{city} 今天晴天，温度 20-25°C"
    return ToolResponse(
        content=[{"type": "text", "text": weather_info}]
    )

async def main():
    # 初始化配置和客户端
    config = ModelConfig.from_env(provider="dashscope")
    client = LLMClient(config)
    
    # 创建工具包并注册函数
    toolkit = Toolkit()
    toolkit.register_tool_function(get_weather)
    
    # 获取工具的 JSON schemas（返回 list[dict]）
    tools = toolkit.get_json_schemas()
    
    # 创建消息
    messages = [
        Msg(name="user", content="北京今天天气怎么样？", role="user")
    ]
    
    # 带工具的聊天请求
    response = await client.chat(messages, tools=tools)
    
    # 检查是否有工具调用
    for block in response.content:
        if block.get("type") == "tool_use":
            # 执行工具调用（toolkit.call_tool_function 返回 AsyncGenerator）
            async for tool_result in toolkit.call_tool_function(block):
                # 处理工具结果（累积的）
                if tool_result.is_last:
                    print(f"工具调用结果: {tool_result.content}")

asyncio.run(main())
```

### 4. 管理聊天历史

```python
import asyncio
from agentscope.message import Msg
from configs.config import ModelConfig
from services.llm import LLMClient

async def main():
    config = ModelConfig.from_env(provider="dashscope")
    client = LLMClient(config)
    
    # 第一轮对话
    messages1 = [Msg(name="user", content="我叫张三", role="user")]
    response1 = await client.chat(messages1, reuse_history=True)
    
    # 第二轮对话（会包含第一轮的历史）
    messages2 = [Msg(name="user", content="我叫什么名字？", role="user")]
    response2 = await client.chat(messages2, reuse_history=True)
    
    # 模型应该能记住之前说的名字

asyncio.run(main())
```

### 5. 自定义模型参数

```python
import asyncio
from agentscope.message import Msg
from configs.config import ModelConfig, ModelProviderConfig
from services.llm import LLMClient

async def main():
    # 方式 1: 从环境变量创建并修改参数
    config = ModelConfig.from_env(provider="dashscope")
    config.temperature = 0.9  # 调整温度
    config.max_tokens = 2000  # 设置最大 token 数
    
    # 方式 2: 手动创建配置
    provider_config = ModelProviderConfig(
        provider="dashscope",
        api_key="your_api_key",
        base_url=None
    )
    
    config = ModelConfig(
        model_name="qwen3-max",
        model_provider=provider_config,
        temperature=0.8,
        max_tokens=4000,
        top_p=0.95,
        stream=True,
        generate_kwargs={
            "temperature": 0.8,
            "max_tokens": 4000,
            "top_p": 0.95
        }
    )
    
    client = LLMClient(config)
    messages = [Msg(name="user", content="生成一个创意故事", role="user")]
    response = await client.chat(messages)

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

## 添加新的提供商

要添加新的 LLM 提供商（如 OpenAI、Anthropic），请按照以下步骤：

1. **创建客户端实现**：在 `services/llm/` 下创建新文件（如 `openai.py`）

```python
from agentscope.model import OpenAIChatModel, ChatResponse
from agentscope.message import Msg
from services.llm.base import BaseLLMClient
from configs.config import ModelConfig

class OpenAIClient(BaseLLMClient):
    """使用 agentscope 实现的 OpenAI 客户端"""
    
    def __init__(self, model_config: ModelConfig):
        super().__init__(model_config)
        self.model = OpenAIChatModel(
            api_key=self.api_key,
            model_name=model_config.model_name,
            stream=model_config.stream,
            generate_kwargs=model_config.generate_kwargs,
        )
        self._chat_history = []
    
    def set_chat_history(self, messages):
        # 实现历史管理
        pass
    
    async def chat(self, messages, model_config, tools=None, reuse_history=True):
        # 实现聊天逻辑
        pass
```

2. **更新 client.py**：在 `LLMClient.__init__` 中添加新的 case

```python
case LLMProvider.OpenAI:
    from .openai import OpenAIClient
    self.client: BaseLLMClient = OpenAIClient(model_config)
```

3. **更新配置**：在 `ModelConfig.from_env` 中添加新提供商的环境变量处理

## API 参考

### ModelConfig

模型配置类，用于管理 LLM 模型的所有配置参数。

**字段：**
- `model_name`: 模型名称（如 "qwen3-max"）
- `model_provider`: 提供商配置
- `temperature`: 温度参数（0.0-1.0）
- `max_tokens`: 最大生成 token 数
- `top_p`: Top-p 采样参数
- `stream`: 是否启用流式输出
- `enable_thinking`: 是否启用思维模式
- `supports_tool_calling`: 是否支持工具调用
- `generate_kwargs`: 额外的生成参数字典

**方法：**
- `from_env(provider: str) -> ModelConfig`: 从环境变量创建配置

### LLMClient

主 LLM 客户端类，提供统一的接口访问不同的 LLM 提供商。

**方法：**

#### `__init__(model_config: ModelConfig)`
初始化客户端

#### `async chat(messages, model_config=None, tools=None, reuse_history=True) -> ChatResponse`
发送聊天消息

**参数：**
- `messages`: Msg 对象列表
- `model_config`: 可选的配置覆盖
- `tools`: 可选的工具 JSON schemas 列表（从 `Toolkit.get_json_schemas()` 获取）
- `reuse_history`: 是否重用历史

**返回：**
- `ChatResponse`: 模型响应

#### `set_chat_history(messages: list[ChatResponse])`
设置聊天历史

#### `supports_tool_calling(model_config=None) -> bool`
检查是否支持工具调用

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DASHSCOPE_API_KEY` | DashScope API 密钥 | 必填 |
| `DASHSCOPE_MODEL_NAME` | DashScope 模型名称 | qwen3-max |
| `DASHSCOPE_BASE_URL` | DashScope API 基础 URL | 可选 |
| `MODEL_TEMPERATURE` | 温度参数 | 0.7 |
| `MODEL_MAX_TOKENS` | 最大 token 数 | 可选 |
| `MODEL_TOP_P` | Top-p 采样 | 可选 |
| `MODEL_STREAM` | 启用流式输出 | true |
| `MODEL_ENABLE_THINKING` | 启用思维模式 | 可选 |

## 常见问题

### Q: 如何处理流式响应？

A: LLM 客户端提供两种方式处理流式响应：

**方式 1: 使用 `chat()` 方法（自动处理流式）**

`chat()` 方法会自动处理流式响应，返回最终的完整 `ChatResponse`：

```python
config = ModelConfig.from_env(provider="dashscope")
config.stream = True  # 启用流式

client = LLMClient(config)
response = await client.chat(messages)  # 自动收集所有流式块

# 直接使用完整响应
for block in response.content:
    if block.get("type") == "text":
        print(block.get("text"))
```

**方式 2: 使用 `chat_stream()` 方法（实时流式）**

如果需要实时处理流式响应（例如实时显示输出），可以使用 `chat_stream()` 方法：

```python
config = ModelConfig.from_env(provider="dashscope")
config.stream = True

client = LLMClient(config)

# 实时处理流式响应
async for chunk in client.client.chat_stream(messages, config):
    for block in chunk.content:
        if block.get("type") == "text":
            print(block.get("text"), end="", flush=True)
print()  # 换行
```

注意：`chat_stream()` 返回的是累积的响应块，每个块都包含从开始到当前的完整内容。

### Q: 如何启用思维模式？

A: 在环境变量中设置 `MODEL_ENABLE_THINKING=true`，或在代码中：

```python
config = ModelConfig.from_env(provider="dashscope")
config.enable_thinking = True
```

### Q: 如何处理工具调用的响应？

A: 工具函数必须返回 `ToolResponse` 对象，使用 `Toolkit.call_tool_function()` 来执行工具调用：

```python
from agentscope.tool import Toolkit, ToolResponse

# 工具函数必须返回 ToolResponse
async def my_tool(arg: str) -> ToolResponse:
    result = f"处理了: {arg}"
    return ToolResponse(content=[{"type": "text", "text": result}])

# 注册工具
toolkit = Toolkit()
toolkit.register_tool_function(my_tool)

# 获取 JSON schemas 传递给模型
tools = toolkit.get_json_schemas()
response = await client.chat(messages, tools=tools)

# 处理工具调用
for block in response.content:
    if block.get("type") == "tool_use":
        # call_tool_function 返回 AsyncGenerator
        async for tool_result in toolkit.call_tool_function(block):
            if tool_result.is_last:
                print(tool_result.content)
```

## 参考资料

- [AgentScope 文档](https://agentscope.io/)
- [DashScope API 文档](https://help.aliyun.com/zh/dashscope/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic API 文档](https://docs.anthropic.com/)

## License

本项目遵循项目根目录的 LICENSE 文件。

