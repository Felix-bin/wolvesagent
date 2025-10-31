#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一模型配置模块
支持DashScope等多个LLM提供商，提供两种配置方式：
1. 从YAML配置文件加载（传统方式）
2. 从环境变量加载（推荐，更灵活）
"""

import os
import yaml
from pathlib import Path

# 加载.env文件
try:
    from dotenv import load_dotenv
    # 查找项目根目录的.env文件
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[INFO] 已从 {env_path} 加载环境变量")
except ImportError:
    print("[WARNING] python-dotenv未安装，无法加载.env文件")
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from agentscope.model import (
    DashScopeChatModel,
    ChatModelBase
)
from services.llm import LLMClient, LLMProvider


@dataclass
class EnhancedModelConfig:
    """增强的模型配置类（兼容新的LLM客户端）"""
    
    model_name: str  # 例如: "qwen3-max", "deepseek-v3"
    provider: str = "dashscope"  # 提供商
    api_key: str = ""
    base_url: str | None = None
    api_version: str | None = None
    
    # 模型参数
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float | None = None
    stream: bool = False  # 默认非流式（兼容当前项目）
    
    # 高级参数
    enable_thinking: bool | None = None
    supports_tool_calling: bool = True
    
    # 额外的生成参数
    generate_kwargs: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls, provider: str = "dashscope", model_name: str = None) -> "EnhancedModelConfig":
        """从环境变量创建增强配置
        
        Args:
            provider: 模型提供商名称
            model_name: 模型名称，如果为None则使用默认值
            
        Returns:
            EnhancedModelConfig 实例
        """
        if provider == "dashscope":
            api_key = os.getenv("DASHSCOPE_API_KEY", "")
            if model_name is None:
                model_name = os.getenv("DASHSCOPE_MODEL_NAME", "qwen-max")
            base_url = os.getenv("DASHSCOPE_BASE_URL")
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY", "")
            if model_name is None:
                model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
            base_url = os.getenv("OPENAI_BASE_URL")
        else:
            raise ValueError(f"不支持的提供商: {provider}")
        
        # 从环境变量读取模型参数
        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("MODEL_MAX_TOKENS")) if os.getenv("MODEL_MAX_TOKENS") else None
        top_p = float(os.getenv("MODEL_TOP_P")) if os.getenv("MODEL_TOP_P") else None
        stream = os.getenv("MODEL_STREAM", "false").lower() == "true"
        enable_thinking_env = os.getenv("MODEL_ENABLE_THINKING", "")
        enable_thinking = enable_thinking_env.lower() == "true" if enable_thinking_env else None
        
        # 构建 generate_kwargs
        generate_kwargs = {}
        if temperature:
            generate_kwargs["temperature"] = temperature
        if max_tokens:
            generate_kwargs["max_tokens"] = max_tokens
        if top_p:
            generate_kwargs["top_p"] = top_p
        
        return cls(
            model_name=model_name,
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            enable_thinking=enable_thinking,
            generate_kwargs=generate_kwargs,
        )
    
    def to_llm_client(self) -> LLMClient:
        """转换为LLM客户端
        
        Returns:
            配置好的LLMClient实例
        """
        return LLMClient(self)


class ModelConfig:
    """模型配置管理类"""
    
    def __init__(self, config_path: str = "config/model_config.yaml"):
        """
        初始化模型配置
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.current_model = None
        self.model_type = None
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # 处理环境变量替换
            self._process_env_vars(config)
            return config
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self._get_default_config()
    
    def _process_env_vars(self, config: Dict[str, Any]) -> None:
        """处理配置中的环境变量"""
        import re
        
        def replace_env_vars(obj):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    obj[key] = replace_env_vars(value)
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    obj[i] = replace_env_vars(item)
            elif isinstance(obj, str) and obj.startswith('${') and obj.endswith('}'):
                # 提取环境变量名
                env_var = obj[2:-1]
                # 获取环境变量值，如果不存在则使用默认值
                default_value = ""
                if ':' in env_var:
                    env_var, default_value = env_var.split(':', 1)
                return os.getenv(env_var, default_value)
            return obj
        
        replace_env_vars(config)
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "default_model": "qwen-max",
            "models": {
                "qwen-max": {
                    "model_class": "DashScopeChatModel",
                    "config_name": "qwen-max",
                    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
                    "model": "qwen-max",
                    "generate_config": {
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                },
                "qwen3-max": {
                    "model_class": "DashScopeChatModel",
                    "config_name": "qwen3-max",
                    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
                    "model": "qwen3-max",
                    "generate_config": {
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                },
                "deepseek-v3": {
                    "model_class": "DashScopeChatModel",
                    "config_name": "deepseek-v3",
                    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
                    "model": "deepseek-v3",
                    "generate_config": {
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                },
                "deepseek-v3.2-exp": {
                    "model_class": "DashScopeChatModel",
                    "config_name": "deepseek-v3.2-exp",
                    "api_key": os.getenv("DASHSCOPE_API_KEY", ""),
                    "model": "deepseek-v3.2-exp",
                    "generate_config": {
                        "temperature": 0.7,
                        "max_tokens": 2048
                    }
                }
            }
        }
    
    def get_model_config(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        获取指定模型的配置
        
        Args:
            model_name: 模型名称，如果为None则使用默认模型
            
        Returns:
            模型配置字典
        """
        if model_name is None:
            model_name = self.config.get("default_model", "dashscope")
        
        models = self.config.get("models", {})
        if model_name not in models:
            raise ValueError(f"不支持的模型: {model_name}")
        
        return models[model_name]
    
    def create_model(self, model_name: Optional[str] = None) -> ChatModelBase:
        """
        创建DashScope模型实例
        
        Args:
            model_name: 模型名称，如果为None则使用默认模型
            
        Returns:
            DashScope模型实例
        """
        model_config = self.get_model_config(model_name)
        model_class_name = model_config.get("model_class")
        
        # 仅支持DashScope模型
        if model_class_name != "DashScopeChatModel":
            raise ValueError(f"仅支持DashScope模型，不支持的模型类: {model_class_name}")
        
        # 创建DashScope模型
        generate_config = model_config.get("generate_config", {})
        model = DashScopeChatModel(
            model_name=model_config.get("model", "qwen-max"),
            api_key=model_config.get("api_key", ""),
            generate_kwargs=generate_config
        )
        
        self.current_model = model
        self.model_type = model_name
        
        return model
    
    def get_current_model(self) -> Optional[ChatModelBase]:
        """获取当前模型实例"""
        return self.current_model
    
    def get_current_model_type(self) -> Optional[str]:
        """获取当前模型类型"""
        return self.model_type
    
    def set_default_model(self, model_name: str) -> None:
        """
        设置默认模型
        
        Args:
            model_name: 模型名称
        """
        models = self.config.get("models", {})
        if model_name not in models:
            raise ValueError(f"不支持的模型: {model_name}")
        
        self.config["default_model"] = model_name
        self._save_config()
    
    def _save_config(self) -> None:
        """保存配置到文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def list_available_models(self) -> list:
        """列出所有可用的模型"""
        return list(self.config.get("models", {}).keys())
    
    def update_model_config(self, model_name: str, config: Dict[str, Any]) -> None:
        """
        更新模型配置
        
        Args:
            model_name: 模型名称
            config: 新的配置
        """
        models = self.config.get("models", {})
        if model_name not in models:
            raise ValueError(f"不支持的模型: {model_name}")
        
        models[model_name].update(config)
        self.config["models"] = models
        self._save_config()


# 全局模型配置实例
model_config = ModelConfig()


def get_model(model_name: Optional[str] = None) -> ChatModelBase:
    """
    获取模型实例的便捷函数
    
    Args:
        model_name: 模型名称，如果为None则使用默认模型
        
    Returns:
        模型实例
    """
    return model_config.create_model(model_name)


def get_current_model() -> Optional[ChatModelBase]:
    """获取当前模型实例的便捷函数"""
    return model_config.get_current_model()


def get_current_model_type() -> Optional[str]:
    """获取当前模型类型的便捷函数"""
    return model_config.model_type


def set_default_model(model_name: str) -> None:
    """
    设置默认模型的便捷函数
    
    Args:
        model_name: 模型名称
    """
    model_config.set_default_model(model_name)


def list_available_models() -> list:
    """列出所有可用模型的便捷函数"""
    return model_config.list_available_models()


def update_model_config(model_name: str, config: Dict[str, Any]) -> None:
    """
    更新模型配置的便捷函数
    
    Args:
        model_name: 模型名称
        config: 新的配置
    """
    model_config.update_model_config(model_name, config)


# ==================== 新的LLM客户端接口 ====================

def create_llm_client(
    provider: str = "dashscope",
    model_name: str = None,
    from_env: bool = True
) -> LLMClient:
    """创建LLM客户端（推荐使用）
    
    Args:
        provider: 提供商名称
        model_name: 模型名称
        from_env: 是否从环境变量读取配置
        
    Returns:
        配置好的LLMClient实例
        
    Example:
        # 从环境变量创建
        client = create_llm_client()
        
        # 指定模型
        client = create_llm_client(model_name="qwen3-max")
    """
    if from_env:
        config = EnhancedModelConfig.from_env(provider=provider, model_name=model_name)
    else:
        # 从YAML配置创建（待实现）
        raise NotImplementedError("从YAML创建LLM客户端尚未实现")
    
    return config.to_llm_client()


def get_enhanced_config(
    provider: str = "dashscope",
    model_name: str = None
) -> EnhancedModelConfig:
    """获取增强的模型配置
    
    Args:
        provider: 提供商名称
        model_name: 模型名称
        
    Returns:
        EnhancedModelConfig实例
    """
    return EnhancedModelConfig.from_env(provider=provider, model_name=model_name)
