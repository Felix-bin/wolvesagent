# -*- coding: utf-8 -*-
"""全面测试策略系统集成 - 验证各角色决策逻辑"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from agentscope.message import Msg
from agents.player_agent import PlayerAgent

# 测试配置
TEST_AGENT_NAME = "Player1"
OTHER_PLAYERS = ["Player2", "Player3", "Player4", "Player5", "Player6"]


def print_test_header(test_name):
    """打印测试头部"""
    print("\n" + "=" * 60)
    print(f"测试: {test_name}")
    print("=" * 60)


def print_test_result(test_name, passed, details=""):
    """打印测试结果"""
    status = "[通过]" if passed else "[失败]"
    print(f"{status} {test_name}")
    if details:
        print(f"   详情: {details}")


async def test_werewolf_night_action():
    """测试狼人夜晚行动"""
    print_test_header("狼人夜晚击杀决策")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 模拟分配狼人角色
    role_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是狼人。",
        role="system"
    )
    await agent.observe(role_msg)
    
    # 模拟夜晚阶段
    night_msg = Msg(
        name="Moderator",
        content=f"现在是夜晚，狼人请讨论并选择击杀目标。存活玩家: {', '.join(OTHER_PLAYERS)}",
        role="system"
    )
    await agent.observe(night_msg)
    
    # 测试狼人讨论决策
    from models.structured_models import WerewolfKillModel
    response = await agent(night_msg, structured_model=WerewolfKillModel)
    
    has_target = response.metadata and 'name' in response.metadata
    print_test_result(
        "狼人击杀决策",
        has_target,
        f"目标: {response.metadata.get('name') if has_target else '无'}"
    )
    
    return has_target


async def test_seer_check():
    """测试先知查验"""
    print_test_header("先知查验决策")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 分配先知角色
    role_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是先知。",
        role="system"
    )
    await agent.observe(role_msg)
    
    # 模拟夜晚查验
    night_msg = Msg(
        name="Moderator",
        content=f"先知请选择查验目标。存活玩家: {', '.join(OTHER_PLAYERS)}",
        role="system"
    )
    await agent.observe(night_msg)
    
    # 测试查验决策
    from models.structured_models import SeerModel
    response = await agent(night_msg, structured_model=SeerModel)
    
    has_target = response.metadata and 'name' in response.metadata
    target = response.metadata.get('name') if has_target else None
    has_reasoning = response.metadata and 'reasoning_chain' in response.metadata
    
    print_test_result(
        "先知查验决策",
        has_target,
        f"目标: {target}, 带推理链: {has_reasoning}"
    )
    
    return has_target


async def test_witch_actions():
    """测试女巫用药"""
    print_test_header("女巫用药决策")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 分配女巫角色
    role_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是女巫。",
        role="system"
    )
    await agent.observe(role_msg)
    
    # 测试1: 救人决策
    killed_msg = Msg(
        name="Moderator",
        content=f"昨晚Player2被狼人杀害。你是否使用解药？",
        role="system"
    )
    await agent.observe(killed_msg)
    
    from models.structured_models import WitchResurrectModel
    response1 = await agent(killed_msg, structured_model=WitchResurrectModel)
    
    has_resurrect_decision = response1.metadata and 'resurrect' in response1.metadata
    resurrect = response1.metadata.get('resurrect', False) if has_resurrect_decision else False
    
    print_test_result(
        "女巫救人决策",
        has_resurrect_decision,
        f"决定: {'救' if resurrect else '不救'}"
    )
    
    # 测试2: 毒人决策
    poison_msg = Msg(
        name="Moderator",
        content=f"你是否使用毒药？存活玩家: {', '.join(OTHER_PLAYERS)}",
        role="system"
    )
    
    from models.structured_models import WitchPoisonModel
    response2 = await agent(poison_msg, structured_model=WitchPoisonModel)
    
    has_poison_decision = response2.metadata and 'poison' in response2.metadata
    poison = response2.metadata.get('poison', False) if has_poison_decision else False
    target = response2.metadata.get('name') if poison else None
    
    print_test_result(
        "女巫毒人决策",
        has_poison_decision,
        f"决定: {'毒' if poison else '不毒'}, 目标: {target if target else '无'}"
    )
    
    return has_resurrect_decision and has_poison_decision


async def test_hunter_shoot():
    """测试猎人开枪"""
    print_test_header("猎人开枪决策")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 分配猎人角色
    role_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是猎人。",
        role="system"
    )
    await agent.observe(role_msg)
    
    # 模拟猎人被淘汰
    death_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}被投票出局。你是否要开枪？存活玩家: {', '.join(OTHER_PLAYERS)}",
        role="system"
    )
    await agent.observe(death_msg)
    
    from models.structured_models import HunterModel
    response = await agent(death_msg, structured_model=HunterModel)
    
    has_shoot_decision = response.metadata and 'shoot' in response.metadata
    shoot = response.metadata.get('shoot', False) if has_shoot_decision else False
    target = response.metadata.get('name') if shoot else None
    
    print_test_result(
        "猎人开枪决策",
        has_shoot_decision,
        f"决定: {'开枪' if shoot else '不开枪'}, 目标: {target if target else '无'}"
    )
    
    return has_shoot_decision


async def test_voting_with_cot():
    """测试带思维链的投票决策"""
    print_test_header("投票决策（带思维链）")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 分配村民角色
    role_msg = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是村民。",
        role="system"
    )
    await agent.observe(role_msg)
    
    # 模拟白天投票
    vote_msg = Msg(
        name="Moderator",
        content=f"现在进入投票环节。存活玩家: {', '.join(OTHER_PLAYERS)}",
        role="system"
    )
    await agent.observe(vote_msg)
    
    from models.structured_models import VoteModel
    response = await agent(vote_msg, structured_model=VoteModel)
    
    has_vote = response.metadata and 'vote' in response.metadata
    vote_target = response.metadata.get('vote') if has_vote else None
    has_reasoning_chain = response.metadata and 'reasoning_chain' in response.metadata
    
    # 检查推理链
    reasoning_details = ""
    if has_reasoning_chain:
        cot = response.metadata['reasoning_chain']
        step_count = len(cot.get('steps', []))
        reasoning_details = f"推理步骤数: {step_count}"
    
    print_test_result(
        "投票决策",
        has_vote and has_reasoning_chain,
        f"目标: {vote_target}, {reasoning_details}"
    )
    
    return has_vote and has_reasoning_chain


async def test_day_speech_with_cot():
    """测试带思维链的白天发言"""
    print_test_header("白天发言（带思维链）")
    
    test_results = []
    roles = ["werewolf", "seer", "villager", "witch", "hunter"]
    
    for role in roles:
        agent = PlayerAgent(name=TEST_AGENT_NAME)
        
        # 分配角色
        role_msg = Msg(
            name="Moderator",
            content=f"{TEST_AGENT_NAME}，你的角色是{role}。",
            role="system"
        )
        await agent.observe(role_msg)
        
        # 模拟白天发言
        speech_msg = Msg(
            name="Moderator",
            content=f"现在是白天发言阶段，请{TEST_AGENT_NAME}发言。",
            role="system"
        )
        await agent.observe(speech_msg)
        
        response = await agent(speech_msg)
        
        has_content = response.content and len(response.content) > 0
        has_reasoning = response.metadata and 'reasoning_chain' in response.metadata
        within_limit = len(response.content) <= 2048 if has_content else True
        
        result = has_content and has_reasoning and within_limit
        test_results.append(result)
        
        print_test_result(
            f"{role}发言",
            result,
            f"长度: {len(response.content) if has_content else 0}, 带推理链: {has_reasoning}"
        )
    
    return all(test_results)


async def test_cross_game_learning():
    """测试跨局学习"""
    print_test_header("跨局学习与状态持久化")
    
    agent = PlayerAgent(name=TEST_AGENT_NAME)
    
    # 第一局游戏
    role_msg1 = Msg(
        name="Moderator",
        content=f"{TEST_AGENT_NAME}，你的角色是狼人。",
        role="system"
    )
    await agent.observe(role_msg1)
    
    # 模拟一些游戏事件
    event_msg = Msg(
        name="Player2",
        content="我怀疑Player3是狼人",
        role="user"
    )
    await agent.observe(event_msg)
    
    # 保存状态
    state1 = agent.state_dict()
    has_state = state1 and len(state1) > 0
    has_memory = 'memory' in state1
    has_strategy = 'strategy_manager' in state1
    
    print_test_result(
        "状态保存",
        has_state and has_memory and has_strategy,
        f"包含记忆: {has_memory}, 包含策略: {has_strategy}"
    )
    
    # 创建新智能体并加载状态
    agent2 = PlayerAgent(name=TEST_AGENT_NAME)
    agent2.load_state_dict(state1)
    
    # 验证状态恢复
    state2 = agent2.state_dict()
    state_restored = state2.get('games_played') == state1.get('games_played')
    
    print_test_result(
        "状态恢复",
        state_restored,
        f"游戏局数: {state2.get('games_played', 0)}"
    )
    
    return has_state and state_restored


async def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("全面策略系统集成测试")
    print("=" * 60)
    
    tests = [
        ("狼人夜晚行动", test_werewolf_night_action),
        ("先知查验", test_seer_check),
        ("女巫用药", test_witch_actions),
        ("猎人开枪", test_hunter_shoot),
        ("投票决策（思维链）", test_voting_with_cot),
        ("白天发言（思维链）", test_day_speech_with_cot),
        ("跨局学习", test_cross_game_learning),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results.append((test_name, result, None))
        except Exception as e:
            print(f"\n错误: {test_name} - {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False, str(e)))
    
    # 汇总结果
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    
    passed = sum(1 for _, result, _ in results if result)
    total = len(results)
    
    for test_name, result, error in results:
        status = "通过" if result else "失败"
        print(f"{status:4s} | {test_name}")
        if error:
            print(f"        错误: {error}")
    
    print("-" * 60)
    print(f"总计: {passed}/{total} 测试通过 ({passed*100//total}%)")
    
    if passed == total:
        print("\n所有测试通过！策略系统集成成功。")
    else:
        print(f"\n警告: 有 {total - passed} 个测试失败。")
    
    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)

