# -*- coding: utf-8 -*-
"""村民策略模块"""

import random
from typing import Dict, List, Any, Optional
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    VillagerReasoning,
    StrategicPlan
)
from strategies.base_strategy import BaseStrategy
from utils.logger import WerewolfLogger


class VillagerStrategy(BaseStrategy):
    """村民策略实现"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        super().__init__(agent_name, logger)
        
        # 村民特有状态
        self.strategy_state.update({
            'analysis_focus': 'behavioral',  # 分析重点：behavioral/logical/voting
            'voting_strategy': 'evidence_based',  # 投票策略
            'information_gathering': 'active',  # 信息收集：active/passive
            'coalition_building': False,  # 联盟建设
            'trusted_players': [],  # 可信玩家列表
            'suspected_werewolves': [],  # 可疑狼人列表
            'speech_patterns': {},  # 发言模式分析
            'voting_patterns': {},  # 投票模式分析
            'logical_consistency': {},  # 逻辑一致性分析
            'leadership_following': True  # 是否跟随领导者
        })
    
    def get_role_name(self) -> str:
        """获取角色名称"""
        return "villager"
    
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        # 村民夜晚没有特殊行动
        return None
    
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        reasoning = self.analyze_situation(observation)
        
        # 根据分析重点选择发言策略
        if reasoning.analysis_focus == "logical":
            return self._logical_analysis_speech(reasoning)
        elif reasoning.analysis_focus == "behavioral":
            return self._behavioral_analysis_speech(reasoning)
        elif reasoning.analysis_focus == "voting":
            return self._voting_analysis_speech(reasoning)
        else:
            return self._general_analysis_speech(reasoning)
    
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        reasoning = self.analyze_situation(observation)
        
        # 根据投票策略选择目标
        if reasoning.voting_strategy == "evidence_based":
            return self._evidence_based_voting(reasoning)
        elif reasoning.voting_strategy == "coalition_based":
            return self._coalition_based_voting(reasoning)
        elif reasoning.voting_strategy == "leader_following":
            return self._leader_following_voting(reasoning)
        else:
            return self._default_voting(reasoning)
    
    def analyze_situation(self, observation: GameObservation) -> VillagerReasoning:
        """分析当前局势"""
        alive_players = self.get_alive_players()
        dead_players = self.get_dead_players()
        
        # 确定分析重点
        analysis_focus = self._determine_analysis_focus()
        
        # 确定投票策略
        voting_strategy = self._determine_voting_strategy()
        
        # 信息收集策略
        information_gathering = self._plan_information_gathering()
        
        # 联盟建设策略
        coalition_building = self._plan_coalition_building()
        
        return VillagerReasoning(
            role="villager",
            phase=observation.phase,
            situation_assessment=self._assess_overall_situation(alive_players, dead_players),
            immediate_action=self._determine_immediate_action(observation),
            long_term_strategy=self._plan_long_term_strategy(),
            allies=self._get_allies(),
            enemies=self.strategy_state['suspected_werewolves'],
            neutral_players=self._get_neutral_players(alive_players),
            analysis_focus=analysis_focus,
            voting_strategy=voting_strategy,
            information_gathering=information_gathering,
            coalition_building=coalition_building
        )
    
    def _determine_analysis_focus(self) -> str:
        """确定分析重点"""
        # 根据游戏阶段调整分析重点
        alive_count = len(self.get_alive_players())
        
        if alive_count <= 5:
            return "voting"  # 关键时刻重点关注投票
        elif len(self.strategy_state['suspected_werewolves']) >= 2:
            return "logical"  # 有多个可疑目标时重点逻辑分析
        else:
            return "behavioral"  # 默认行为分析
    
    def _determine_voting_strategy(self) -> str:
        """确定投票策略"""
        if self.strategy_state['coalition_building']:
            return "coalition_based"
        elif self.strategy_state['leadership_following'] and self.strategy_state['trusted_players']:
            return "leader_following"
        else:
            return "evidence_based"
    
    def _plan_information_gathering(self) -> str:
        """规划信息收集策略"""
        if len(self.strategy_state['trusted_players']) >= 2:
            return "focused_information"
        elif len(self.get_alive_players()) <= 6:
            return "intensive_gathering"
        else:
            return "passive_observation"
    
    def _plan_coalition_building(self) -> str:
        """规划联盟建设策略"""
        if self.strategy_state['coalition_building']:
            return "active_coalition"
        elif len(self.strategy_state['trusted_players']) >= 3:
            return "coalition_maintenance"
        else:
            return "coalition_preparation"
    
    def _assess_overall_situation(self, alive_players: List[str], dead_players: List[str]) -> str:
        """评估整体局势"""
        if len(alive_players) <= 4:
            return "critical_phase"
        elif len(self.strategy_state['suspected_werewolves']) >= 3:
            return "high_suspicion_phase"
        elif len(self.strategy_state['trusted_players']) >= 3:
            return "strong_coalition_phase"
        else:
            return "information_gathering_phase"
    
    def _determine_immediate_action(self, observation: GameObservation) -> str:
        """确定立即行动"""
        if observation.phase == "night":
            return "rest_and_plan"
        elif observation.phase == "day":
            focus = self._determine_analysis_focus()
            if focus == "logical":
                return "logical_analysis"
            elif focus == "behavioral":
                return "behavioral_analysis"
            else:
                return "voting_analysis"
        else:
            return "observe_and_learn"
    
    def _plan_long_term_strategy(self) -> str:
        """规划长期策略"""
        if self.strategy_state['coalition_building']:
            return "coalition_dominance"
        elif len(self.strategy_state['suspected_werewolves']) >= 2:
            return "werewolf_elimination"
        else:
            return "information_accumulation"
    
    def _get_allies(self) -> List[str]:
        """获取盟友列表"""
        return self.strategy_state['trusted_players'].copy()
    
    def _get_neutral_players(self, alive_players: List[str]) -> List[str]:
        """获取中立玩家"""
        return [p for p in alive_players 
                if p not in self.strategy_state['trusted_players'] and 
                   p not in self.strategy_state['suspected_werewolves']]
    
    def _logical_analysis_speech(self, reasoning: VillagerReasoning) -> str:
        """逻辑分析发言"""
        speeches = [
            "从逻辑角度分析，某些玩家的发言存在矛盾。",
            "基于时间线分析，昨晚的情况值得深思。",
            "我注意到投票模式中的一些异常，需要大家注意。",
            "让我们用逻辑推理来找出狼人，而不是凭感觉。"
        ]
        return random.choice(speeches)
    
    def _behavioral_analysis_speech(self, reasoning: VillagerReasoning) -> str:
        """行为分析发言"""
        speeches = [
            "观察某些玩家的行为模式，我发现了一些可疑之处。",
            "从发言频率和内容来看，有些玩家不太正常。",
            "我注意到某些玩家在关键时刻的异常反应。",
            "行为分析往往能揭示隐藏的信息。"
        ]
        return random.choice(speeches)
    
    def _voting_analysis_speech(self, reasoning: VillagerReasoning) -> str:
        """投票分析发言"""
        speeches = [
            "分析投票历史，我发现了一些值得关注的模式。",
            "某些玩家的投票选择与他们的发言不符。",
            "投票倾向分析可以帮助我们识别狼人。",
            "让我们回顾一下之前的投票结果。"
        ]
        return random.choice(speeches)
    
    def _general_analysis_speech(self, reasoning: VillagerReasoning) -> str:
        """一般分析发言"""
        speeches = [
            "我需要更多时间来分析当前局势。",
            "作为村民，我会努力为好人阵营做出贡献。",
            "建议大家理性分析，避免被误导。",
            "我会基于证据做出判断。"
        ]
        return random.choice(speeches)
    
    def _evidence_based_voting(self, reasoning: VillagerReasoning) -> ActionDecision:
        """基于证据的投票"""
        # 选择证据最充分的可疑玩家
        if self.strategy_state['suspected_werewolves']:
            # 根据可疑程度排序
            suspicious_scores = {}
            for player in self.strategy_state['suspected_werewolves']:
                player_info = self.get_player_info(player)
                if player_info:
                    suspicious_scores[player] = player_info.suspicion_level
            
            if suspicious_scores:
                target = max(suspicious_scores, key=suspicious_scores.get)
                return self.create_action_decision(
                    action_type="vote",
                    target=target,
                    reasoning=f"基于证据分析，{target}最可疑",
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
        return self._default_voting(reasoning)
    
    def _coalition_based_voting(self, reasoning: VillagerReasoning) -> ActionDecision:
        """基于联盟的投票"""
        if self.strategy_state['trusted_players']:
            # 选择可信玩家投票的目标
            for trusted_player in self.strategy_state['trusted_players']:
                player_info = self.get_player_info(trusted_player)
                if player_info and hasattr(player_info, 'voting_target'):
                    target = player_info.voting_target
                    if target and target in self.get_alive_players():
                        return self.create_action_decision(
                            action_type="vote",
                            target=target,
                            reasoning=f"跟随可信玩家{trusted_player}投票{target}",
                            confidence=0.6,
                            priority=6
                        )
        
        return self._evidence_based_voting(reasoning)
    
    def _leader_following_voting(self, reasoning: VillagerReasoning) -> ActionDecision:
        """跟随领导者的投票"""
        if self.strategy_state['trusted_players']:
            # 选择最可信的玩家作为领导者
            leader = self.strategy_state['trusted_players'][0]
            player_info = self.get_player_info(leader)
            
            if player_info and hasattr(player_info, 'voting_target'):
                target = player_info.voting_target
                if target and target in self.get_alive_players():
                    return self.create_action_decision(
                        action_type="vote",
                        target=target,
                        reasoning=f"跟随领导者{leader}投票{target}",
                        confidence=0.5,
                        priority=5
                    )
        
        return self._evidence_based_voting(reasoning)
    
    def _default_voting(self, reasoning: VillagerReasoning) -> ActionDecision:
        """默认投票"""
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
    
    def add_trusted_player(self, player: str) -> None:
        """添加可信玩家"""
        if player not in self.strategy_state['trusted_players']:
            self.strategy_state['trusted_players'].append(player)
            self.logger.info(f"添加可信玩家: {player}")
    
    def remove_trusted_player(self, player: str) -> None:
        """移除可信玩家"""
        if player in self.strategy_state['trusted_players']:
            self.strategy_state['trusted_players'].remove(player)
            self.logger.info(f"移除可信玩家: {player}")
    
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
    
    def record_speech_pattern(self, player: str, pattern: Dict[str, Any]) -> None:
        """记录发言模式"""
        self.strategy_state['speech_patterns'][player] = pattern
        self.logger.debug(f"记录发言模式: {player}", pattern)
    
    def record_voting_pattern(self, player: str, pattern: Dict[str, Any]) -> None:
        """记录投票模式"""
        self.strategy_state['voting_patterns'][player] = pattern
        self.logger.debug(f"记录投票模式: {player}", pattern)
    
    def analyze_logical_consistency(self, player: str, consistency_score: float) -> None:
        """分析逻辑一致性"""
        self.strategy_state['logical_consistency'][player] = consistency_score
        self.logger.debug(f"逻辑一致性分析: {player} = {consistency_score}")
    
    def enable_coalition_building(self) -> None:
        """启用联盟建设"""
        self.strategy_state['coalition_building'] = True
        self.logger.info("启用联盟建设")
    
    def disable_coalition_building(self) -> None:
        """禁用联盟建设"""
        self.strategy_state['coalition_building'] = False
        self.logger.info("禁用联盟建设")
    
    def enable_leadership_following(self) -> None:
        """启用领导者跟随"""
        self.strategy_state['leadership_following'] = True
        self.logger.info("启用领导者跟随")
    
    def disable_leadership_following(self) -> None:
        """禁用领导者跟随"""
        self.strategy_state['leadership_following'] = False
        self.logger.info("禁用领导者跟随")
    
    def update_analysis_focus(self, focus: str) -> None:
        """更新分析重点"""
        valid_focuses = ["behavioral", "logical", "voting"]
        if focus in valid_focuses:
            self.strategy_state['analysis_focus'] = focus
            self.logger.info(f"更新分析重点: {focus}")
    
    def update_voting_strategy(self, strategy: str) -> None:
        """更新投票策略"""
        valid_strategies = ["evidence_based", "coalition_based", "leader_following"]
        if strategy in valid_strategies:
            self.strategy_state['voting_strategy'] = strategy
            self.logger.info(f"更新投票策略: {strategy}")
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """获取分析摘要"""
        return {
            'trusted_players': self.strategy_state['trusted_players'].copy(),
            'suspected_werewolves': self.strategy_state['suspected_werewolves'].copy(),
            'analysis_focus': self.strategy_state['analysis_focus'],
            'voting_strategy': self.strategy_state['voting_strategy'],
            'coalition_building': self.strategy_state['coalition_building'],
            'speech_patterns': self.strategy_state['speech_patterns'].copy(),
            'voting_patterns': self.strategy_state['voting_patterns'].copy(),
            'logical_consistency': self.strategy_state['logical_consistency'].copy()
        }
    
    def reset_analysis_state(self) -> None:
        """重置分析状态"""
        self.strategy_state['speech_patterns'].clear()
        self.strategy_state['voting_patterns'].clear()
        self.strategy_state['logical_consistency'].clear()
        self.logger.info("重置分析状态")
