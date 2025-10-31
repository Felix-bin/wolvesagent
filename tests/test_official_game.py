#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""官方比赛测试程序集成测试 - 使用9个PlayerAgent进行完整游戏"""

import asyncio
import sys
import os
from pathlib import Path

# 在导入任何项目模块之前，先设置默认环境变量（如果环境中未设置）
# 注意：请通过.env文件或系统环境变量设置DASHSCOPE_API_KEY
# 不要在代码中硬编码API密钥
os.environ.setdefault('DASHSCOPE_MODEL_NAME', 'glm-4.5-air')
os.environ.setdefault('MODEL_TEMPERATURE', '0.7')
os.environ.setdefault('MODEL_MAX_TOKENS', '2048')

# 添加项目根目录到路径（注意：项目路径必须优先）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# werewolves目录加到后面，避免覆盖项目的utils包
werewolves_dir = project_root / "werewolves"
sys.path.append(str(werewolves_dir))

# 加载.env文件
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    if env_path.exists():
        # 强制覆盖加载环境变量
        load_dotenv(env_path, override=True)
        print(f"[INFO] 已从 {env_path} 加载环境变量")
        api_key = os.environ.get('DASHSCOPE_API_KEY')
        if api_key:
            print(f"[INFO] DASHSCOPE_API_KEY: {api_key[:10]}... (已设置)")
        else:
            print(f"[WARNING] DASHSCOPE_API_KEY: 未设置")
            # 手动从文件读取并设置
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print(f"[INFO] 已手动加载环境变量")
            api_key = os.environ.get('DASHSCOPE_API_KEY')
            if api_key:
                print(f"[INFO] DASHSCOPE_API_KEY: {api_key[:10]}... (手动设置成功)")
except ImportError:
    print("[WARNING] python-dotenv未安装")

from agent import PlayerAgent
from game import werewolves_game
from agentscope.session import JSONSession


async def test_official_game_with_9_agents():
    """使用9个PlayerAgent进行完整的官方游戏测试"""
    print("\n" + "=" * 80)
    print("官方比赛测试程序集成测试")
    print("使用9个PlayerAgent智能体进行完整游戏")
    print("=" * 80 + "\n")
    
    try:
        # 创建9个PlayerAgent
        print("[1/5] 创建9个PlayerAgent智能体...")
        players = [PlayerAgent(name=f"Player{i+1}") for i in range(9)]
        print(f"[OK] 成功创建 {len(players)} 个智能体")
        for player in players:
            print(f"  - {player.name}")
        
        # 检查智能体是否正确初始化
        print("\n[2/5] 验证智能体初始化...")
        for player in players:
            assert hasattr(player, 'observe'), f"{player.name} 缺少 observe 方法"
            assert hasattr(player, '__call__'), f"{player.name} 缺少 __call__ 方法"
            assert hasattr(player, 'state_dict'), f"{player.name} 缺少 state_dict 方法"
            assert hasattr(player, 'load_state_dict'), f"{player.name} 缺少 load_state_dict 方法"
        print("[OK] 所有智能体已正确初始化")
        
        # 准备session（用于状态持久化）
        print("\n[3/5] 准备Session...")
        checkpoint_dir = project_root / "tests" / "test_checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)
        session = JSONSession(save_dir=str(checkpoint_dir))
        
        # 尝试加载之前的状态（如果存在）
        try:
            await session.load_session_state(
                session_id="test_players_checkpoint",
                **{player.name: player for player in players},
            )
            print("[OK] 已加载之前的检查点")
        except Exception as e:
            print(f"[INFO] 未找到之前的检查点，将从头开始: {e}")
        
        # 运行游戏
        print("\n[4/5] 开始游戏...")
        print("-" * 80)
        
        await werewolves_game(players)
        
        print("-" * 80)
        print("[OK] 游戏结束")
        
        # 保存状态
        print("\n[5/5] 保存状态...")
        await session.save_session_state(
            session_id="test_players_checkpoint",
            **{player.name: player for player in players},
        )
        print("[OK] 状态已保存")
        
        # 测试完成
        print("\n" + "=" * 80)
        print("测试成功完成！")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n[FAIL] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    # 检查API密钥
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("\n[ERROR] 未设置DASHSCOPE_API_KEY环境变量")
        print("请在.env文件中设置API密钥")
        return False
    
    print(f"[INFO] 使用API密钥: {api_key[:10]}...")
    print(f"[INFO] 使用模型: {os.environ.get('DASHSCOPE_MODEL_NAME', 'glm-4.5-air')}")
    
    # 运行测试
    success = await test_official_game_with_9_agents()
    
    return success


if __name__ == "__main__":
    # Windows兼容性设置
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 运行测试
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

