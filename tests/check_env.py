# -*- coding: utf-8 -*-
"""
环境配置检查脚本
"""

import os
import sys
from pathlib import Path

# 设置Windows控制台UTF-8编码
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    # 重新配置stdout和stderr
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境变量
from dotenv import load_dotenv
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)

def check_environment():
    """检查环境配置"""
    print("="*70)
    print("  环境配置检查")
    print("="*70)
    print()
    
    # 检查.env文件
    print("[1] .env文件检查")
    if env_path.exists():
        print(f"    [OK] 找到.env文件: {env_path}")
    else:
        print(f"    [NO] 未找到.env文件: {env_path}")
        print(f"    --> 请从.env.example创建.env文件")
    print()
    
    # 检查API密钥
    print("[2] API密钥检查")
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        if len(api_key) > 16:
            masked = f"{api_key[:8]}...{api_key[-8:]}"
        else:
            masked = "***"
        print(f"    [OK] DASHSCOPE_API_KEY: {masked}")
    else:
        print(f"    [NO] 未找到DASHSCOPE_API_KEY")
        print(f"    --> 请在.env文件中设置API密钥")
    print()
    
    # 检查模型配置
    print("[3] 模型配置检查")
    model_name = os.getenv("DASHSCOPE_MODEL_NAME", "qwen-max")
    temperature = os.getenv("MODEL_TEMPERATURE", "0.7")
    max_tokens = os.getenv("MODEL_MAX_TOKENS", "2048")
    print(f"    • 模型名称: {model_name}")
    print(f"    • 温度参数: {temperature}")
    print(f"    • 最大令牌: {max_tokens}")
    print()
    
    # 检查依赖
    print("[4] 依赖包检查")
    required_packages = [
        ('agentscope', 'AgentScope框架'),
        ('dashscope', 'DashScope SDK'),
        ('pydantic', 'Pydantic数据验证'),
        ('yaml', 'PyYAML配置解析'),
        ('dotenv', 'python-dotenv环境变量'),
    ]
    
    all_ok = True
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"    [OK] {description} ({package})")
        except ImportError:
            print(f"    [NO] {description} ({package}) - 未安装")
            all_ok = False
    print()
    
    # 检查项目文件
    print("[5] 项目文件检查")
    required_files = [
        'agent.py',
        'agents/player_agent.py',
        'config/model_config.yaml',
        'werewolves/game.py',
        'werewolves/main.py',
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"    [OK] {file_path}")
        else:
            print(f"    [NO] {file_path} - 未找到")
            all_ok = False
    print()
    
    # 总结
    print("="*70)
    if all_ok and api_key:
        print("  [OK] 环境配置完整，可以开始测试")
    else:
        print("  [NO] 环境配置不完整，请检查上述问题")
    print("="*70)
    print()
    
    return all_ok and api_key

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)

