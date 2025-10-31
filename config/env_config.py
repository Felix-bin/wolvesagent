#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""环境配置加载模块"""

import os


def load_env_config():
    """加载环境配置
    
    注意：请通过.env文件或系统环境变量设置DASHSCOPE_API_KEY
    不要在代码中硬编码API密钥
    """
    # 设置默认模型配置（不包含API密钥）
    os.environ.setdefault("DASHSCOPE_MODEL_NAME", "glm-4.5-air")
    
    # 设置模型参数
    os.environ.setdefault("MODEL_TEMPERATURE", "0.7")
    os.environ.setdefault("MODEL_MAX_TOKENS", "2048")


# 自动加载
load_env_config()

