# -*- coding: utf-8 -*-
"""女巫策略模块"""

import random
from typing import Dict, List, Any, Optional
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    WitchReasoning,
    StrategicPlan
)
from strategies.base_strategy import BaseStrategy
from utils.logger import WerewolfLogger


class WitchStrategy(BaseStrategy):
    """女巫策略实现"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        super().__init__(agent_name, logger)
        
        # 女巫特有状态
        self.strategy_state.update({
            'healing_potion_used': False,  # 解药是否已使用
            'poison_potion_used': False,   # 毒药是否已使用
            'last_night_victim': None,     # 昨晚受害者
            'heal_history': [],            # 治疗历史
            'poison_history': [],           # 毒药历史
            'suspected_werewolves': [],     # 可疑的狼人
            'protected_players': [],         # 保护过的玩家
            'role_concealment_strategy': 'hidden',  # 身份隐藏策略
            'potion_timing_strategy': 'conservative'  # 药水使用时机策略
        })
    
    def get_role_name(self) -> str:
        """获取角色名称"""
        return "witch"
    
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        if observation.phase != "night":
            return None
        
        reasoning = self.analyze_situation(observation)
        
        # 决定是否使用解药
        heal_decision = self._decide_heal_action(reasoning)
        if heal_decision:
            return heal_decision
        
        # 决定是否使用毒药
        poison_decision = self._decide_poison_action(reasoning)
        if poison_decision:
            return poison_decision
        
        return None
    
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        reasoning = self.analyze_situation(observation)
        
        # 根据身份隐藏策略选择发言
        if reasoning.role_concealment == "hidden":
            return self._hidden_role_speech(reasoning)
        elif reasoning.role_concealment == "semi_revealed":
            return self._semi_revealed_speech(reasoning)
        else:
            return self._revealed_speech(reasoning)
    
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        reasoning = self.analyze_situation(observation)
        
        # 优先投票给可疑的狼人
        if self.strategy_state['suspected_werewolves']:
            target = self._select_werewolf_target()
            if target:
                return self.create_action_decision(
                    action_type="vote",
                    target=target,
                    reasoning=f"基于分析，{target}很可能是狼人",
                    confidence=0.7,
                    priority=8
                )
        
        # 投票给最可疑的玩家
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
    
    def analyze_situation(self, observation: GameObservation) -> WitchReasoning:
        """分析当前局势"""
        alive_players = self.get_alive_players()
        dead_players = self.get_dead_players()
        
        # 评估威胁等级
        threats = self._assess_threats(alive_players)
        
        # 决定治疗策略
        heal_decision = self._plan_heal_decision()
        
        # 决定毒药策略
        poison_decision = self._plan_poison_decision()
        
        # 确定药水使用时机
        potion_timing = self._determine_potion_timing()
        
        # 身份隐藏策略
        role_concealment = self._plan_role_concealment()
        
        return WitchReasoning(
            role="witch",
            phase=observation.phase,
            situation_assessment=self._assess_overall_situation(alive_players, dead_players),
            immediate_action=self._determine_immediate_action(observation),
            long_term_strategy=self._plan_long_term_strategy(),
            allies=self._get_allies(),
            enemies=threats,
            neutral_players=self._get_neutral_players(alive_players, threats),
            heal_decision=heal_decision,
            poison_decision=poison_decision,
            potion_timing=potion_timing,
            role_concealment=role_concealment
        )
    
    def _decide_heal_action(self, reasoning: WitchReasoning) -> Optional[ActionDecision]:
        """决定治疗行动"""
        if self.strategy_state['healing_potion_used']:
            return None
        
        # 获取昨晚受害者
        victim = self.strategy_state.get('last_night_victim')
        if not victim:
            return None
        
        # 评估是否应该救
        should_heal = self._should_heal_victim(victim, reasoning)
        
        if should_heal:
            self.strategy_state['healing_potion_used'] = True
            self.strategy_state['heal_history'].append(victim)
            self.strategy_state['protected_players'].append(victim)
            
            return self.create_action_decision(
                action_type="heal",
                target=victim,
                reasoning=f"评估后决定救{victim}",
                confidence=0.8,
                priority=9,
                content=f"治疗{victim}"
            )
        
        return None
    
    def _decide_poison_action(self, reasoning: WitchReasoning) -> Optional[ActionDecision]:
        """决定毒药行动"""
        if self.strategy_state['poison_potion_used']:
            return None
        
        # 评估是否应该使用毒药
        should_poison, target = self._should_use_poison(reasoning)
        
        if should_poison and target:
            self.strategy_state['poison_potion_used'] = True
            self.strategy_state['poison_history'].append(target)
            
            return self.create_action_decision(
                action_type="poison",
                target=target,
                reasoning=f"基于分析决定毒{target}",
                confidence=0.7,
                priority=8,
                content=f"毒杀{target}"
            )
        
        return None
    
    def _should_heal_victim(self, victim: str, reasoning: WitchReasoning) -> bool:
        """判断是否应该治疗受害者"""
        # 第一晚通常救人
        if len(self.strategy_state['heal_history']) == 0:
            return True
        
        # 如果受害者是已知的狼人，不救
        if victim in self.strategy_state['suspected_werewolves']:
            return False
        
        # 如果受害者是保护过的玩家，考虑不救
        if victim in self.strategy_state['protected_players']:
            return random.random() < 0.3  # 30%概率再救
        
        # 根据局势评估
        alive_count = len(self.get_alive_players())
        if alive_count <= 5:
            return True  # 关键时刻救人
        
        # 根据可信度评估
        player_info = self.get_player_info(victim)
        if player_info and player_info.trust_score > 0.6:
            return True
        
        # 默认有50%概率救人
        return random.random() < 0.5
    
    def _should_use_poison(self, reasoning: WitchReasoning) -> tuple[bool, Optional[str]]:
        """判断是否应该使用毒药"""
        # 如果解药已使用，更倾向于使用毒药
        heal_used = self.strategy_state['healing_potion_used']
        
        # 如果有高度可疑的玩家
        if self.strategy_state['suspected_werewolves']:
            # 选择最可疑的玩家
            suspicious_scores = {}
            for player in self.strategy_state['suspected_werewolves']:
                player_info = self.get_player_info(player)
                if player_info:
                    suspicious_scores[player] = player_info.suspicion_level
            
            if suspicious_scores:
                target = max(suspicious_scores, key=suspicious_scores.get)
                confidence = suspicious_scores[target]
                
                # 根据局势调整使用概率
                use_probability = 0.6 if heal_used else 0.4
                if confidence > 0.7:
                    use_probability += 0.3
                
                if random.random() < use_probability:
                    return True, target
        
        # 根据玩家数量决定
        alive_count = len(self.get_alive_players())
        if alive_count <= 4:
            # 关键时刻更可能使用毒药
            use_probability = 0.7 if heal_used else 0.5
        else:
            use_probability = 0.3 if heal_used else 0.2
        
        if random.random() < use_probability:
            # 选择最可疑的玩家
            most_suspicious = self.get_most_suspicious_players(1)
            if most_suspicious:
                return True, most_suspicious[0]
        
        return False, None
    
    def _select_werewolf_target(self) -> Optional[str]:
        """选择狼人投票目标"""
        if not self.strategy_state['suspected_werewolves']:
            return None
        
        # 选择威胁最大的狼人
        werewolves = self.strategy_state['suspected_werewolves']
        
        # 简单策略：投票给第一个可疑的狼人
        return werewolves[0] if werewolves else None
    
    def _assess_threats(self, alive_players: List[str]) -> List[str]:
        """评估威胁玩家"""
        threats = []
        
        for player in alive_players:
            player_info = self.get_player_info(player)
            if not player_info:
                continue
            
            # 高可疑度的玩家是威胁
            if player_info.suspicion_level > 0.6:
                threats.append(player)
                if player not in self.strategy_state['suspected_werewolves']:
                    self.strategy_state['suspected_werewolves'].append(player)
        
        return threats
    
    def _plan_heal_decision(self) -> str:
        """规划治疗决策"""
        if self.strategy_state['healing_potion_used']:
            return "no_heal_available"
        elif len(self.strategy_state['heal_history']) == 0:
            return "first_night_heal"
        elif len(self.get_alive_players()) <= 5:
            return "critical_situation_heal"
        else:
            return "selective_heal"
    
    def _plan_poison_decision(self) -> str:
        """规划毒药决策"""
        if self.strategy_state['poison_potion_used']:
            return "no_poison_available"
        elif self.strategy_state['healing_potion_used']:
            return "aggressive_poison"
        elif len(self.strategy_state['suspected_werewolves']) >= 2:
            return "confirmed_poison"
        else:
            return "conservative_poison"
    
    def _determine_potion_timing(self) -> str:
        """确定药水使用时机"""
        heal_used = self.strategy_state['healing_potion_used']
        poison_used = self.strategy_state['poison_potion_used']
        
        if not heal_used and not poison_used:
            return "both_available"
        elif heal_used and not poison_used:
            return "only_poison"
        elif not heal_used and poison_used:
            return "only_heal"
        else:
            return "no_potions"
    
    def _plan_role_concealment(self) -> str:
        """规划身份隐藏策略"""
        # 如果药水都已使用，可以考虑暴露身份
        if (self.strategy_state['healing_potion_used'] and 
            self.strategy_state['poison_potion_used']):
            return "revealed"
        
        # 如果有高度可疑的狼人，可以考虑半暴露
        if self.strategy_state['suspected_werewolves']:
            return "semi_revealed"
        
        return "hidden"
    
    def _assess_overall_situation(self, alive_players: List[str], dead_players: List[str]) -> str:
        """评估整体局势"""
        potions_available = (
            not self.strategy_state['healing_potion_used'] or 
            not self.strategy_state['poison_potion_used']
        )
        
        if len(alive_players) <= 4:
            return "critical"
        elif not potions_available:
            return "no_potions"
        elif len(self.strategy_state['suspected_werewolves']) >= 2:
            return "strong_intelligence"
        else:
            return "information_gathering"
    
    def _determine_immediate_action(self, observation: GameObservation) -> str:
        """确定立即行动"""
        if observation.phase == "night":
            return "evaluate_potions_usage"
        elif observation.phase == "day":
            concealment = self._plan_role_concealment()
            if concealment == "revealed":
                return "share_information"
            else:
                return "analyze_and_guide"
        else:
            return "observe_and_plan"
    
    def _plan_long_term_strategy(self) -> str:
        """规划长期策略"""
        heal_used = self.strategy_state['healing_potion_used']
        poison_used = self.strategy_state['poison_potion_used']
        
        if not heal_used and not poison_used:
            return "balanced_potion_strategy"
        elif heal_used and not poison_used:
            return "poison_focused_strategy"
        elif not heal_used and poison_used:
            return "heal_focused_strategy"
        else:
            return "post_potion_strategy"
    
    def _get_allies(self) -> List[str]:
        """获取盟友列表"""
        # 女巫的盟友是可信的好人
        allies = []
        for player_name, player_info in self.player_info.items():
            if (player_info.trust_score > 0.7 and 
                player_info.suspicion_level < 0.3 and
                player_name not in self.strategy_state['suspected_werewolves']):
                allies.append(player_name)
        return allies
    
    def _get_neutral_players(self, alive_players: List[str], threats: List[str]) -> List[str]:
        """获取中立玩家"""
        return [p for p in alive_players 
                if p not in threats and p not in self.strategy_state['suspected_werewolves']]
    
    def _hidden_role_speech(self, reasoning: WitchReasoning) -> str:
        """隐藏身份的发言"""
        speeches = [
            "我需要更多时间来分析局势。",
            "从逻辑角度，某些玩家的行为值得怀疑。",
            "建议大家仔细观察投票模式。",
            "我会基于证据做出判断。"
        ]
        return random.choice(speeches)
    
    def _semi_revealed_speech(self, reasoning: WitchReasoning) -> str:
        """半暴露身份的发言"""
        speeches = [
            "昨晚的情况很复杂，我有一些信息。",
            "我注意到一些异常情况，需要大家注意。",
            "基于我的观察，某些玩家很可疑。",
            "我会在关键时刻提供重要信息。"
        ]
        return random.choice(speeches)
    
    def _revealed_speech(self, reasoning: WitchReasoning) -> str:
        """暴露身份的发言"""
        if self.strategy_state['heal_history']:
            healed = self.strategy_state['heal_history'][0]
            return f"我是女巫，第一晚救了{healed}。"
        elif self.strategy_state['poison_history']:
            poisoned = self.strategy_state['poison_history'][0]
            return f"我是女巫，我毒了{poisoned}。"
        else:
            return "我是女巫，会尽力保护好人阵营。"
    
    def set_night_victim(self, victim: str) -> None:
        """设置昨晚受害者"""
        self.strategy_state['last_night_victim'] = victim
        self.logger.info(f"昨晚受害者: {victim}")
    
    def add_suspected_werewolf(self, player: str) -> None:
        """添加可疑狼人"""
        if player not in self.strategy_state['suspected_werewolves']:
            self.strategy_state['suspected_werewolves'].append(player)
            self.logger.info(f"添加可疑狼人: {player}")
    
    def remove_suspected_werewolf(self, player: str) -> None:
        """移除可疑狼人"""
        if player in self.strategy_state['suspected_werewolves']:
            self.strategy_state['suspected_werewolves'].remove(player)
            self.logger.info(f"移除可疑狼人: {player}")
    
    def get_potion_status(self) -> Dict[str, bool]:
        """获取药水状态"""
        return {
            'heal_available': not self.strategy_state['healing_potion_used'],
            'poison_available': not self.strategy_state['poison_potion_used']
        }
    
    def get_action_history(self) -> Dict[str, List[str]]:
        """获取行动历史"""
        return {
            'heal_history': self.strategy_state['heal_history'].copy(),
            'poison_history': self.strategy_state['poison_history'].copy(),
            'protected_players': self.strategy_state['protected_players'].copy()
        }
