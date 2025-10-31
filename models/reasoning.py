# -*- coding: utf-8 -*-
"""推理模型模块 - 完整实现"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum


class GamePhase(Enum):
    """游戏阶段枚举"""
    DAY = "day"
    NIGHT = "night"
    VOTING = "voting"
    DISCUSSION = "discussion"


class ActionType(Enum):
    """行动类型枚举"""
    SPEAK = "speak"
    VOTE = "vote"
    KILL = "kill"
    CHECK = "check"
    HEAL = "heal"
    POISON = "poison"
    SHOOT = "shoot"
    PROTECT = "protect"


@dataclass
class PlayerInfo:
    """玩家信息"""
    name: str
    role: Optional[str] = None
    status: str = "unknown"  # alive, dead, unknown
    trust_score: float = 0.5  # 信任度 0-1
    suspicion_level: float = 0.3  # 可疑度 0-1
    last_action: Optional[str] = None
    voting_history: List[str] = field(default_factory=list)
    speech_patterns: Dict[str, Any] = field(default_factory=dict)
    
    def update_trust(self, delta: float) -> None:
        """更新信任度"""
        self.trust_score = max(0.0, min(1.0, self.trust_score + delta))
    
    def update_suspicion(self, delta: float) -> None:
        """更新可疑度"""
        self.suspicion_level = max(0.0, min(1.0, self.suspicion_level + delta))
    
    def add_vote(self, target: str) -> None:
        """添加投票记录"""
        self.voting_history.append(target)
        # 保持最近10次投票
        if len(self.voting_history) > 10:
            self.voting_history = self.voting_history[-10:]


@dataclass
class GameObservation:
    """游戏观察"""
    phase: GamePhase
    round: int
    alive_players: List[str]
    dead_players: List[str]
    current_speaker: Optional[str] = None
    last_night_result: Optional[Dict[str, Any]] = None
    voting_results: Optional[Dict[str, str]] = None
    discussion_content: Optional[str] = None
    time_left: Optional[float] = None
    
    def get_player_count(self) -> int:
        """获取玩家总数"""
        return len(self.alive_players) + len(self.dead_players)
    
    def get_alive_count(self) -> int:
        """获取存活玩家数"""
        return len(self.alive_players)
    
    def is_critical_phase(self) -> bool:
        """判断是否为关键阶段"""
        return self.get_alive_count() <= 4


@dataclass
class ActionDecision:
    """行动决策"""
    action_type: ActionType
    target: Optional[str] = None
    reasoning: str = ""
    confidence: float = 0.5
    priority: int = 5  # 1-10, 10为最高优先级
    content: str = ""
    expected_outcome: Optional[str] = None
    risk_assessment: float = 0.5
    
    def is_valid(self) -> bool:
        """检查决策是否有效"""
        return (
            0.0 <= self.confidence <= 1.0 and
            1 <= self.priority <= 10 and
            0.0 <= self.risk_assessment <= 1.0
        )


@dataclass
class ThreatAssessment:
    """威胁评估"""
    player_name: str
    threat_level: float  # 0-1
    threat_type: str  # direct, indirect, potential
    reasons: List[str] = field(default_factory=list)
    counter_measures: List[str] = field(default_factory=list)
    
    def add_reason(self, reason: str) -> None:
        """添加威胁原因"""
        if reason not in self.reasons:
            self.reasons.append(reason)
    
    def add_counter_measure(self, measure: str) -> None:
        """添加应对措施"""
        if measure not in self.counter_measures:
            self.counter_measures.append(measure)


@dataclass
class VotingAnalysis:
    """投票分析"""
    voting_patterns: Dict[str, List[str]] = field(default_factory=dict)
    alliances: Dict[str, List[str]] = field(default_factory=dict)
    betrayals: List[str] = field(default_factory=list)
    consistency_scores: Dict[str, float] = field(default_factory=dict)
    
    def add_vote(self, voter: str, target: str) -> None:
        """添加投票记录"""
        if voter not in self.voting_patterns:
            self.voting_patterns[voter] = []
        self.voting_patterns[voter].append(target)
    
    def calculate_consistency(self, player: str) -> float:
        """计算投票一致性"""
        if player not in self.voting_patterns or len(self.voting_patterns[player]) < 2:
            return 0.5
        
        votes = self.voting_patterns[player]
        # 计算投票目标的多样性
        unique_targets = len(set(votes))
        total_votes = len(votes)
        
        # 一致性 = 1 - (多样性/总数)
        consistency = 1.0 - (unique_targets / total_votes)
        return max(0.0, min(1.0, consistency))


@dataclass
class InformationAnalysis:
    """信息分析"""
    known_roles: Dict[str, str] = field(default_factory=dict)
    suspected_roles: Dict[str, str] = field(default_factory=dict)
    verified_information: List[str] = field(default_factory=list)
    rumors: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    
    def add_known_role(self, player: str, role: str) -> None:
        """添加已知角色"""
        self.known_roles[player] = role
    
    def add_suspected_role(self, player: str, role: str, confidence: float = 0.5) -> None:
        """添加疑似角色"""
        self.suspected_roles[player] = role
    
    def verify_information(self, info: str) -> None:
        """验证信息"""
        if info not in self.verified_information:
            self.verified_information.append(info)
    
    def add_rumor(self, rumor: str) -> None:
        """添加谣言"""
        if rumor not in self.rumors:
            self.rumors.append(rumor)
    
    def check_contradiction(self, statement: str) -> bool:
        """检查矛盾"""
        # 简化的矛盾检查逻辑
        for verified in self.verified_information:
            if self._is_contradictory(verified, statement):
                if statement not in self.contradictions:
                    self.contradictions.append(statement)
                return True
        return False
    
    def _is_contradictory(self, info1: str, info2: str) -> bool:
        """检查两条信息是否矛盾"""
        # 简化的矛盾检测
        if "是狼人" in info1 and "不是狼人" in info2:
            return True
        if "是好人" in info1 and "不是好人" in info2:
            return True
        return False


@dataclass
class StrategicPlan:
    """战略计划"""
    short_term_goals: List[str] = field(default_factory=list)
    long_term_goals: List[str] = field(default_factory=list)
    immediate_actions: List[ActionDecision] = field(default_factory=list)
    contingency_plans: Dict[str, ActionDecision] = field(default_factory=dict)
    success_probability: float = 0.5
    
    def add_short_term_goal(self, goal: str) -> None:
        """添加短期目标"""
        if goal not in self.short_term_goals:
            self.short_term_goals.append(goal)
    
    def add_long_term_goal(self, goal: str) -> None:
        """添加长期目标"""
        if goal not in self.long_term_goals:
            self.long_term_goals.append(goal)
    
    def add_immediate_action(self, action: ActionDecision) -> None:
        """添加立即行动"""
        self.immediate_actions.append(action)
        # 按优先级排序
        self.immediate_actions.sort(key=lambda x: x.priority, reverse=True)
    
    def add_contingency_plan(self, scenario: str, action: ActionDecision) -> None:
        """添加应急计划"""
        self.contingency_plans[scenario] = action


@dataclass
class RoleSpecificReasoning:
    """角色特定推理基类"""
    role: str
    phase: GamePhase
    situation_assessment: str
    immediate_action: str
    long_term_strategy: str
    allies: List[str] = field(default_factory=list)
    enemies: List[str] = field(default_factory=list)
    neutral_players: List[str] = field(default_factory=list)
    threat_assessment: List[ThreatAssessment] = field(default_factory=list)
    information_analysis: InformationAnalysis = field(default_factory=InformationAnalysis)
    voting_analysis: VotingAnalysis = field(default_factory=VotingAnalysis)
    strategic_plan: StrategicPlan = field(default_factory=StrategicPlan)
    
    def add_threat(self, player: str, threat_level: float, threat_type: str, reasons: List[str]) -> None:
        """添加威胁评估"""
        threat = ThreatAssessment(
            player_name=player,
            threat_level=threat_level,
            threat_type=threat_type,
            reasons=reasons
        )
        self.threat_assessment.append(threat)
    
    def get_highest_threat(self) -> Optional[ThreatAssessment]:
        """获取最高威胁"""
        if not self.threat_assessment:
            return None
        return max(self.threat_assessment, key=lambda x: x.threat_level)


@dataclass
class WerewolfReasoning(RoleSpecificReasoning):
    """狼人推理"""
    teammates: List[str] = field(default_factory=list)
    night_targets: List[str] = field(default_factory=list)
    deception_strategy: str = "stealth"  # stealth, aggressive, defensive
    exposure_risk: float = 0.0
    fake_seer_mode: bool = False
    seer_claims: List[str] = field(default_factory=list)
    teammate_coordination: str = "independent"  # independent, coordinated, split
    
    def __post_init__(self):
        """初始化后处理"""
        self.role = "werewolf"


@dataclass
class SeerReasoning(RoleSpecificReasoning):
    """预言家推理"""
    checked_players: Dict[str, str] = field(default_factory=dict)  # player -> role
    seer_plan: str = "conservative"  # conservative, aggressive, balanced
    reveal_strategy: str = "cautious"  # cautious, immediate, strategic
    badge_flow: List[str] = field(default_factory=list)  # 警徽流
    credibility_score: float = 0.8
    
    def __post_init__(self):
        """初始化后处理"""
        self.role = "seer"
    
    def add_check_result(self, player: str, role: str) -> None:
        """添加查验结果"""
        self.checked_players[player] = role
        self.information_analysis.add_known_role(player, role)
    
    def should_reveal_identity(self) -> bool:
        """判断是否应该暴露身份"""
        # 基于局势判断是否暴露身份
        if len(self.enemies) >= len(self.allies):
            return True
        if self.credibility_score < 0.5:
            return False
        return self.reveal_strategy == "immediate"


@dataclass
class WitchReasoning(RoleSpecificReasoning):
    """女巫推理"""
    has_poison: bool = True
    has_antidote: bool = True
    poison_used: bool = False
    antidote_used: bool = False
    heal_strategy: str = "selective"  # selective, conservative, aggressive
    poison_strategy: str = "strategic"  # strategic, defensive, revenge
    saved_players: List[str] = field(default_factory=list)
    poisoned_players: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初始化后处理"""
        self.role = "witch"
    
    def should_use_antidote(self, target: str) -> bool:
        """判断是否使用解药"""
        if not self.has_antidote or self.antidote_used:
            return False
        
        # 基于策略判断
        if self.heal_strategy == "conservative":
            return target in self.allies
        elif self.heal_strategy == "aggressive":
            return True  # 总是救
        else:  # selective
            return target in self.allies or len(self.allies) > len(self.enemies)
    
    def should_use_poison(self, target: str) -> bool:
        """判断是否使用毒药"""
        if not self.has_poison or self.poison_used:
            return False
        
        # 基于策略判断
        if self.poison_strategy == "strategic":
            return target in self.enemies
        elif self.poison_strategy == "defensive":
            return len(self.enemies) > len(self.allies)
        else:  # revenge
            return target in self.enemies and len(self.enemies) <= 2
    
    def use_antidote(self, target: str) -> None:
        """使用解药"""
        if self.should_use_antidote(target):
            self.antidote_used = True
            self.saved_players.append(target)
            return True
        return False
    
    def use_poison(self, target: str) -> None:
        """使用毒药"""
        if self.should_use_poison(target):
            self.poison_used = True
            self.poisoned_players.append(target)
            return True
        return False


@dataclass
class HunterReasoning(RoleSpecificReasoning):
    """猎人推理"""
    has_shot: bool = True
    shot_used: bool = False
    shot_strategy: str = "strategic"  # strategic, revenge, random
    shot_targets: List[str] = field(default_factory=list)
    death_trigger: str = "unknown"  # vote, kill, poison
    
    def __post_init__(self):
        """初始化后处理"""
        self.role = "hunter"
    
    def should_shoot(self) -> bool:
        """判断是否应该开枪"""
        if not self.has_shot or self.shot_used:
            return False
        
        # 基于策略判断
        if self.shot_strategy == "strategic":
            return len(self.enemies) > 0
        elif self.shot_strategy == "revenge":
            return self.death_trigger in ["vote", "kill"]
        else:  # random
            return True
    
    def select_target(self) -> Optional[str]:
        """选择开枪目标"""
        if not self.should_shoot():
            return None
        
        if self.shot_strategy == "strategic":
            # 选择威胁最大的敌人
            if self.enemies:
                return self.enemies[0]
        elif self.shot_strategy == "revenge":
            # 选择投票杀死自己的玩家
            # 这里需要更多信息，简化处理
            if self.enemies:
                return self.enemies[0]
        else:  # random
            import random
            all_players = self.allies + self.enemies + self.neutral_players
            if all_players:
                return random.choice(all_players)
        
        return None
    
    def use_shot(self, target: str) -> bool:
        """使用开枪技能"""
        selected_target = self.select_target()
        if selected_target and selected_target == target:
            self.shot_used = True
            self.shot_targets.append(target)
            return True
        return False


@dataclass
class VillagerReasoning(RoleSpecificReasoning):
    """村民推理"""
    analysis_level: str = "basic"  # basic, advanced, expert
    analysis_focus: str = "behavioral"  # behavioral, logical, voting (兼容旧代码)
    voting_strategy: str = "logical"  # logical, emotional, random
    leadership_tendency: float = 0.5
    suspicion_method: str = "behavioral"  # behavioral, voting, speech
    information_gathering: str = "active"  # active, passive
    coalition_building: bool = False
    
    def __post_init__(self):
        """初始化后处理"""
        self.role = "villager"
    
    def analyze_suspicion(self, player: str) -> float:
        """分析玩家可疑度"""
        suspicion = 0.3  # 基础可疑度
        
        # 基于投票模式分析
        if self.suspicion_method in ["behavioral", "voting"]:
            voting_consistency = self.voting_analysis.calculate_consistency(player)
            if voting_consistency > 0.8:
                suspicion += 0.2  # 投票过于一致可能有问题
        
        # 基于发言模式分析
        if self.suspicion_method in ["behavioral", "speech"]:
            # 这里需要更多发言分析逻辑
            pass
        
        return min(1.0, suspicion)
    
    def should_take_leadership(self) -> bool:
        """判断是否应该承担领导角色"""
        return (
            self.leadership_tendency > 0.7 and
            len(self.allies) >= len(self.enemies) and
            self.analysis_level in ["advanced", "expert"]
        )


# 导出的类和枚举
__all__ = [
    'GamePhase',
    'ActionType',
    'PlayerInfo',
    'GameObservation',
    'ActionDecision',
    'ThreatAssessment',
    'VotingAnalysis',
    'InformationAnalysis',
    'StrategicPlan',
    'RoleSpecificReasoning',
    'WerewolfReasoning',
    'SeerReasoning',
    'WitchReasoning',
    'HunterReasoning',
    'VillagerReasoning'
]
