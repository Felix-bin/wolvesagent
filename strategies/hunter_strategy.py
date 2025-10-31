# -*- coding: utf-8 -*-
"""猎人策略模块"""

import random
from typing import Dict, List, Any, Optional
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    HunterReasoning,
    StrategicPlan
)
from strategies.base_strategy import BaseStrategy
from utils.logger import WerewolfLogger


class HunterStrategy(BaseStrategy):
    """猎人策略实现"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        super().__init__(agent_name, logger)
        
        # 猎人特有状态
        self.strategy_state.update({
            'shot_used': False,           # 是否已开枪
            'death_triggered': False,       # 是否触发死亡
            'shot_target': None,           # 开枪目标
            'threat_assessment': {},        # 威胁评估
            'legacy_players': [],          # 遗志玩家列表
            'death_timing_strategy': 'immediate',  # 死亡时机策略
            'threat_elimination_priority': [],  # 威胁消除优先级
            'final_words': '',            # 遗言
            'shot_history': []            # 开枪历史
        })
    
    def get_role_name(self) -> str:
        """获取角色名称"""
        return "hunter"
    
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        # 猎人夜晚没有特殊行动
        return None
    
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        reasoning = self.analyze_situation(observation)
        
        # 根据死亡时机策略选择发言
        if reasoning.death_timing == "immediate":
            return self._immediate_strategy_speech(reasoning)
        elif reasoning.death_timing == "strategic":
            return self._strategic_timing_speech(reasoning)
        else:
            return self._conservative_speech(reasoning)
    
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        reasoning = self.analyze_situation(observation)
        
        # 优先投票给威胁最大的玩家
        if self.strategy_state['threat_elimination_priority']:
            target = self._select_threat_target()
            if target:
                return self.create_action_decision(
                    action_type="vote",
                    target=target,
                    reasoning=f"{target}是最大威胁，必须消除",
                    confidence=0.8,
                    priority=9
                )
        
        # 投票给最可疑的玩家
        suspicious_players = self.get_most_suspicious_players(3)
        if suspicious_players:
            target = suspicious_players[0]
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning=f"基于分析，{target}最可疑",
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
    
    def analyze_situation(self, observation: GameObservation) -> HunterReasoning:
        """分析当前局势"""
        alive_players = self.get_alive_players()
        dead_players = self.get_dead_players()
        
        # 评估威胁等级
        threats = self._assess_threats(alive_players)
        
        # 确定死亡时机策略
        death_timing = self._determine_death_timing()
        
        # 威胁消除策略
        threat_elimination = self._plan_threat_elimination(threats)
        
        # 遗志规划
        legacy_planning = self._plan_legacy()
        
        return HunterReasoning(
            role="hunter",
            phase=observation.phase,
            situation_assessment=self._assess_overall_situation(alive_players, dead_players),
            immediate_action=self._determine_immediate_action(observation),
            long_term_strategy=self._plan_long_term_strategy(),
            allies=self._get_allies(),
            enemies=threats,
            neutral_players=self._get_neutral_players(alive_players, threats),
            shot_target=self._select_shot_target(),
            death_timing=death_timing,
            threat_elimination=threat_elimination,
            legacy_planning=legacy_planning
        )
    
    def _select_shot_target(self) -> Optional[str]:
        """选择开枪目标"""
        if self.strategy_state['shot_used']:
            return None
        
        # 如果有威胁消除优先级
        if self.strategy_state['threat_elimination_priority']:
            return self.strategy_state['threat_elimination_priority'][0]
        
        # 选择最可疑的玩家
        suspicious_players = self.get_most_suspicious_players(3)
        if suspicious_players:
            return suspicious_players[0]
        
        # 选择威胁最大的玩家
        threats = self._assess_threats(self.get_alive_players())
        if threats:
            return threats[0]
        
        return None
    
    def _select_threat_target(self) -> Optional[str]:
        """选择威胁目标"""
        if not self.strategy_state['threat_elimination_priority']:
            return None
        
        # 选择优先级最高的威胁
        return self.strategy_state['threat_elimination_priority'][0]
    
    def _assess_threats(self, alive_players: List[str]) -> List[str]:
        """评估威胁玩家"""
        threats = []
        
        for player in alive_players:
            player_info = self.get_player_info(player)
            if not player_info:
                continue
            
            threat_score = 0.0
            
            # 高可疑度是威胁
            threat_score += player_info.suspicion_level * 0.4
            
            # 低信任度是威胁
            threat_score += (1.0 - player_info.trust_score) * 0.3
            
            # 发言模式分析
            if hasattr(player_info, 'last_action') and player_info.last_action:
                # 如果经常指控他人，可能是威胁
                if "怀疑" in str(player_info.last_action) or "accuse" in str(player_info.last_action).lower():
                    threat_score += 0.2
            
            # 如果威胁分数高，加入威胁列表
            if threat_score > 0.6:
                threats.append(player)
                self.strategy_state['threat_assessment'][player] = threat_score
        
        # 按威胁分数排序
        threats.sort(key=lambda x: self.strategy_state['threat_assessment'].get(x, 0), reverse=True)
        
        return threats
    
    def _determine_death_timing(self) -> str:
        """确定死亡时机策略"""
        alive_count = len(self.get_alive_players())
        
        # 如果存活玩家很少，立即死亡
        if alive_count <= 4:
            return "immediate"
        # 如果有明确威胁，策略性死亡
        elif self.strategy_state['threat_elimination_priority']:
            return "strategic"
        else:
            return "conservative"
    
    def _plan_threat_elimination(self, threats: List[str]) -> str:
        """规划威胁消除策略"""
        if not threats:
            return "no_clear_threats"
        elif len(threats) >= 2:
            return "multiple_threat_elimination"
        elif len(threats) == 1:
            return "single_threat_elimination"
        else:
            return "threat_assessment_phase"
    
    def _plan_legacy(self) -> str:
        """规划遗志"""
        if self.strategy_state['shot_used']:
            return "legacy_communicated"
        elif self.strategy_state['threat_elimination_priority']:
            return "prepare_final_message"
        else:
            return "information_gathering"
    
    def _assess_overall_situation(self, alive_players: List[str], dead_players: List[str]) -> str:
        """评估整体局势"""
        if len(alive_players) <= 4:
            return "critical_phase"
        elif len(self.strategy_state['threat_elimination_priority']) >= 2:
            return "high_threat_situation"
        elif self.strategy_state['shot_used']:
            return "post_shot_phase"
        else:
            return "normal_hunting_phase"
    
    def _determine_immediate_action(self, observation: GameObservation) -> str:
        """确定立即行动"""
        if observation.phase == "night":
            return "observe_and_plan"
        elif self.strategy_state['death_triggered']:
            return "execute_shot"
        else:
            return "analyze_and_vote"
    
    def _plan_long_term_strategy(self) -> str:
        """规划长期策略"""
        if self.strategy_state['shot_used']:
            return "post_shot_strategy"
        elif len(self.strategy_state['threat_elimination_priority']) > 0:
            return "threat_elimination_focused"
        else:
            return "information_and_timing_strategy"
    
    def _get_allies(self) -> List[str]:
        """获取盟友列表"""
        allies = []
        for player_name, player_info in self.player_info.items():
            if (player_info.trust_score > 0.7 and 
                player_info.suspicion_level < 0.3):
                allies.append(player_name)
        return allies
    
    def _get_neutral_players(self, alive_players: List[str], threats: List[str]) -> List[str]:
        """获取中立玩家"""
        return [p for p in alive_players if p not in threats]
    
    def _immediate_strategy_speech(self, reasoning: HunterReasoning) -> str:
        """立即策略发言"""
        speeches = [
            "我有一些重要信息需要分享。",
            "基于我的观察，某些玩家很可疑。",
            "我会在关键时刻采取行动。",
            "请大家仔细分析投票模式。"
        ]
        return random.choice(speeches)
    
    def _strategic_timing_speech(self, reasoning: HunterReasoning) -> str:
        """策略时机发言"""
        speeches = [
            "我正在等待最佳时机采取行动。",
            "从逻辑角度，我们需要更多信息。",
            "某些玩家的行为模式值得注意。",
            "我会根据局势发展做出决定。"
        ]
        return random.choice(speeches)
    
    def _conservative_speech(self, reasoning: HunterReasoning) -> str:
        """保守发言"""
        speeches = [
            "我需要更多时间来分析局势。",
            "作为普通村民，我会努力找出狼人。",
            "建议大家理性分析，避免盲目投票。",
            "我会基于证据做出判断。"
        ]
        return random.choice(speeches)
    
    def trigger_death(self) -> Optional[ActionDecision]:
        """触发死亡并开枪"""
        if self.strategy_state['shot_used'] or self.strategy_state['death_triggered']:
            return None
        
        self.strategy_state['death_triggered'] = True
        
        # 选择开枪目标
        target = self._select_shot_target()
        if target:
            self.strategy_state['shot_used'] = True
            self.strategy_state['shot_target'] = target
            self.strategy_state['shot_history'].append({
                'target': target,
                'timing': 'death_trigger',
                'round': len(self.strategy_state['shot_history']) + 1
            })
            
            return self.create_action_decision(
                action_type="shoot",
                target=target,
                reasoning=f"死亡时开枪带走{target}",
                confidence=0.9,
                priority=10,
                content=f"开枪带走{target}"
            )
        
        return None
    
    def set_shot_target(self, target: str) -> None:
        """设置开枪目标"""
        self.strategy_state['shot_target'] = target
        self.strategy_state['threat_elimination_priority'].append(target)
        self.logger.info(f"设置开枪目标: {target}")
    
    def add_threat(self, player: str, threat_level: float) -> None:
        """添加威胁玩家"""
        self.strategy_state['threat_assessment'][player] = threat_level
        if player not in self.strategy_state['threat_elimination_priority']:
            self.strategy_state['threat_elimination_priority'].append(player)
        self.logger.info(f"添加威胁: {player} (等级: {threat_level})")
    
    def remove_threat(self, player: str) -> None:
        """移除威胁玩家"""
        if player in self.strategy_state['threat_assessment']:
            del self.strategy_state['threat_assessment'][player]
        
        if player in self.strategy_state['threat_elimination_priority']:
            self.strategy_state['threat_elimination_priority'].remove(player)
        
        self.logger.info(f"移除威胁: {player}")
    
    def set_final_words(self, words: str) -> None:
        """设置遗言"""
        self.strategy_state['final_words'] = words
        self.logger.info(f"设置遗言: {words}")
    
    def get_threat_assessment(self) -> Dict[str, float]:
        """获取威胁评估"""
        return self.strategy_state['threat_assessment'].copy()
    
    def get_shot_status(self) -> Dict[str, Any]:
        """获取开枪状态"""
        return {
            'shot_used': self.strategy_state['shot_used'],
            'shot_target': self.strategy_state['shot_target'],
            'death_triggered': self.strategy_state['death_triggered'],
            'shot_history': self.strategy_state['shot_history'].copy()
        }
    
    def reset_death_trigger(self) -> None:
        """重置死亡触发"""
        self.strategy_state['death_triggered'] = False
        self.logger.info("重置死亡触发状态")
    
    def update_death_timing_strategy(self, strategy: str) -> None:
        """更新死亡时机策略"""
        valid_strategies = ["immediate", "strategic", "conservative"]
        if strategy in valid_strategies:
            self.strategy_state['death_timing_strategy'] = strategy
            self.logger.info(f"更新死亡时机策略: {strategy}")
    
    def create_legacy_message(self) -> str:
        """创建遗志信息"""
        if self.strategy_state['final_words']:
            return self.strategy_state['final_words']
        
        # 根据局势生成遗言
        if self.strategy_state['shot_target']:
            return f"我开枪带走了{self.strategy_state['shot_target']}，相信我的判断。"
        elif self.strategy_state['threat_elimination_priority']:
            threat = self.strategy_state['threat_elimination_priority'][0]
            return f"如果我有机会，我会带走{threat}。请相信我的分析。"
        else:
            return "作为猎人，我尽力为好人阵营做出贡献。请大家继续找出狼人。"
