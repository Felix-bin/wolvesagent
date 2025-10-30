#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""策略系统集成测试"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agentscope.message import Msg
from agent import PlayerAgent


async def test_strategy_switching():
    """测试策略自动切换"""
    print("=" * 60)
    print("测试: 策略自动切换")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        
        # 测试狼人角色
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is werewolf.",
            role="system"
        )
        await agent.observe(role_msg)
        
        # 验证策略切换
        assert agent.strategy_manager.get_current_role() == "werewolf"
        strategy = agent.strategy_manager.get_current_strategy()
        assert strategy is not None
        assert strategy.get_role_name() == "werewolf"
        print("[OK] 狼人策略已激活")
        
        # 测试先知角色
        role_msg2 = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is seer.",
            role="system"
        )
        await agent.observe(role_msg2)
        
        assert agent.strategy_manager.get_current_role() == "seer"
        strategy2 = agent.strategy_manager.get_current_strategy()
        assert strategy2.get_role_name() == "seer"
        print("[OK] 先知策略已激活")
        
        return True
    except Exception as e:
        print(f"[FAIL] 策略切换测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_intelligent_response():
    """测试智能响应生成"""
    print("\n" + "=" * 60)
    print("测试: 智能响应生成")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        
        # 设置角色
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is villager.",
            role="system"
        )
        await agent.observe(role_msg)
        
        # 测试普通发言
        test_msg = Msg(
            name="Moderator",
            content="Please discuss your thoughts.",
            role="user"
        )
        
        response = await agent(test_msg)
        
        assert response is not None
        assert isinstance(response, Msg)
        assert len(response.content) > 0
        print(f"[OK] 生成响应: {response.content[:50]}...")
        
        return True
    except Exception as e:
        print(f"[FAIL] 智能响应测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_voting_decision():
    """测试投票决策"""
    print("\n" + "=" * 60)
    print("测试: 投票决策")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        
        # 设置角色
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is werewolf.",
            role="system"
        )
        await agent.observe(role_msg)
        
        # 模拟投票请求（需要结构化模型）
        # 注意：这里需要导入实际的结构化模型
        vote_msg = Msg(
            name="Moderator",
            content="Please vote for a player to eliminate.",
            role="user"
        )
        
        # 不使用structured_model时的测试
        response = await agent(vote_msg)
        
        assert response is not None
        print(f"[OK] 投票响应生成: {response.content[:50]}...")
        
        return True
    except Exception as e:
        print(f"[FAIL] 投票决策测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_strategy_state_persistence():
    """测试策略状态持久化"""
    print("\n" + "=" * 60)
    print("测试: 策略状态持久化")
    print("=" * 60)
    
    try:
        # 创建第一个智能体
        agent1 = PlayerAgent(name="TestPlayer1")
        
        # 设置角色并进行一些操作
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is seer.",
            role="system"
        )
        await agent1.observe(role_msg)
        
        # 获取策略并更新一些状态
        strategy1 = agent1.strategy_manager.get_current_strategy()
        strategy1.update_trust_score("Player2", 0.3)
        strategy1.update_suspicion_level("Player3", 0.4)
        
        # 保存状态
        state = agent1.state_dict()
        
        # 创建新智能体并加载状态
        agent2 = PlayerAgent(name="TestPlayer1")
        agent2.load_state_dict(state)
        
        # 验证策略状态恢复
        strategy2 = agent2.strategy_manager.get_current_strategy()
        assert strategy2 is not None
        
        # 检查玩家信息是否恢复
        player2_info = strategy2.get_player_info("Player2")
        if player2_info:
            print(f"[OK] Player2信任度已恢复: {player2_info.trust_score}")
        
        print("[OK] 策略状态持久化成功")
        return True
    except Exception as e:
        print(f"[FAIL] 策略状态持久化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """运行所有测试"""
    print("\n[TEST] 策略系统集成测试\n")
    
    tests = [
        ("策略自动切换", test_strategy_switching),
        ("智能响应生成", test_intelligent_response),
        ("投票决策", test_voting_decision),
        ("策略状态持久化", test_strategy_state_persistence),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n[FAIL] 测试 '{test_name}' 发生异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    import os
    
    # 检查API密钥
    if not os.environ.get("DASHSCOPE_API_KEY"):
        print("[WARNING] 未设置DASHSCOPE_API_KEY环境变量")
        print("某些测试可能会失败")
        print()
    
    # 运行测试
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

