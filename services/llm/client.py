# -*- coding: utf-8 -*-
"""LLM客户端主类"""

from enum import Enum
from typing import Any
from services.llm.base import BaseLLMClient
from agentscope.message import Msg
from agentscope.model import ChatResponse


class LLMProvider(Enum):
    """支持的 LLM 提供商"""
    
    DashScope = "dashscope"
    OpenAI = "openai"
    Anthropic = "anthropic"


class LLMClient:
    """支持多个提供商的主 LLM 客户端
    
    此类充当不同 LLM 提供商实现的门面。
    它根据模型配置中指定的提供商自动选择适当的客户端。
    """

    def __init__(self, model_config):
        """使用模型配置初始化 LLM 客户端
        
        Args:
            model_config: 包含提供商和模型设置的配置对象
            
        Raises:
            ValueError: 当指定的提供商不受支持时抛出
        """
        # 获取provider
        provider_str = getattr(model_config, 'provider', 'dashscope')
        self.provider: LLMProvider = LLMProvider(provider_str)
        self.model_config = model_config

        match self.provider:
            case LLMProvider.DashScope:
                from services.llm.dashscope import DashScopeClient
                self.client: BaseLLMClient = DashScopeClient(model_config)
            case LLMProvider.OpenAI:
                # TODO: 实现 OpenAI 客户端
                raise NotImplementedError("OpenAI 客户端尚未实现")
            case LLMProvider.Anthropic:
                # TODO: 实现 Anthropic 客户端
                raise NotImplementedError("Anthropic 客户端尚未实现")
            case _:
                raise ValueError(f"不支持的提供商: {self.provider}")

    def set_chat_history(self, messages: list[ChatResponse]) -> None:
        """设置聊天历史
        
        Args:
            messages: 来自之前对话的 ChatResponse 对象列表
        """
        self.client.set_chat_history(messages)

    async def chat(
        self,
        messages: list[Msg],
        model_config=None,
        tools: list[dict[str, Any]] | None = None,
        reuse_history: bool = True,
    ) -> ChatResponse:
        """向 LLM 发送聊天消息
        
        Args:
            messages: 要发送的 Msg 对象列表
            model_config: 可选的模型配置覆盖。如果为 None，使用默认配置
            tools: 可选的工具 JSON schemas 列表
            reuse_history: 是否包含之前的聊天历史
            
        Returns:
            来自模型的 ChatResponse
        """
        # 如果未提供，使用默认配置
        config = model_config or self.model_config
        return await self.client.chat(messages, config, tools, reuse_history)

    def supports_tool_calling(self, model_config=None) -> bool:
        """检查当前客户端是否支持工具调用
        
        Args:
            model_config: 可选的模型配置检查。如果为 None，使用默认配置
            
        Returns:
            如果模型支持工具调用返回 True，否则返回 False
        """
        config = model_config or self.model_config
        return hasattr(self.client, "supports_tool_calling") and self.client.supports_tool_calling(config)

