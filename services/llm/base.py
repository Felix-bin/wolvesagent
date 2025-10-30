# -*- coding: utf-8 -*-
"""LLM客户端基类"""

from abc import ABC, abstractmethod
from typing import Any
from agentscope.message import Msg
from agentscope.model import ChatResponse


class BaseLLMClient(ABC):
    """LLM 客户端基类
    
    此类为所有 LLM 客户端实现提供基础接口。
    它处理模型配置的初始化，并定义所有客户端必须实现的核心方法。
    """

    def __init__(self, model_config):
        """使用模型配置初始化 LLM 客户端
        
        Args:
            model_config: 包含模型和提供商设置的配置对象
        """
        self.api_key: str = model_config.api_key
        self.base_url: str | None = getattr(model_config, 'base_url', None)
        self.api_version: str | None = getattr(model_config, 'api_version', None)
        self.model_config = model_config

    @abstractmethod
    def set_chat_history(self, messages: list[ChatResponse]) -> None:
        """设置聊天历史
        
        Args:
            messages: 代表之前对话的 ChatResponse 对象列表
        """
        pass

    @abstractmethod
    async def chat(
        self,
        messages: list[Msg],
        model_config,
        tools: list[dict[str, Any]] | None = None,
        reuse_history: bool = True,
    ) -> ChatResponse:
        """向 LLM 发送聊天消息
        
        Args:
            messages: 要发送到模型的 Msg 对象列表
            model_config: 此次调用的模型配置
            tools: 可选的工具 JSON schemas 列表，用于函数调用
            reuse_history: 是否包含之前的聊天历史
            
        Returns:
            来自模型的 ChatResponse
        """
        pass

    def supports_tool_calling(self, model_config) -> bool:
        """检查当前模型是否支持工具调用
        
        Args:
            model_config: 要检查的模型配置
            
        Returns:
            如果模型支持工具调用返回 True，否则返回 False
        """
        return getattr(model_config, 'supports_tool_calling', True)

