# -*- coding: utf-8 -*-
"""狼人策略模块"""

import random
from typing import Dict, List, Any, Optional
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    WerewolfReasoning,
    StrategicPlan
)
from strategies.base_strategy import BaseStrategy
from utils.logger import WerewolfLogger


class WerewolfStrategy(BaseStrategy):
    """狼人策略实现"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        super().__init__(agent_name, logger)
        
        # 狼人特有状态
        self.strategy_state.update({
            'teammates': [],  # 已知的队友
            'night_targets': [],  # 历史夜晚目标
            'deception_level': 0.5,  # 欺骗程度
            'exposure_risk': 0.0,  # 暴露风险
            'last_night_kill': None,  # 昨晚击杀目标
            'self_harm_cooldown': 0,  # 自刀冷却
            'fake_seer_mode': False,  # 悍跳模式
            'seer_claims': [],  # 宣称先知的玩家
            'voted_werewolves': []  # 被投票的狼人
        })
    
    def get_role_name(self) -> str:
        """获取角色名称"""
        return "werewolf"
    
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        if observation.phase != "night":
            return None
        
        alive_players = self.get_alive_players()
        if not alive_players:
            return None
        
        # 分析局势
        reasoning = self.analyze_situation(observation)
        
        # 选择击杀目标
        target = self._select_night_target(alive_players, reasoning)
        
        if target:
            self.strategy_state['last_night_kill'] = target
            self.strategy_state['night_targets'].append(target)
            
            return self.create_action_decision(
                action_type="kill",
                target=target,
                reasoning=f"基于威胁评估选择击杀{target}",
                confidence=0.8,
                priority=9,
                content=f"击杀{target}"
            )
        
        return None
    
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        reasoning = self.analyze_situation(observation)
        
        # 根据局势选择发言策略
        if reasoning.exposure_risk > 0.7:
            return self._defensive_speech(reasoning)
        elif reasoning.fake_seer_mode:
            return self._fake_seer_speech(reasoning)
        else:
            return self._normal_deceptive_speech(reasoning)
    
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        reasoning = self.analyze_situation(observation)
        
        # 选择投票目标
        target = self._select_voting_target(reasoning)
        
        if target:
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning=self._generate_voting_reasoning(target, reasoning),
                confidence=0.7,
                priority=8
            )
        
        # 默认投票给最可疑的好人
        suspicious_good = self._get_most_suspicious_good_player()
        if suspicious_good:
            return self.create_action_decision(
                action_type="vote",
                target=suspicious_good,
                reasoning=f"基于分析，{suspicious_good}最可疑",
                confidence=0.6,
                priority=6
            )
        
        # 随机投票
        alive_players = self.get_alive_players()
        if alive_players:
            target = random.choice(alive_players)
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning="随机投票",
                confidence=0.3,
                priority=3
            )
        
        return self.create_action_decision(
            action_type="speak",
            content="弃权",
            confidence=0.1,
            priority=1
        )
    
    def analyze_situation(self, observation: GameObservation) -> WerewolfReasoning:
        """分析当前局势"""
        alive_players = self.get_alive_players()
        dead_players = self.get_dead_players()
        
        # 评估威胁等级
        threats = self._assess_threats(alive_players)
        
        # 计算暴露风险
        exposure_risk = self._calculate_exposure_risk()
        
        # 制定欺骗策略
        deception_strategy = self._plan_deception_strategy(threats, exposure_risk)
        
        # 队友协调
        teammate_coordination = self._plan_teammate_coordination()
        
        return WerewolfReasoning(
            role="werewolf",
            phase=observation.phase,
            situation_assessment=self._assess_overall_situation(alive_players, dead_players),
            immediate_action=self._determine_immediate_action(observation),
            long_term_strategy=self._plan_long_term_strategy(),
            allies=self.strategy_state['teammates'],
            enemies=threats,
            neutral_players=self._get_neutral_players(alive_players, threats),
            night_targets=self.strategy_state['night_targets'],
            deception_strategy=deception_strategy,
            teammate_coordination=teammate_coordination,
            exposure_risk=exposure_risk
        )
    
    def _select_night_target(self, alive_players: List[str], reasoning: Optional[WerewolfReasoning]) -> Optional[str]:
        """选择夜晚击杀目标"""
        if not alive_players:
            return None
        
        # 优先级排序
        target_scores = {}
        
        for player in alive_players:
            score = 0.0
            
            player_info = self.get_player_info(player)
            if not player_info:
                continue
            
            # 威胁等级权重
            if player_info.role in ['seer', 'witch', 'hunter']:
                score += 0.4  # 特殊角色优先
            
            # 可信度权重（可信的好人更危险）
            score += player_info.trust_score * 0.3
            
            # 发言活跃度权重
            if hasattr(player_info, 'last_action') and player_info.last_action:
                score += 0.2
            
            # 避免连续击杀同一玩家
            if player == self.strategy_state.get('last_night_kill'):
                score -= 0.2
            
            # 随机因素
            score += random.random() * 0.1
            
            target_scores[player] = score
        
        if target_scores:
            # 选择得分最高的目标
            best_target = max(target_scores, key=target_scores.get)
            return best_target
        
        return random.choice(alive_players) if alive_players else None
    
    def _select_voting_target(self, reasoning: WerewolfReasoning) -> Optional[str]:
        """选择投票目标"""
        alive_players = self.get_alive_players()
        
        # 如果在悍跳模式，投票给威胁最大的好人
        if self.strategy_state['fake_seer_mode']:
            threats = [p for p in alive_players if self.get_player_info(p).role in ['seer', 'witch', 'hunter']]
            if threats:
                return random.choice(threats)
        
        # 投票给最可疑的好人
        suspicious_good = self._get_most_suspicious_good_player()
        if suspicious_good:
            return suspicious_good
        
        # 投票给非队友
        non_teammates = [p for p in alive_players if p not in self.strategy_state['teammates']]
        if non_teammates:
            # 选择最可疑的
            most_suspicious = self.get_most_suspicious_players(1)
            if most_suspicious and most_suspicious[0] in non_teammates:
                return most_suspicious[0]
            return random.choice(non_teammates)
        
        return None
    
    def _get_most_suspicious_good_player(self) -> Optional[str]:
        """获取最可疑的好人玩家"""
        alive_players = self.get_alive_players()
        good_players = []
        
        for player in alive_players:
            player_info = self.get_player_info(player)
            if player_info and player_info.role not in ['werewolf']:
                good_players.append((player, player_info.suspicion_level))
        
        if good_players:
            good_players.sort(key=lambda x: x[1], reverse=True)
            return good_players[0][0]
        
        return None
    
    def _assess_threats(self, alive_players: List[str]) -> List[str]:
        """评估威胁玩家"""
        threats = []
        
        for player in alive_players:
            player_info = self.get_player_info(player)
            if not player_info:
                continue
            
            # 特殊角色是主要威胁
            if player_info.role in ['seer', 'witch', 'hunter']:
                threats.append(player)
            # 高可信度的玩家也是威胁
            elif player_info.trust_score > 0.7:
                threats.append(player)
        
        return threats
    
    def _calculate_exposure_risk(self) -> float:
        """计算暴露风险"""
        risk = 0.0
        
        # 基于队友数量
        teammate_count = len(self.strategy_state['teammates'])
        if teammate_count == 0:
            risk += 0.2  # 不知道队友时风险较高
        elif teammate_count == 1:
            risk += 0.1
        
        # 基于被投票的狼人数量
        voted_werewolves = len(self.strategy_state['voted_werewolves'])
        risk += voted_werewolves * 0.3
        
        # 基于宣称先知的玩家数量
        seer_claims = len(self.strategy_state['seer_claims'])
        risk += seer_claims * 0.2
        
        return min(1.0, risk)
    
    def _plan_deception_strategy(self, threats: List[str], exposure_risk: float) -> str:
        """规划欺骗策略"""
        if exposure_risk > 0.7:
            return "defensive"  # 防守型
        elif len(threats) >= 2:
            return "aggressive"  # 激进型
        elif self.strategy_state['fake_seer_mode']:
            return "fake_seer"  # 悍跳先知
        else:
            return "stealth"  # 隐藏型
    
    def _plan_teammate_coordination(self) -> str:
        """规划队友协调"""
        teammate_count = len(self.strategy_state['teammates'])
        
        if teammate_count == 0:
            return "search_for_teammates"
        elif teammate_count == 1:
            return "coordinate_with_single_teammate"
        else:
            return "full_team_coordination"
    
    def _assess_overall_situation(self, alive_players: List[str], dead_players: List[str]) -> str:
        """评估整体局势"""
        total_players = len(alive_players) + len(dead_players)
        werewolf_count = len(self.strategy_state['teammates']) + 1  # +1 for self
        
        if len(alive_players) <= 4:
            return "critical"  # 关键时刻
        elif werewolf_count >= len(alive_players) // 2:
            return "advantage"  # 优势
        elif werewolf_count <= 2:
            return "disadvantage"  # 劣势
        else:
            return "balanced"  # 均势
    
    def _determine_immediate_action(self, observation: GameObservation) -> str:
        """确定立即行动"""
        if observation.phase == "night":
            return "select_kill_target"
        elif observation.phase == "day":
            if self.strategy_state['fake_seer_mode']:
                return "maintain_fake_seer_act"
            else:
                return "deceive_and_blend"
        else:
            return "observe_and_analyze"
    
    def _plan_long_term_strategy(self) -> str:
        """规划长期策略"""
        exposure_risk = self.strategy_state['exposure_risk']
        
        if exposure_risk > 0.6:
            return "survival_focused"
        elif len(self.strategy_state['teammates']) >= 2:
            return "domination_strategy"
        else:
            return "infiltration_strategy"
    
    def _get_neutral_players(self, alive_players: List[str], threats: List[str]) -> List[str]:
        """获取中立玩家"""
        return [p for p in alive_players if p not in threats and p not in self.strategy_state['teammates']]
    
    def _generate_voting_reasoning(self, target: str, reasoning: WerewolfReasoning) -> str:
        """生成投票理由"""
        player_info = self.get_player_info(target)
        
        if player_info and player_info.role in ['seer', 'witch', 'hunter']:
            return f"{target}是特殊角色，对狼人阵营威胁很大"
        elif player_info and player_info.trust_score > 0.7:
            return f"{target}在玩家中可信度很高，可能是关键好人"
        else:
            return f"基于发言分析，{target}的行为很可疑"
    
    def _defensive_speech(self, reasoning: WerewolfReasoning) -> str:
        """防守型发言"""
        speeches = [
            "我觉得我们需要更仔细地分析，不要急于投票。",
            "作为普通村民，我会努力找出狼人，但需要更多证据。",
            "大家冷静分析，避免被误导。",
            "我注意到有些玩家的发言有矛盾，需要进一步观察。"
        ]
        return random.choice(speeches)
    
    def _fake_seer_speech(self, reasoning: WerewolfReasoning) -> str:
        """悍跳先知发言"""
        # 选择一个"查验"目标
        alive_players = self.get_alive_players()
        if alive_players:
            target = random.choice(alive_players)
            return f"作为先知，我昨晚查验了{target}，他是狼人！"
        return "我是先知，会为大家提供准确信息。"
    
    def _normal_deceptive_speech(self, reasoning: WerewolfReasoning) -> str:
        """普通欺骗发言"""
        speeches = [
            "我认为我们应该重点关注那些发言较少的玩家。",
            "从逻辑角度分析，某些玩家的行为确实可疑。",
            "我会仔细观察每个人的投票模式。",
            "作为村民，我的目标是找出所有狼人。"
        ]
        return random.choice(speeches)
    
    def add_teammate(self, teammate_name: str) -> None:
        """添加队友"""
        if teammate_name not in self.strategy_state['teammates']:
            self.strategy_state['teammates'].append(teammate_name)
            self.logger.info(f"发现队友: {teammate_name}")
    
    def add_seer_claim(self, player_name: str) -> None:
        """添加宣称先知的玩家"""
        if player_name not in self.strategy_state['seer_claims']:
            self.strategy_state['seer_claims'].append(player_name)
            self.logger.info(f"玩家宣称先知: {player_name}")
    
    def enable_fake_seer_mode(self) -> None:
        """启用悍跳模式"""
        self.strategy_state['fake_seer_mode'] = True
        self.logger.info("启用悍跳先知模式")
    
    def disable_fake_seer_mode(self) -> None:
        """禁用悍跳模式"""
        self.strategy_state['fake_seer_mode'] = False
        self.logger.info("禁用悍跳先知模式")
    
    def consider_self_harm(self) -> bool:
        """考虑自刀策略"""
        # 只在特定情况下考虑自刀
        if self.strategy_state['self_harm_cooldown'] > 0:
            return False
        
        # 如果女巫还有解药且局势不利
        # 这里简化逻辑，实际应该更复杂
        return random.random() < 0.1  # 10%概率
    
    def execute_self_harm_strategy(self) -> Optional[ActionDecision]:
        """执行自刀策略"""
        if self.consider_self_harm():
            self.strategy_state['self_harm_cooldown'] = 3  # 冷却3轮
            return self.create_action_decision(
                action_type="kill",
                target=self.agent_name,
                reasoning="自刀骗取女巫解药",
                confidence=0.6,
                priority=7
            )
        return None
