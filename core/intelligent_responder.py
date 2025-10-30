# -*- coding: utf-8 -*-
"""智能响应器 - 集成策略系统的响应生成"""

import time
from typing import Optional, Dict, Any, List
from agentscope.message import Msg
from agentscope.model import ChatModelBase

from core.strategy_manager import StrategyManager
from core.message_handler import MessageHandler
from models.memory import MemoryManager
from models.reasoning import GameObservation, GamePhase
from models.chain_of_thought import ChainOfThought, ChainOfThoughtBuilder
from utils.logger import WerewolfLogger


class IntelligentResponder:
    """智能响应器 - 结合策略系统生成高质量响应"""
    
    def __init__(
        self,
        agent_name: str,
        model: ChatModelBase,
        strategy_manager: StrategyManager,
        message_handler: MessageHandler,
        memory_manager: MemoryManager
    ):
        self.agent_name = agent_name
        self.model = model
        self.strategy_manager = strategy_manager
        self.message_handler = message_handler
        self.memory_manager = memory_manager
        self.logger = WerewolfLogger(agent_name)
    
    async def generate_intelligent_response(
        self,
        msg: Msg,
        structured_model: Optional[type] = None
    ) -> Msg:
        """生成智能响应（基于策略）
        
        Args:
            msg: 输入消息
            structured_model: 结构化模型（如果需要）
            
        Returns:
            响应消息
        """
        try:
            # 获取当前策略
            if not self.strategy_manager.has_strategy():
                # 如果还没有角色，返回等待消息
                return Msg(
                    name=self.agent_name,
                    content="等待角色分配。",
                    role="assistant"
                )
            
            strategy = self.strategy_manager.get_current_strategy()
            current_role = self.strategy_manager.get_current_role()
            
            # 构建游戏观察
            observation = self._build_observation()
            
            # 如果有结构化模型，说明是特定行动
            if structured_model:
                return await self._generate_structured_action(
                    msg,
                    structured_model,
                    strategy,
                    observation
                )
            else:
                # 普通发言
                return await self._generate_normal_speech(
                    msg,
                    strategy,
                    observation
                )
                
        except Exception as e:
            self.logger.error(f"智能响应生成失败: {e}")
            import traceback
            traceback.print_exc()
            return Msg(
                name=self.agent_name,
                content="思考中遇到问题，暂时保留意见。",
                role="assistant"
            )
    
    def _build_observation(self) -> GameObservation:
        """构建当前游戏观察"""
        game_state = self.message_handler.get_game_state()
        
        # 获取存活和死亡玩家
        alive_players = game_state.get('alive_players', [])
        dead_players = game_state.get('dead_players', [])
        
        # 确定当前阶段
        phase_str = game_state.get('phase', 'unknown')
        phase_map = {
            'night': GamePhase.NIGHT,
            'day': GamePhase.DAY,
            'discussion': GamePhase.DISCUSSION,
            'voting': GamePhase.VOTING
        }
        phase = phase_map.get(phase_str, GamePhase.DAY)
        
        return GameObservation(
            phase=phase,
            round=game_state.get('round', 0),
            alive_players=alive_players,
            dead_players=dead_players,
            current_speaker=None,
            last_night_result=game_state.get('last_night_result'),
            voting_results=None,
            discussion_content=None
        )
    
    async def _generate_structured_action(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """生成结构化行动（如投票、查验等）
        
        这里需要根据不同的结构化模型类型，调用策略的相应方法
        """
        model_name = getattr(structured_model, '__name__', 'Unknown')
        self.logger.info(f"生成结构化行动: {model_name}")
        
        try:
            # 根据模型类型调用不同的策略方法
            if 'Discussion' in model_name:
                # 狼人讨论阶段
                return await self._handle_discussion(msg, structured_model, strategy, observation)
            
            elif 'Vote' in model_name:
                # 投票
                return await self._handle_voting(msg, structured_model, strategy, observation)
            
            elif 'Seer' in model_name:
                # 先知查验
                return await self._handle_seer_check(msg, structured_model, strategy, observation)
            
            elif 'WitchResurrect' in model_name:
                # 女巫救人
                return await self._handle_witch_resurrect(msg, structured_model, strategy, observation)
            
            elif 'Poison' in model_name:
                # 女巫毒人
                return await self._handle_witch_poison(msg, structured_model, strategy, observation)
            
            elif 'Hunter' in model_name:
                # 猎人开枪
                return await self._handle_hunter_shoot(msg, structured_model, strategy, observation)
            
            elif 'Werewolf' in model_name or 'Kill' in model_name:
                # 狼人击杀
                return await self._handle_werewolf_kill(msg, structured_model, strategy, observation)
            
            else:
                # 未知类型，使用默认处理
                self.logger.warning(f"未知的结构化模型: {model_name}")
                return await self._default_structured_response(structured_model)
                
        except Exception as e:
            self.logger.error(f"结构化行动生成失败: {e}")
            return await self._default_structured_response(structured_model)
    
    async def _handle_werewolf_kill(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理狼人击杀（智能决策）"""
        # 使用策略生成夜晚行动
        night_action = strategy.generate_night_action(observation)
        
        if night_action and night_action.target:
            target = night_action.target
        else:
            # 默认选择第一个非自己的玩家
            target = None
            for player in observation.alive_players:
                if player != self.agent_name:
                    target = player
                    break
            
            if not target and observation.alive_players:
                # 随机选择一个不是自己的存活玩家
                import random
                candidates = [p for p in observation.alive_players if p != self.agent_name]
                target = random.choice(candidates) if candidates else observation.alive_players[0]
        
        response = Msg(
            name=self.agent_name,
            content=f"建议击杀{target}",
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['name'] = target
        
        self.logger.info(f"狼人击杀决策: {target}")
        return response
    
    async def _handle_discussion(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理狼人讨论"""
        # 狼人讨论是否达成一致
        # 简单策略：前2轮讨论，第3轮达成一致
        context = {'discussion_round': 1}  # TODO: 从消息中提取
        
        # 策略分析
        reasoning = strategy.analyze_situation(observation)
        
        # 生成讨论内容
        discussion_content = strategy.generate_day_speech(observation, context)
        
        # 决定是否达成一致（简化逻辑）
        reach_agreement = context.get('discussion_round', 1) >= 3
        
        response = Msg(
            name=self.agent_name,
            content=discussion_content,
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['reach_agreement'] = reach_agreement
        
        return response
    
    async def _handle_voting(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理投票（带思维链）"""
        # 构建思维链
        current_role = self.strategy_manager.get_current_role()
        
        # 获取可疑和信任的玩家
        suspected_players = {}
        trusted_players = {}
        for player in observation.alive_players:
            player_info = strategy.get_player_info(player)
            if player_info:
                suspected_players[player] = player_info.suspicion_level
                trusted_players[player] = player_info.trust_score
        
        # 获取最近事件
        recent_conversations = self.memory_manager.get_recent_conversations(5)
        recent_events = [conv.get('content', '')[:30] for conv in recent_conversations]
        
        # 构建思维链
        cot = ChainOfThoughtBuilder.build_voting_cot(
            my_role=current_role,
            alive_players=observation.alive_players,
            suspected_players=suspected_players,
            trusted_players=trusted_players,
            recent_events=recent_events
        )
        
        # 使用策略生成投票决策
        voting_decision = strategy.generate_voting_decision(observation, {})
        
        # 选择投票目标
        if voting_decision.target:
            target = voting_decision.target
        elif observation.alive_players:
            # 选择第一个不是自己的玩家
            candidates = [p for p in observation.alive_players if p != self.agent_name]
            target = candidates[0] if candidates else observation.alive_players[0]
        else:
            # 理论上不应该到这里，但以防万一
            target = self.agent_name
        
        # 生成带推理过程的发言
        reasoning_summary = cot.get_reasoning_summary()
        speech = f"我投票给{target}。"
        
        # 如果推理过程不太长，加入简化版
        if len(reasoning_summary) < 150:
            # 提取关键推理步骤
            key_reasoning = [step.content for step in cot.steps 
                           if step.step_type.value in ["分析", "推理"]]
            if key_reasoning:
                speech += f" {key_reasoning[0][:50]}"
        
        response = Msg(
            name=self.agent_name,
            content=speech,
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['vote'] = target
        response.metadata['reasoning_chain'] = cot.to_dict()  # 保存完整推理链
        
        self.logger.info(f"投票决策（带思维链）: {target}")
        self.logger.debug(f"推理过程: {reasoning_summary}")
        return response
    
    async def _handle_seer_check(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理先知查验（带思维链）"""
        # 获取已查验玩家列表
        checked_players = []
        if hasattr(strategy, 'strategy_state') and 'checked_players' in strategy.strategy_state:
            checked_players = strategy.strategy_state['checked_players']
        
        # 获取可疑玩家
        suspected_players = {}
        for player in observation.alive_players:
            player_info = strategy.get_player_info(player)
            if player_info:
                suspected_players[player] = player_info.suspicion_level
        
        # 优先目标（最可疑的未查验玩家）
        unchecked = [p for p in observation.alive_players if p not in checked_players]
        priority_targets = sorted(
            unchecked,
            key=lambda p: suspected_players.get(p, 0.3),
            reverse=True
        )[:3]
        
        # 构建思维链
        cot = ChainOfThoughtBuilder.build_seer_check_cot(
            checked_players=checked_players,
            alive_players=observation.alive_players,
            suspected_players=suspected_players,
            priority_targets=priority_targets
        )
        
        # 使用策略生成查验决策
        night_action = strategy.generate_night_action(observation)
        
        if night_action and night_action.target:
            target = night_action.target
        elif priority_targets:
            target = priority_targets[0]
        else:
            # 选择第一个不是自己的存活玩家
            if observation.alive_players:
                candidates = [p for p in observation.alive_players if p != self.agent_name]
                target = candidates[0] if candidates else observation.alive_players[0]
            else:
                target = self.agent_name  # 理论上不应该到这里
        
        response = Msg(
            name=self.agent_name,
            content=f"查验{target}",
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['name'] = target
        response.metadata['reasoning_chain'] = cot.to_dict()
        
        self.logger.info(f"先知查验（带思维链）: {target}")
        self.logger.debug(f"推理过程: {cot.get_reasoning_summary()}")
        return response
    
    async def _handle_witch_resurrect(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理女巫救人（智能决策）"""
        # 从消息中提取被杀的玩家
        killed_player = None
        if msg and msg.content:
            import re
            # 尝试匹配被杀玩家的名字
            match = re.search(r'Player\d+', msg.content)
            if match:
                killed_player = match.group(0)
        
        # 女巫用药决策逻辑
        resurrect = False
        reasoning = "不使用解药"
        
        # 检查女巫是否还有解药
        has_antidote = True
        if hasattr(strategy, 'strategy_state'):
            has_antidote = strategy.strategy_state.get('has_antidote', True)
        
        if has_antidote and killed_player:
            # 智能决策：是否救人
            should_save = False
            
            # 1. 不救自己（标准规则）
            if killed_player == self.agent_name:
                reasoning = "不能救自己"
            else:
                # 2. 评估被杀玩家的价值
                player_info = strategy.get_player_info(killed_player)
                
                if player_info:
                    # 信任度高的玩家更值得救
                    if player_info.trust_score > 0.7:
                        should_save = True
                        reasoning = f"救{killed_player}，该玩家可信度高"
                    # 可疑度很高的玩家不救
                    elif player_info.suspicion_level > 0.7:
                        reasoning = f"不救{killed_player}，该玩家可疑"
                    else:
                        # 3. 第一晚通常不救（标准策略）
                        if observation.round == 1:
                            reasoning = "第一晚不使用解药（保守策略）"
                        else:
                            # 后续轮次，视情况而定
                            if player_info.trust_score > 0.5:
                                should_save = True
                                reasoning = f"救{killed_player}"
                else:
                    # 没有玩家信息，保守策略
                    reasoning = "信息不足，不使用解药"
            
            resurrect = should_save
        elif not has_antidote:
            reasoning = "解药已用，无法救人"
        else:
            reasoning = "未获取被杀玩家信息"
        
        response = Msg(
            name=self.agent_name,
            content=reasoning,
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['resurrect'] = resurrect
        
        self.logger.info(f"女巫救人决策: {resurrect} - {reasoning}")
        return response
    
    async def _handle_witch_poison(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理女巫毒人（智能决策）"""
        # 检查女巫是否还有毒药
        has_poison = True
        if hasattr(strategy, 'strategy_state'):
            has_poison = strategy.strategy_state.get('has_poison', True)
        
        poison = False
        target = None
        reasoning = "不使用毒药"
        
        if has_poison and observation.alive_players:
            # 智能决策：是否用毒
            
            # 1. 找出最可疑的玩家
            most_suspicious = None
            max_suspicion = 0.0
            
            for player in observation.alive_players:
                if player == self.agent_name:  # 不能毒自己
                    continue
                    
                player_info = strategy.get_player_info(player)
                if player_info and player_info.suspicion_level > max_suspicion:
                    max_suspicion = player_info.suspicion_level
                    most_suspicious = player
            
            # 2. 决定是否用毒
            if most_suspicious and max_suspicion > 0.8:
                # 非常确定是狼人，使用毒药
                poison = True
                target = most_suspicious
                reasoning = f"毒{target}（高度可疑: {max_suspicion:.2f}）"
            elif most_suspicious and max_suspicion > 0.7 and observation.round >= 3:
                # 较为可疑且游戏进入中后期，考虑使用
                if len(observation.alive_players) <= 5:
                    # 玩家数量较少，关键时刻
                    poison = True
                    target = most_suspicious
                    reasoning = f"毒{target}（关键时刻，可疑度: {max_suspicion:.2f}）"
                else:
                    reasoning = "暂不使用毒药，继续观察"
            else:
                reasoning = "目标可疑度不足，保留毒药"
        elif not has_poison:
            reasoning = "毒药已用完"
        else:
            reasoning = "无可用目标"
        
        response = Msg(
            name=self.agent_name,
            content=reasoning,
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['poison'] = poison
        response.metadata['name'] = target
        
        self.logger.info(f"女巫毒人决策: poison={poison}, target={target} - {reasoning}")
        return response
    
    async def _handle_hunter_shoot(
        self,
        msg: Msg,
        structured_model: type,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """处理猎人开枪（智能决策）"""
        shoot = False
        target = None
        reasoning = "不开枪"
        
        # 猎人开枪决策逻辑
        if observation.alive_players:
            # 1. 评估局势
            alive_count = len(observation.alive_players)
            
            # 2. 找出最可疑的玩家
            most_suspicious = None
            max_suspicion = 0.0
            
            for player in observation.alive_players:
                if player == self.agent_name:  # 不能射自己
                    continue
                    
                player_info = strategy.get_player_info(player)
                if player_info and player_info.suspicion_level > max_suspicion:
                    max_suspicion = player_info.suspicion_level
                    most_suspicious = player
            
            # 3. 决定是否开枪
            # 猎人开枪的考虑因素：
            # - 有明确的高可疑目标
            # - 局势紧张（玩家数少）
            # - 自己已经被淘汰，需要利用技能
            
            should_shoot = False
            
            if most_suspicious:
                # 非常确定是狼人
                if max_suspicion > 0.85:
                    should_shoot = True
                    target = most_suspicious
                    reasoning = f"带走{target}（高度可疑: {max_suspicion:.2f}）"
                # 较为可疑且局势危急
                elif max_suspicion > 0.7 and alive_count <= 4:
                    should_shoot = True
                    target = most_suspicious
                    reasoning = f"关键时刻带走{target}（可疑度: {max_suspicion:.2f}）"
                else:
                    reasoning = "放弃开枪（目标不够确定）"
            else:
                reasoning = "放弃开枪（无明确目标）"
            
            shoot = should_shoot
        else:
            reasoning = "无可用目标"
        
        response = Msg(
            name=self.agent_name,
            content=reasoning,
            role="assistant"
        )
        
        # 设置metadata
        if response.metadata is None:
            response.metadata = {}
        response.metadata['shoot'] = shoot
        response.metadata['name'] = target
        
        self.logger.info(f"猎人开枪决策: shoot={shoot}, target={target} - {reasoning}")
        return response
    
    async def _generate_normal_speech(
        self,
        msg: Msg,
        strategy,
        observation: GameObservation
    ) -> Msg:
        """生成普通发言（带思维链）"""
        current_role = self.strategy_manager.get_current_role()
        
        # 收集关键信息
        key_information = []
        recent_conversations = self.memory_manager.get_recent_conversations(3)
        for conv in recent_conversations:
            content = conv.get('content', '')
            if len(content) > 10:
                key_information.append(content[:50])
        
        # 确定发言目标
        phase_str = str(observation.phase.value) if hasattr(observation.phase, 'value') else str(observation.phase)
        
        speaking_goals = {
            "werewolf": "隐藏狼人身份，混淆视听",
            "seer": "引导好人阵营，但不过早暴露",
            "witch": "保护关键角色，理性分析",
            "hunter": "隐藏身份，关键时刻威慑",
            "villager": "逻辑分析，识破谎言"
        }
        speaking_goal = speaking_goals.get(current_role, "理性分析局势")
        
        # 构建思维链
        cot = ChainOfThoughtBuilder.build_speech_cot(
            my_role=current_role,
            game_phase=phase_str,
            key_information=key_information,
            speaking_goal=speaking_goal
        )
        
        # 使用策略生成白天发言
        context = {
            'message': msg.content if msg else "",
            'phase': observation.phase,
            'cot': cot  # 传递思维链给策略
        }
        
        try:
            speech = strategy.generate_day_speech(observation, context)
        except Exception as e:
            self.logger.error(f"策略生成发言失败: {e}")
            # 使用思维链的结论作为备用
            speech = f"基于当前局势，{speaking_goal}。"
        
        response = Msg(
            name=self.agent_name,
            content=speech,
            role="assistant"
        )
        
        # 可选：将思维链添加到metadata（用于调试）
        if response.metadata is None:
            response.metadata = {}
        response.metadata['reasoning_chain'] = cot.to_dict()
        
        self.logger.debug(f"发言推理过程: {cot.get_reasoning_summary()}")
        
        return response
    
    async def _default_structured_response(self, structured_model: type) -> Msg:
        """生成默认结构化响应"""
        model_name = getattr(structured_model, '__name__', 'Unknown')
        
        response = Msg(
            name=self.agent_name,
            content="采用默认决策",
            role="assistant"
        )
        
        if response.metadata is None:
            response.metadata = {}
        
        # 从游戏状态中获取存活玩家列表
        alive_players = self.memory_manager.game_state.get('alive_players', [])
        if not alive_players:
            # 如果没有存活玩家信息，使用空列表
            alive_players = []
        
        # 根据模型类型设置默认值
        if 'Discussion' in model_name:
            response.metadata['reach_agreement'] = False
        elif 'Vote' in model_name:
            # 选择一个默认投票目标
            if alive_players:
                candidates = [p for p in alive_players if p != self.agent_name]
                default_vote = candidates[0] if candidates else alive_players[0]
            else:
                # 如果没有存活玩家信息，返回自己
                default_vote = self.agent_name
            response.metadata['vote'] = default_vote
        elif 'Seer' in model_name:
            # 选择一个默认查验目标
            if alive_players:
                candidates = [p for p in alive_players if p != self.agent_name]
                default_target = candidates[0] if candidates else alive_players[0]
            else:
                default_target = self.agent_name
            response.metadata['name'] = default_target
        elif 'WitchResurrect' in model_name:
            response.metadata['resurrect'] = False
        elif 'Poison' in model_name:
            response.metadata['poison'] = False
            response.metadata['name'] = None
        elif 'Hunter' in model_name:
            response.metadata['shoot'] = False
            response.metadata['name'] = None
        
        return response

