#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""狼人杀AI智能体比赛测试脚本

使用我们的智能体创建9个参赛者，运行官方比赛测试程序进行比赛
"""

import asyncio
import os
import sys
import time
from pathlib import Path

# 加载.env文件中的环境变量
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # 如果没有python-dotenv，手动读取.env文件
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载环境配置
from config.env_config import load_env_config
load_env_config()

# 导入我们的智能体
from agent import PlayerAgent

# 导入官方游戏模块
from werewolves.game import werewolves_game
from werewolves.utils import Players
from agentscope.session import JSONSession


def get_our_agents(name: str) -> PlayerAgent:
    """获取我们的智能体实例
    
    Args:
        name: 智能体名称
        
    Returns:
        PlayerAgent: 我们的智能体实例
    """
    return PlayerAgent(name=name)


async def run_single_game(player_names: list = None) -> None:
    """运行单场比赛
    
    Args:
        player_names: 玩家名称列表，如果为None则使用默认名称
    """
    print("=" * 60)
    print("🐺 狼人杀AI智能体比赛开始")
    print("=" * 60)
    
    # 准备9个玩家
    if player_names is None:
        player_names = [f"AI玩家{i+1}" for i in range(9)]
    
    print(f"参赛玩家: {', '.join(player_names)}")
    print()
    
    # 创建我们的智能体实例
    players = []
    for name in player_names:
        try:
            player = get_our_agents(name)
            players.append(player)
            print(f"✅ 成功创建智能体: {name}")
        except Exception as e:
            print(f"❌ 创建智能体失败 {name}: {e}")
            return
    
    print(f"\n🎮 所有{len(players)}个智能体创建完成，开始比赛...")
    print("-" * 60)
    
    # 记录开始时间
    start_time = time.time()
    
    try:
        # 运行游戏
        await werewolves_game(players)
        
        # 记录结束时间
        end_time = time.time()
        game_duration = end_time - start_time
        
        print("-" * 60)
        print(f"⏱️  比赛结束，耗时: {game_duration:.2f}秒")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 比赛过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


async def run_multiple_games(num_games: int = 1) -> None:
    """运行多场比赛
    
    Args:
        num_games: 比赛场次
    """
    print(f"🎯 开始运行{num_games}场比赛...")
    
    # 创建会话管理器，用于保存和加载智能体状态
    session = JSONSession(save_dir="./checkpoints")
    
    for game_num in range(1, num_games + 1):
        print(f"\n📋 第{game_num}/{num_games}场比赛")
        
        # 玩家名称
        player_names = [f"AI玩家{i+1}" for i in range(9)]
        
        try:
            # 如果不是第一场，尝试加载之前的状态
            if game_num > 1:
                print("🔄 加载上一场比赛的智能体状态...")
                players = []
                for name in player_names:
                    player = get_our_agents(name)
                    players.append(player)
                
                # 尝试加载状态
                try:
                    await session.load_session_state(
                        session_id="players_checkpoint",
                        **{player.name: player for player in players},
                    )
                    print("✅ 智能体状态加载成功")
                except Exception as e:
                    print(f"⚠️  智能体状态加载失败，使用初始状态: {e}")
            else:
                # 第一场比赛，创建新的智能体
                players = []
                for name in player_names:
                    player = get_our_agents(name)
                    players.append(player)
            
            # 运行比赛
            await werewolves_game(players)
            
            # 保存智能体状态
            await session.save_session_state(
                session_id="players_checkpoint",
                **{player.name: player for player in players},
            )
            print("💾 智能体状态已保存")
            
        except Exception as e:
            print(f"❌ 第{game_num}场比赛失败: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n🏁 所有{num_games}场比赛完成!")


def check_environment() -> bool:
    """检查环境配置
    
    Returns:
        bool: 环境是否配置正确
    """
    print("🔍 检查环境配置...")
    
    # 检查API密钥
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置DASHSCOPE_API_KEY环境变量")
        print("请设置环境变量: export DASHSCOPE_API_KEY=your_api_key")
        return False
    
    print("✅ DASHSCOPE_API_KEY已设置")
    
    # 检查必要的文件
    required_files = [
        "agent.py",
        "agents/player_agent.py", 
        "werewolves/game.py",
        "werewolves/main.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"❌ 错误: 缺少必要文件 {file_path}")
            return False
    
    print("✅ 所有必要文件存在")
    
    # 检查依赖
    try:
        import agentscope
        print("✅ AgentScope已安装")
    except ImportError:
        print("❌ 错误: AgentScope未安装")
        print("请安装: pip install agentscope")
        return False
    
    return True


async def main():
    """主函数"""
    # 设置控制台编码为UTF-8（Windows兼容）
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("🐺 狼人杀AI智能体比赛测试程序")
    print("=" * 60)
    
    # 检查环境
    if not check_environment():
        print("\n❌ 环境检查失败，请修复后重试")
        return
    
    print("\n🎮 选择比赛模式:")
    print("1. 运行单场比赛")
    print("2. 运行多场比赛 (连续5局，模拟真实比赛)")
    print("3. 运行完整轮次 (10轮 x 5局 = 50局)")
    
    try:
        choice = input("\n请输入选择 (1-3): ").strip()
        
        if choice == "1":
            await run_single_game()
        elif choice == "2":
            await run_multiple_games(5)
        elif choice == "3":
            await run_multiple_games(50)
        else:
            print("❌ 无效选择，运行单场比赛")
            await run_single_game()
            
    except KeyboardInterrupt:
        print("\n\n⏹️  比赛被用户中断")
    except Exception as e:
        print(f"\n❌ 程序运行错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 设置事件循环策略 (Windows兼容性)
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
