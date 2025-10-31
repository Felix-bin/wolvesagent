# -*- coding: utf-8 -*-
"""响应生成器 - 负责生成符合规范的响应"""

import time
from typing import Optional, Any, Dict
from agentscope.message import Msg
from agentscope.model import ChatModelBase
from utils.logger import WerewolfLogger


class ResponseGenerator:
    """响应生成器 - 处理大模型调用和响应格式化"""
    
    # 严格的时间和字符限制
    MAX_TIME = 30  # 30秒
    MAX_CHARS = 2048  # 2048字符
    SAFETY_MARGIN_TIME = 2  # 预留2秒安全边际
    
    def __init__(self, agent_name: str, model: ChatModelBase):
        self.agent_name = agent_name
        self.model = model
        self.logger = WerewolfLogger(agent_name)
    
    async def generate_response(
        self,
        prompt_msg: Msg,
        structured_model: Optional[type] = None,
        timeout: Optional[float] = None
    ) -> Msg:
        """生成响应（带时间和字符限制）
        
        Args:
            prompt_msg: 输入消息
            structured_model: 结构化输出模型类
            timeout: 超时时间（秒），默认使用MAX_TIME
            
        Returns:
            响应消息
        """
        start_time = time.time()
        timeout = timeout or self.MAX_TIME
        
        try:
            # 检查初始时间
            if time.time() - start_time > self.SAFETY_MARGIN_TIME:
                return self._create_timeout_response()
            
            # 如果有结构化模型，使用结构化输出
            if structured_model:
                response = await self._generate_structured_response(
                    prompt_msg,
                    structured_model,
                    start_time,
                    timeout
                )
            else:
                response = await self._generate_normal_response(
                    prompt_msg,
                    start_time,
                    timeout
                )
            
            # 检查响应长度
            if response.content and len(response.content) > self.MAX_CHARS:
                self.logger.warning(f"响应超长({len(response.content)}字符)，截断")
                response.content = response.content[:self.MAX_CHARS - 3] + "..."
            
            # 最终时间检查
            elapsed = time.time() - start_time
            if elapsed > timeout:
                self.logger.warning(f"响应超时({elapsed:.2f}秒)")
                return self._create_timeout_response()
            
            return response
            
        except Exception as e:
            self.logger.error(f"响应生成失败: {e}")
            return self._create_error_response(str(e))
    
    async def _generate_structured_response(
        self,
        prompt_msg: Msg,
        structured_model: type,
        start_time: float,
        timeout: float
    ) -> Msg:
        """生成结构化响应
        
        使用AgentScope的结构化输出机制，让框架自动处理
        """
        try:
            # 计算剩余时间
            remaining_time = timeout - (time.time() - start_time) - self.SAFETY_MARGIN_TIME
            
            if remaining_time <= 0:
                return self._create_timeout_response()
            
            # 调用模型生成结构化响应
            # AgentScope会自动处理structured_model
            response = await self._call_model_with_timeout(
                prompt_msg,
                structured_model,
                remaining_time
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"结构化响应生成失败: {e}")
            # 返回默认结构化响应
            return self._create_default_structured_response(structured_model)
    
    async def _generate_normal_response(
        self,
        prompt_msg: Msg,
        start_time: float,
        timeout: float
    ) -> Msg:
        """生成普通响应"""
        try:
            # 计算剩余时间
            remaining_time = timeout - (time.time() - start_time) - self.SAFETY_MARGIN_TIME
            
            if remaining_time <= 0:
                return self._create_timeout_response()
            
            # 调用模型
            response = await self._call_model_with_timeout(
                prompt_msg,
                None,
                remaining_time
            )
            
            return response
            
        except Exception as e:
            self.logger.error(f"普通响应生成失败: {e}")
            return self._create_error_response(str(e))
    
    async def _call_model_with_timeout(
        self,
        prompt_msg: Msg,
        structured_model: Optional[type],
        timeout: float
    ) -> Msg:
        """调用模型（带超时）
        
        注意：AgentScope的DashScopeChatModel支持结构化输出
        当传入structured_model时，模型会返回符合该结构的数据
        """
        try:
            # 准备消息内容
            if isinstance(prompt_msg, Msg):
                content = prompt_msg.content
            else:
                content = str(prompt_msg)
            
            # 构造消息列表
            messages = [{"role": "user", "content": content}]
            
            # 调用模型
            # AgentScope的模型API会自动处理structured_model参数
            if structured_model:
                # 带结构化输出
                # DashScopeChatModel支持structured_output参数
                try:
                    # 使用模型的generate方法
                    model_response = await self.model(
                        messages=messages,
                        parse_func=structured_model,
                        max_retries=1
                    )
                except Exception as model_error:
                    self.logger.warning(f"结构化模型调用失败: {model_error}，使用默认值")
                    # 返回默认值
                    return self._create_default_structured_response(structured_model)
            else:
                # 普通输出
                model_response = await self.model(messages=messages)
            
            # 构造响应消息
            response = Msg(
                name=self.agent_name,
                content=str(model_response.get('content', '')) if isinstance(model_response, dict) else str(model_response),
                role="assistant"
            )
            
            # 如果有结构化数据，存入metadata
            if structured_model:
                if response.metadata is None:
                    response.metadata = {}
                
                # 从模型响应中提取结构化数据
                if isinstance(model_response, dict):
                    # 如果响应是字典，直接更新metadata
                    response.metadata.update(model_response)
                elif hasattr(model_response, 'dict'):
                    # 如果响应是Pydantic模型
                    response.metadata.update(model_response.dict())
                elif hasattr(model_response, 'model_dump'):
                    # Pydantic v2
                    response.metadata.update(model_response.model_dump())
            
            return response
            
        except Exception as e:
            self.logger.error(f"模型调用失败: {e}")
            raise
    
    def _create_timeout_response(self) -> Msg:
        """创建超时响应"""
        return Msg(
            name=self.agent_name,
            content="时间不足，暂时跳过。",
            role="assistant"
        )
    
    def _create_error_response(self, error_msg: str) -> Msg:
        """创建错误响应"""
        return Msg(
            name=self.agent_name,
            content="遇到问题，需要重新思考。",
            role="assistant"
        )
    
    def _create_default_structured_response(self, structured_model: type) -> Msg:
        """创建默认结构化响应"""
        # 根据模型类型返回默认值
        default_values = self._get_default_structured_values(structured_model)
        
        msg = Msg(
            name=self.agent_name,
            content="采用默认决策。",
            role="assistant"
        )
        
        if msg.metadata is None:
            msg.metadata = {}
        msg.metadata.update(default_values)
        
        return msg
    
    def _get_default_structured_values(self, structured_model: type) -> Dict[str, Any]:
        """获取结构化模型的默认值"""
        model_name = getattr(structured_model, '__name__', 'Unknown')
        
        # 根据模型名称返回默认值
        if 'Discussion' in model_name:
            return {'reach_agreement': False}
        elif 'Vote' in model_name:
            # 返回一个空投票（让上层处理）
            return {'vote': ''}
        elif 'WitchResurrect' in model_name:
            return {'resurrect': False}
        elif 'Poison' in model_name:
            return {'poison': False, 'name': None}
        elif 'Seer' in model_name:
            # 返回一个空名字（让上层处理）
            return {'name': ''}
        elif 'Hunter' in model_name:
            return {'shoot': False, 'name': None}
        else:
            return {}
    
    def truncate_content(self, content: str) -> str:
        """截断内容到允许的最大长度"""
        if len(content) <= self.MAX_CHARS:
            return content
        return content[:self.MAX_CHARS - 3] + "..."
    
    def check_time_remaining(self, start_time: float) -> float:
        """检查剩余时间"""
        elapsed = time.time() - start_time
        remaining = self.MAX_TIME - elapsed
        return max(0, remaining)

