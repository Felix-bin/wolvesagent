#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""环境配置加载模块"""

import os
from dotenv import load_dotenv


def load_env_config():
    """加载环境配置
    
    从.env文件或系统环境变量加载配置
    """
    # 尝试加载.env文件
    load_dotenv()
    
    # 设置默认模型配置（不包含API密钥）
    os.environ.setdefault("DASHSCOPE_MODEL_NAME", "glm-4.5-air")
    
    # 设置模型参数
    os.environ.setdefault("MODEL_TEMPERATURE", "0.7")
    os.environ.setdefault("MODEL_MAX_TOKENS", "2048")


# 自动加载
load_env_config()

