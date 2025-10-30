# -*- coding: utf-8 -*-
"""DashScope客户端实现"""

from typing import Any
from agentscope.model import DashScopeChatModel, ChatResponse
from agentscope.message import Msg
from services.llm.base import BaseLLMClient


class DashScopeClient(BaseLLMClient):
    """使用 agentscope 实现的 DashScope 客户端"""

    def __init__(self, model_config):
        super().__init__(model_config)
        
        # 使用配置中的所有参数初始化 DashScope 模型
        generate_kwargs = getattr(model_config, 'generate_kwargs', {})
        if not generate_kwargs:
            # 从配置构建generate_kwargs
            generate_kwargs = {}
            if hasattr(model_config, 'temperature'):
                generate_kwargs['temperature'] = model_config.temperature
            if hasattr(model_config, 'max_tokens') and model_config.max_tokens:
                generate_kwargs['max_tokens'] = model_config.max_tokens
            if hasattr(model_config, 'top_p') and model_config.top_p:
                generate_kwargs['top_p'] = model_config.top_p
        
        self.model: DashScopeChatModel = DashScopeChatModel(
            api_key=self.api_key,
            model_name=model_config.model_name,
            stream=getattr(model_config, 'stream', True),
            enable_thinking=getattr(model_config, 'enable_thinking', None),
            generate_kwargs=generate_kwargs,
            base_http_api_url=self.base_url,
        )
        
        # 存储聊天历史
        self._chat_history: list[dict] = []
    
    def set_chat_history(self, messages: list[ChatResponse]) -> None:
        """设置聊天历史
        
        Args:
            messages: 要设置为历史的 ChatResponse 对象列表
        """
        # 将 ChatResponse 转换为 DashScope API 的 dict 格式
        self._chat_history = []
        for msg in messages:
            # 根据 ChatResponse 内容提取消息字典
            for block in msg.content:
                if block.get("type") == "text":
                    self._chat_history.append({
                        "role": "assistant",
                        "content": block.get("text", "")
                    })
    
    async def chat(
        self,
        messages: list[Msg],
        model_config,
        tools: list[dict[str, Any]] | None = None,
        reuse_history: bool = True,
    ) -> ChatResponse:
        """向 DashScope API 发送聊天消息
        
        Args:
            messages: 要发送的 Msg 对象列表
            model_config: 模型配置
            tools: 可选的工具 JSON schemas 列表
            reuse_history: 是否重用现有聊天历史
            
        Returns:
            来自模型的 ChatResponse
        """
        # 准备 API 调用的消息
        api_messages = []
        
        # 如果 reuse_history 为 True，则添加历史记录
        if reuse_history and self._chat_history:
            api_messages.extend(self._chat_history)
        
        # 将 Msg 对象转换为 dict 格式
        for msg in messages:
            message_dict = {
                "role": msg.role,
                "content": msg.content if isinstance(msg.content, str) else self._convert_content_blocks(msg.content)
            }
            if hasattr(msg, "name") and msg.name:
                message_dict["name"] = msg.name
            api_messages.append(message_dict)
        
        # 工具 schemas 已经是正确的格式
        tool_schemas = tools
        
        # 获取generate_kwargs
        generate_kwargs = getattr(model_config, 'generate_kwargs', {})
        if not generate_kwargs:
            generate_kwargs = {}
            if hasattr(model_config, 'temperature'):
                generate_kwargs['temperature'] = model_config.temperature
            if hasattr(model_config, 'max_tokens') and model_config.max_tokens:
                generate_kwargs['max_tokens'] = model_config.max_tokens
            if hasattr(model_config, 'top_p') and model_config.top_p:
                generate_kwargs['top_p'] = model_config.top_p
        
        # 调用模型
        response = await self.model(
            messages=api_messages,
            tools=tool_schemas,
            **generate_kwargs
        )
        
        # 处理流式响应
        stream = getattr(model_config, 'stream', True)
        if stream:
            # 对于流式响应，收集所有块并返回最后一个（累积的）
            final_response = None
            async for chunk in response:
                final_response = chunk
            response = final_response
        
        # 使用新消息和响应更新聊天历史
        if reuse_history and response:
            self._chat_history.extend(api_messages)
            # 将助手响应添加到历史
            self._chat_history.append({
                "role": "assistant",
                "content": self._extract_text_from_response(response)
            })
        
        return response
    
    async def chat_stream(
        self,
        messages: list[Msg],
        model_config,
        tools: list[dict[str, Any]] | None = None,
        reuse_history: bool = True,
    ):
        """向 DashScope API 发送聊天消息并返回流式生成器
        
        此方法仅在 stream=True 时有效，返回一个异步生成器用于实时处理响应。
        
        Args:
            messages: 要发送的 Msg 对象列表
            model_config: 模型配置
            tools: 可选的工具 JSON schemas 列表
            reuse_history: 是否重用现有聊天历史
            
        Yields:
            ChatResponse 的流式块（累积的）
        """
        # 准备 API 调用的消息
        api_messages = []
        
        if reuse_history and self._chat_history:
            api_messages.extend(self._chat_history)
        
        for msg in messages:
            message_dict = {
                "role": msg.role,
                "content": msg.content if isinstance(msg.content, str) else self._convert_content_blocks(msg.content)
            }
            if hasattr(msg, "name") and msg.name:
                message_dict["name"] = msg.name
            api_messages.append(message_dict)
        
        tool_schemas = tools
        
        # 获取generate_kwargs
        generate_kwargs = getattr(model_config, 'generate_kwargs', {})
        
        # 调用模型
        response = await self.model(
            messages=api_messages,
            tools=tool_schemas,
            **generate_kwargs
        )
        
        # 流式返回
        last_chunk = None
        async for chunk in response:
            last_chunk = chunk
            yield chunk
        
        # 更新历史
        if reuse_history and last_chunk:
            self._chat_history.extend(api_messages)
            self._chat_history.append({
                "role": "assistant",
                "content": self._extract_text_from_response(last_chunk)
            })
    
    def _convert_content_blocks(self, content: list) -> str | list:
        """将内容块转换为适当的格式
        
        Args:
            content: 内容块列表
            
        Returns:
            API 格式化的内容
        """
        # 对于简单的文本块，返回字符串
        if len(content) == 1 and content[0].get("type") == "text":
            return content[0].get("text", "")
        # 对于复杂内容（多模态），返回列表
        return content
    
    def _extract_text_from_response(self, response: ChatResponse) -> str:
        """从 ChatResponse 中提取文本内容
        
        Args:
            response: ChatResponse 对象
            
        Returns:
            提取的文本内容
        """
        text_parts = []
        for block in response.content:
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
        return " ".join(text_parts)

