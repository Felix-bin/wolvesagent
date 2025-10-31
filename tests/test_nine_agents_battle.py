# -*- coding: utf-8 -*-
"""
9个智能体官方比赛测试脚本
专为Windows系统优化，处理中文编码问题
"""

import asyncio
import os
import sys
from pathlib import Path

# 设置Windows控制台为UTF-8编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    # 设置控制台代码页为UTF-8
    os.system('chcp 65001 > nul')

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
# 不添加werewolves目录，避免与utils包冲突

# 加载环境变量
from dotenv import load_dotenv
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)
    print(f"[✓] 已从 {env_path} 加载环境变量")
else:
    print(f"[!] 警告: 未找到.env文件: {env_path}")

# 导入必要的模块
from agent import PlayerAgent
from werewolves.game import werewolves_game
from agentscope.session import JSONSession


async def test_nine_agents_battle():
    """测试9个智能体之间的比赛"""
    print("\n" + "="*70)
    print("  狼人杀智能体官方比赛测试")
    print("  使用9个PlayerAgent进行完整比赛")
    print("="*70 + "\n")
    
    # 检查API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("[✗] 错误: 未找到DASHSCOPE_API_KEY环境变量")
        print("    请确保.env文件中包含有效的API密钥")
        return
    else:
        # 显示API密钥的前后几位
        masked_key = f"{api_key[:8]}...{api_key[-8:]}" if len(api_key) > 16 else "***"
        print(f"[✓] 已加载API密钥: {masked_key}\n")
    
    try:
        # 创建9个智能体
        print("[1/4] 正在创建9个智能体...")
        players = []
        for i in range(9):
            player_name = f"Player{i+1}"
            print(f"  • 创建智能体: {player_name}")
            player = PlayerAgent(name=player_name)
            players.append(player)
        print(f"[✓] 成功创建 {len(players)} 个智能体\n")
        
        # 创建会话管理器（用于跨局保存状态）
        print("[2/4] 初始化会话管理器...")
        checkpoint_dir = project_root / "tests" / "test_checkpoints"
        checkpoint_dir.mkdir(exist_ok=True, parents=True)
        session = JSONSession(save_dir=str(checkpoint_dir))
        print(f"[✓] 检查点目录: {checkpoint_dir}\n")
        
        # 尝试加载之前的会话状态（如果存在）
        print("[3/4] 检查历史会话...")
        try:
            await session.load_session_state(
                session_id="nine_agents_battle",
                **{player.name: player for player in players}
            )
            print("[✓] 已加载历史会话状态\n")
        except Exception as e:
            print(f"[i] 未找到历史会话，将开始新游戏\n")
        
        # 开始游戏
        print("[4/4] 开始狼人杀比赛...")
        print("-" * 70)
        print("游戏进行中，请耐心等待...\n")
        
        await werewolves_game(players)
        
        print("\n" + "-" * 70)
        print("[✓] 游戏结束！")
        
        # 保存会话状态
        print("\n[*] 正在保存会话状态...")
        await session.save_session_state(
            session_id="nine_agents_battle",
            **{player.name: player for player in players}
        )
        print("[✓] 会话状态已保存\n")
        
        # 显示统计信息
        print("="*70)
        print("  游戏统计")
        print("="*70)
        for player in players:
            state = player.state_dict()
            games_played = state.get('games_played', 0)
            print(f"  {player.name}: 已参与 {games_played} 局游戏")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n[!] 用户中断游戏")
        return
    except Exception as e:
        print(f"\n[✗] 游戏出错: {e}")
        import traceback
        traceback.print_exc()
        return


async def main():
    """主函数"""
    await test_nine_agents_battle()


if __name__ == "__main__":
    # 确保Windows控制台正确显示中文
    if sys.platform == 'win32':
        import locale
        print(f"系统默认编码: {locale.getpreferredencoding()}\n")
    
    # 运行测试
    asyncio.run(main())

