# -*- coding: utf-8 -*-
"""先知策略模块"""

import random
from typing import Dict, List, Any, Optional
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    SeerReasoning,
    StrategicPlan
)
from strategies.base_strategy import BaseStrategy
from utils.logger import WerewolfLogger


class SeerStrategy(BaseStrategy):
    """先知策略实现"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        super().__init__(agent_name, logger)
        
        # 先知特有状态
        self.strategy_state.update({
            'checked_players': [],  # 已查验的玩家
            'known_werewolves': [],  # 已知的狼人
            'known_good_players': [],  # 已知的好人
            'badge_flow_plan': [],  # 警徽流计划
            'revealed_identity': False,  # 是否已暴露身份
            'protection_priority': [],  # 保护优先级
            'last_check_result': None,  # 上次查验结果
            'check_history': [],  # 查验历史
            'credibility_score': 0.5  # 可信度分数
        })
    
    def get_role_name(self) -> str:
        """获取角色名称"""
        return "seer"
    
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        if observation.phase != "night":
            return None
        
        # 选择查验目标
        target = self._select_check_target()
        
        if target:
            return self.create_action_decision(
                action_type="check",
                target=target,
                reasoning=f"查验{target}以获取身份信息",
                confidence=0.9,
                priority=9,
                content=f"查验{target}"
            )
        
        return None
    
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        reasoning = self.analyze_situation(observation)
        
        # 根据是否暴露身份选择发言策略
        if self.strategy_state['revealed_identity']:
            return self._revealed_speech(reasoning)
        elif self._should_reveal_identity(reasoning):
            return self._reveal_identity_speech(reasoning)
        else:
            return self._hidden_speech(reasoning)
    
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        reasoning = self.analyze_situation(observation)
        
        # 优先投票给已知的狼人
        if self.strategy_state['known_werewolves']:
            target = self._select_werewolf_target()
            if target:
                return self.create_action_decision(
                    action_type="vote",
                    target=target,
                    reasoning=f"通过查验确认{target}是狼人",
                    confidence=0.95,
                    priority=10
                )
        
        # 投票给可疑玩家
        suspicious_players = self.get_most_suspicious_players(3)
        if suspicious_players:
            target = suspicious_players[0]
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning=f"基于行为分析，{target}最可疑",
                confidence=0.6,
                priority=7
            )
        
        # 默认投票
        alive_players = self.get_alive_players()
        if alive_players:
            target = random.choice(alive_players)
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning="信息不足，随机投票",
                confidence=0.3,
                priority=4
            )
        
        return self.create_action_decision(
            action_type="speak",
            content="弃权",
            confidence=0.1,
            priority=1
        )
    
    def analyze_situation(self, observation: GameObservation) -> SeerReasoning:
        """分析当前局势"""
        alive_players = self.get_alive_players()
        dead_players = self.get_dead_players()
        
        # 评估信息价值
        information_value = self._assess_information_value()
        
        # 制定信息策略
        information_strategy = self._plan_information_strategy(information_value)
        
        # 确定保护优先级
        protection_priority = self._determine_protection_priority()
        
        # 管理可信度
        credibility_management = self._plan_credibility_management()
        
        return SeerReasoning(
            role="seer",
            phase=observation.phase,
            situation_assessment=self._assess_overall_situation(alive_players, dead_players),
            immediate_action=self._determine_immediate_action(observation),
            long_term_strategy=self._plan_long_term_strategy(),
            allies=self.strategy_state['known_good_players'],
            enemies=self.strategy_state['known_werewolves'],
            neutral_players=self._get_neutral_players(alive_players),
            check_target=self._select_check_target(),
            information_strategy=information_strategy,
            protection_priority=protection_priority,
            credibility_management=credibility_management
        )
    
    def _select_check_target(self) -> Optional[str]:
        """选择查验目标"""
        alive_players = self.get_alive_players()
        unchecked_players = [p for p in alive_players if p not in self.strategy_state['checked_players']]
        
        if not unchecked_players:
            return None
        
        # 优先级评分
        target_scores = {}
        
        for player in unchecked_players:
            score = 0.0
            player_info = self.get_player_info(player)
            
            if not player_info:
                continue
            
            # 可疑程度权重
            score += player_info.suspicion_level * 0.4
            
            # 发言活跃度权重
            if hasattr(player_info, 'last_action') and player_info.last_action:
                score += 0.2
            
            # 信任度权重（低信任度的玩家更可疑）
            score += (1.0 - player_info.trust_score) * 0.3
            
            # 随机因素
            score += random.random() * 0.1
            
            target_scores[player] = score
        
        if target_scores:
            best_target = max(target_scores, key=target_scores.get)
            return best_target
        
        return random.choice(unchecked_players) if unchecked_players else None
    
    def _should_reveal_identity(self, reasoning: SeerReasoning) -> bool:
        """判断是否应该暴露身份"""
        # 如果已经知道狼人，应该暴露身份
        if self.strategy_state['known_werewolves']:
            return True
        
        # 如果存活玩家很少，应该暴露身份
        alive_count = len(self.get_alive_players())
        if alive_count <= 5:
            return True
        
        # 如果可信度很低，不应该暴露身份
        if self.strategy_state['credibility_score'] < 0.3:
            return False
        
        # 如果有多个宣称先知的玩家，需要竞争
        # 这里简化逻辑
        return False
    
    def _revealed_speech(self, reasoning: SeerReasoning) -> str:
        """已暴露身份的发言"""
        if self.strategy_state['known_werewolves']:
            werewolf = self.strategy_state['known_werewolves'][0]
            return f"我是先知！昨晚查验了{werewolf}，他是狼人！请大家投票给他。"
        elif self.strategy_state['known_good_players']:
            good_player = self.strategy_state['known_good_players'][0]
            return f"我是先知，昨晚查验了{good_player}，他是好人。我会继续为大家提供信息。"
        else:
            return "我是先知，正在努力找出狼人。请大家相信我。"
    
    def _reveal_identity_speech(self, reasoning: SeerReasoning) -> str:
        """暴露身份的发言"""
        if self.strategy_state['last_check_result']:
            target, result = self.strategy_state['last_check_result']
            if result == 'werewolf':
                return f"我是先知！昨晚查验了{target}，他是狼人！"
            else:
                return f"我是先知，昨晚查验了{target}，他是好人。"
        else:
            return "我是先知，会为大家提供准确信息。"
    
    def _hidden_speech(self, reasoning: SeerReasoning) -> str:
        """隐藏身份的发言"""
        speeches = [
            "我需要更多时间来分析每个人的发言。",
            "从逻辑角度，某些玩家的行为值得怀疑。",
            "建议大家仔细观察投票模式。",
            "我会基于证据做出判断，而不是盲目跟风。"
        ]
        return random.choice(speeches)
    
    def _select_werewolf_target(self) -> Optional[str]:
        """选择狼人投票目标"""
        if not self.strategy_state['known_werewolves']:
            return None
        
        # 选择威胁最大的狼人
        werewolves = self.strategy_state['known_werewolves']
        
        # 简单策略：投票给第一个已知的狼人
        return werewolves[0] if werewolves else None
    
    def _assess_information_value(self) -> float:
        """评估信息价值"""
        alive_count = len(self.get_alive_players())
        checked_count = len(self.strategy_state['checked_players'])
        
        # 未查验的玩家越多，信息价值越高
        unchecked_ratio = (alive_count - checked_count) / max(1, alive_count)
        
        return unchecked_ratio
    
    def _plan_information_strategy(self, information_value: float) -> str:
        """规划信息策略"""
        if self.strategy_state['revealed_identity']:
            return "open_information_sharing"
        elif information_value > 0.7:
            return "aggressive_information_gathering"
        elif information_value > 0.4:
            return "balanced_information_strategy"
        else:
            return "selective_information_disclosure"
    
    def _determine_protection_priority(self) -> List[str]:
        """确定保护优先级"""
        priority = []
        
        # 已知的好人优先保护
        priority.extend(self.strategy_state['known_good_players'])
        
        # 高可信度的玩家
        trusted_players = self.get_most_trusted_players(2)
        priority.extend(trusted_players)
        
        # 去重
        return list(dict.fromkeys(priority))
    
    def _plan_credibility_management(self) -> str:
        """规划可信度管理"""
        if self.strategy_state['revealed_identity']:
            return "maintain_revealed_credibility"
        elif self.strategy_state['credibility_score'] < 0.4:
            return "rebuild_credibility"
        else:
            return "gradual_credibility_building"
    
    def _assess_overall_situation(self, alive_players: List[str], dead_players: List[str]) -> str:
        """评估整体局势"""
        werewolf_count = len(self.strategy_state['known_werewolves'])
        good_count = len(self.strategy_state['known_good_players'])
        
        if werewolf_count >= 2:
            return "critical_werewolf_threat"
        elif good_count >= 3:
            return "strong_good_position"
        elif len(alive_players) <= 5:
            return "late_game_critical"
        else:
            return "information_gathering_phase"
    
    def _determine_immediate_action(self, observation: GameObservation) -> str:
        """确定立即行动"""
        if observation.phase == "night":
            return "check_suspicious_player"
        elif self.strategy_state['revealed_identity']:
            return "share_information_and_guide"
        else:
            return "analyze_and_gather_information"
    
    def _plan_long_term_strategy(self) -> str:
        """规划长期策略"""
        if self.strategy_state['revealed_identity']:
            return "lead_good_camp"
        elif len(self.strategy_state['known_werewolves']) > 0:
            return "prepare_reveal_and_eliminate"
        else:
            return "silent_information_collection"
    
    def _get_neutral_players(self, alive_players: List[str]) -> List[str]:
        """获取中立玩家"""
        known_players = (self.strategy_state['known_werewolves'] + 
                        self.strategy_state['known_good_players'])
        return [p for p in alive_players if p not in known_players]
    
    def record_check_result(self, target: str, result: str) -> None:
        """记录查验结果"""
        if target not in self.strategy_state['checked_players']:
            self.strategy_state['checked_players'].append(target)
        
        self.strategy_state['last_check_result'] = (target, result)
        
        check_entry = {
            'target': target,
            'result': result,
            'round': len(self.strategy_state['check_history']) + 1
        }
        self.strategy_state['check_history'].append(check_entry)
        
        # 更新已知信息
        if result == 'werewolf':
            if target not in self.strategy_state['known_werewolves']:
                self.strategy_state['known_werewolves'].append(target)
                self.update_suspicion_level(target, 0.8)
        else:  # good
            if target not in self.strategy_state['known_good_players']:
                self.strategy_state['known_good_players'].append(target)
                self.update_trust_score(target, 0.4)
                self.update_suspicion_level(target, -0.3)
        
        self.logger.info(f"查验结果: {target} -> {result}")
    
    def reveal_identity(self) -> None:
        """暴露身份"""
        self.strategy_state['revealed_identity'] = True
        self.logger.info("先知暴露身份")
    
    def hide_identity(self) -> None:
        """隐藏身份"""
        self.strategy_state['revealed_identity'] = False
        self.logger.info("先知隐藏身份")
    
    def update_credibility_score(self, score_change: float) -> None:
        """更新可信度分数"""
        old_score = self.strategy_state['credibility_score']
        new_score = max(0.0, min(1.0, old_score + score_change))
        self.strategy_state['credibility_score'] = new_score
        
        self.logger.debug(f"更新可信度: {old_score:.2f}->{new_score:.2f}")
    
    def create_badge_flow_plan(self) -> List[str]:
        """创建警徽流计划"""
        alive_players = self.get_alive_players()
        unchecked_players = [p for p in alive_players if p not in self.strategy_state['checked_players']]
        
        # 简单的警徽流：按优先级查验
        plan = []
        
        # 优先查验可疑玩家
        suspicious = self.get_most_suspicious_players(3)
        plan.extend([p for p in suspicious if p in unchecked_players])
        
        # 然后查验其他玩家
        remaining = [p for p in unchecked_players if p not in plan]
        plan.extend(remaining)
        
        self.strategy_state['badge_flow_plan'] = plan
        return plan
    
    def get_check_summary(self) -> Dict[str, Any]:
        """获取查验摘要"""
        return {
            'checked_count': len(self.strategy_state['checked_players']),
            'known_werewolves': len(self.strategy_state['known_werewolves']),
            'known_good_players': len(self.strategy_state['known_good_players']),
            'badge_flow_plan': self.strategy_state['badge_flow_plan'].copy(),
            'check_history': self.strategy_state['check_history'].copy()
        }
