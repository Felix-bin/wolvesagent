import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelProviderConfig:
    """模型提供商配置"""
    
    provider: str  # 例如: "dashscope", "openai", "anthropic"
    api_key: str
    base_url: str | None = None
    api_version: str | None = None


@dataclass
class ModelConfig:
    """LLM 模型配置"""
    
    model_name: str  # 例如: "qwen3-max", "gpt-4o"
    model_provider: ModelProviderConfig
    
    # 从配置读取的模型参数
    temperature: float = 0.7
    max_tokens: int | None = None
    top_p: float | None = None
    stream: bool = True
    
    # 高级参数
    enable_thinking: bool | None = None  # 用于 DeepSeek-R1, QwQ 等模型
    supports_tool_calling: bool = True
    
    # 额外的生成参数
    generate_kwargs: dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_env(cls, provider: str = "dashscope") -> "ModelConfig":
        """从环境变量创建 ModelConfig
        
        Args:
            provider: 模型提供商名称
            
        Returns:
            ModelConfig 实例
            
        Raises:
            ValueError: 当缺少必需的环境变量时抛出
        """
        # 从环境变量读取
        if provider == "dashscope":
            api_key = os.getenv("DASHSCOPE_API_KEY")
            model_name = os.getenv("DASHSCOPE_MODEL_NAME", "qwen3-max")
            base_url = os.getenv("DASHSCOPE_BASE_URL")
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
            base_url = os.getenv("OPENAI_BASE_URL")
        elif provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            model_name = os.getenv("ANTHROPIC_MODEL_NAME", "claude-3-5-sonnet-20241022")
            base_url = os.getenv("ANTHROPIC_BASE_URL")
        else:
            raise ValueError(f"不支持的提供商: {provider}")
            
        if not api_key:
            raise ValueError(f"未找到提供商 {provider} 的 API key")
        
        # 从环境变量读取模型参数或使用默认值
        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.7"))
        max_tokens = int(os.getenv("MODEL_MAX_TOKENS")) if os.getenv("MODEL_MAX_TOKENS") else None
        top_p = float(os.getenv("MODEL_TOP_P")) if os.getenv("MODEL_TOP_P") else None
        stream = os.getenv("MODEL_STREAM", "true").lower() == "true"
        enable_thinking = os.getenv("MODEL_ENABLE_THINKING", "").lower() == "true" if os.getenv("MODEL_ENABLE_THINKING") else None
        
        model_provider = ModelProviderConfig(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
        )
        
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
            model_provider=model_provider,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream,
            enable_thinking=enable_thinking,
            generate_kwargs=generate_kwargs,
        )