"""LLM 客户端使用示例

此文件演示了如何使用 LLM 客户端与不同的模型提供商进行交互。
"""

import asyncio
import os
from dotenv import load_dotenv

from agentscope.message import Msg
from configs.config import ModelConfig
from services.llm import LLMClient


async def basic_chat_example():
    """基本聊天示例"""
    print("=" * 50)
    print("基本聊天示例")
    print("=" * 50)
    
    # 从环境变量创建配置
    config = ModelConfig.from_env(provider="dashscope")
    
    # 初始化客户端
    client = LLMClient(config)
    
    # 创建消息
    messages = [
        Msg(name="user", content="你好，请用一句话介绍一下自己", role="user")
    ]
    
    # 发送聊天请求
    print("\n发送消息: 你好，请用一句话介绍一下自己")
    response = await client.chat(messages, reuse_history=False)
    
    # 处理响应
    print("\n模型回复:")
    for block in response.content:
        if block.get("type") == "text":
            print(block.get("text"))
    
    print("\n" + "=" * 50 + "\n")


async def chat_with_history_example():
    """带历史记录的多轮对话示例"""
    print("=" * 50)
    print("多轮对话示例（带历史）")
    print("=" * 50)
    
    config = ModelConfig.from_env(provider="dashscope")
    client = LLMClient(config)
    
    # 第一轮对话
    messages1 = [Msg(name="user", content="我叫张三", role="user")]
    print("\n第一轮 - 用户: 我叫张三")
    response1 = await client.chat(messages1, reuse_history=True)
    
    print("助手:", end=" ")
    for block in response1.content:
        if block.get("type") == "text":
            print(block.get("text"))
    
    # 第二轮对话（会包含第一轮的历史）
    messages2 = [Msg(name="user", content="我叫什么名字？", role="user")]
    print("\n第二轮 - 用户: 我叫什么名字？")
    response2 = await client.chat(messages2, reuse_history=True)
    
    print("助手:", end=" ")
    for block in response2.content:
        if block.get("type") == "text":
            print(block.get("text"))
    
    print("\n" + "=" * 50 + "\n")


async def custom_parameters_example():
    """自定义模型参数示例"""
    print("=" * 50)
    print("自定义参数示例（高温度 = 更有创意）")
    print("=" * 50)
    
    # 创建高温度配置（更有创意）
    config = ModelConfig.from_env(provider="dashscope")
    config.temperature = 0.95
    config.top_p = 0.9
    config.generate_kwargs = {
        "temperature": 0.95,
        "top_p": 0.9,
    }
    
    client = LLMClient(config)
    
    messages = [
        Msg(name="user", content="用一个词形容春天", role="user")
    ]
    
    print(f"\n模型参数: temperature={config.temperature}, top_p={config.top_p}")
    print("\n发送消息: 用一个词形容春天")
    response = await client.chat(messages, reuse_history=False)
    
    print("\n模型回复:")
    for block in response.content:
        if block.get("type") == "text":
            print(block.get("text"))
    
    print("\n" + "=" * 50 + "\n")


async def streaming_chat_example():
    """流式响应示例"""
    print("=" * 50)
    print("流式响应示例（实时显示）")
    print("=" * 50)
    
    config = ModelConfig.from_env(provider="dashscope")
    # 确保启用流式
    config.stream = True
    
    client = LLMClient(config)
    
    messages = [
        Msg(name="user", content="请数数字从1到10", role="user")
    ]
    
    print("\n发送消息: 请数数字从1到10")
    print("\n模型回复（流式）:", end=" ", flush=True)
    
    # 使用 chat_stream 方法获取流式响应
    if hasattr(client.client, "chat_stream"):
        async for chunk in client.client.chat_stream(messages, config, reuse_history=False):
            # 提取并显示文本
            for block in chunk.content:
                if block.get("type") == "text":
                    # 只打印新增的部分（实际使用中可能需要做差分）
                    print(block.get("text", ""), end="", flush=True)
        print()  # 换行
    else:
        print("\n当前客户端不支持流式响应方法")
    
    print("\n" + "=" * 50 + "\n")


async def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()
    
    # 检查环境变量
    if not os.getenv("DASHSCOPE_API_KEY"):
        print("错误: 未找到 DASHSCOPE_API_KEY 环境变量")
        print("请复制 .env.example 到 .env 并填写您的 API 密钥")
        return
    
    print("\n")
    print("🚀 LLM 客户端使用示例")
    print("\n")
    
    try:
        # 运行各种示例
        await basic_chat_example()
        await chat_with_history_example()
        await custom_parameters_example()
        await streaming_chat_example()
        
        print("✅ 所有示例运行完成！")
        
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

