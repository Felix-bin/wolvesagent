#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""基础功能测试 - 验证重构后的PlayerAgent"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agentscope.message import Msg
from agent import PlayerAgent


async def test_basic_initialization():
    """测试基础初始化"""
    print("=" * 60)
    print("测试1: 基础初始化")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        print(f"[OK] 智能体创建成功: {agent.name}")
        
        # 验证核心组件
        assert agent.message_handler is not None, "消息处理器未初始化"
        assert agent.strategy_manager is not None, "策略管理器未初始化"
        assert agent.memory_manager is not None, "记忆管理器未初始化"
        print("[OK] 所有核心组件已初始化")
        
        return True
    except Exception as e:
        print(f"[FAIL] 初始化失败: {e}")
        return False


async def test_observe_function():
    """测试observe函数"""
    print("\n" + "=" * 60)
    print("测试2: observe函数")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        
        # 测试角色分配消息
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is werewolf.",
            role="system"
        )
        
        await agent.observe(role_msg)
        
        # 验证角色设置
        role = agent.message_handler.get_current_role()
        assert role == "werewolf", f"角色设置失败，期望werewolf，得到{role}"
        print(f"[OK] 角色分配成功: {role}")
        
        # 验证策略切换
        assert agent.strategy_manager.get_current_role() == "werewolf", "策略未切换"
        print("[OK] 策略管理器已切换到对应角色")
        
        return True
    except Exception as e:
        print(f"[FAIL] observe函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_state_persistence():
    """测试状态持久化"""
    print("\n" + "=" * 60)
    print("测试3: 状态持久化")
    print("=" * 60)
    
    try:
        # 创建第一个智能体并设置状态
        agent1 = PlayerAgent(name="TestPlayer1")
        
        # 模拟游戏状态
        role_msg = Msg(
            name="Moderator",
            content="[TestPlayer1 ONLY] TestPlayer1, your role is seer.",
            role="system"
        )
        await agent1.observe(role_msg)
        
        # 保存状态
        state = agent1.state_dict()
        print(f"[OK] 状态已保存，包含 {len(state)} 个字段")
        
        # 创建新智能体并加载状态
        agent2 = PlayerAgent(name="TestPlayer1")
        agent2.load_state_dict(state)
        
        # 验证状态恢复
        assert agent2.name == "TestPlayer1", "名称未恢复"
        print("[OK] 状态成功恢复")
        
        return True
    except Exception as e:
        print(f"[FAIL] 状态持久化测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_message_handling():
    """测试消息处理"""
    print("\n" + "=" * 60)
    print("测试4: 消息处理")
    print("=" * 60)
    
    try:
        agent = PlayerAgent(name="TestPlayer1")
        
        # 测试多种消息格式
        messages = [
            Msg(name="Moderator", content="Night has fallen.", role="system"),
            Msg(name="Player2", content="I think Player3 is suspicious.", role="user"),
            "Simple string message"
        ]
        
        for msg in messages:
            await agent.observe(msg)
        
        print("[OK] 各种消息格式处理成功")
        
        # 验证记忆系统
        recent_conversations = agent.memory_manager.get_recent_conversations(5)
        assert len(recent_conversations) > 0, "对话未记录"
        print(f"[OK] 记录了 {len(recent_conversations)} 条对话")
        
        return True
    except Exception as e:
        print(f"[FAIL] 消息处理测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_call_function_timeout():
    """测试__call__函数的时间限制"""
    print("\n" + "=" * 60)
    print("测试5: __call__函数时间和字符限制")
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
        
        # 测试普通调用
        test_msg = Msg(
            name="Moderator",
            content="Please introduce yourself.",
            role="user"
        )
        
        response = await agent(test_msg)
        
        # 验证响应
        assert response is not None, "响应为空"
        assert isinstance(response, Msg), "响应类型错误"
        assert len(response.content) <= 2048, f"响应超长: {len(response.content)}字符"
        
        print(f"[OK] __call__函数正常工作")
        print(f"[OK] 响应长度: {len(response.content)} 字符（限制: 2048）")
        
        return True
    except Exception as e:
        print(f"[FAIL] __call__函数测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """运行所有测试"""
    print("\n[TEST] 开始基础功能测试\n")
    
    tests = [
        ("基础初始化", test_basic_initialization),
        ("observe函数", test_observe_function),
        ("状态持久化", test_state_persistence),
        ("消息处理", test_message_handling),
        ("__call__函数限制", test_call_function_timeout),
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

