# -*- coding: utf-8 -*-
"""记忆管理模块 - 完整实现"""

import time
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, deque


@dataclass
class PlayerAction:
    """玩家行为记录"""
    timestamp: float
    action_type: str  # speak, vote, kill, check, poison, resurrect, shoot
    content: Optional[str] = None
    target: Optional[str] = None
    round: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerAction":
        """从字典创建实例"""
        return cls(**data)


@dataclass
class PlayerProfile:
    """玩家画像"""
    name: str
    trust_score: float = 0.5  # 信任度 0-1
    suspicion_level: float = 0.5  # 可疑度 0-1
    role_history: List[str] = None  # 历史角色
    actions: List[PlayerAction] = None  # 行为记录
    behavior_analysis: Dict[str, Any] = None  # 行为分析
    last_seen: float = 0.0  # 最后见到的时间
    
    def __post_init__(self):
        """初始化后处理"""
        if self.role_history is None:
            self.role_history = []
        if self.actions is None:
            self.actions = []
        if self.behavior_analysis is None:
            self.behavior_analysis = {}
        self.last_seen = time.time()
    
    def add_action(self, action: PlayerAction) -> None:
        """添加行为记录"""
        self.actions.append(action)
        self.last_seen = action.timestamp
        # 保持最近50条记录
        if len(self.actions) > 50:
            self.actions = self.actions[-50:]
    
    def update_trust_score(self, delta: float) -> None:
        """更新信任度"""
        self.trust_score = max(0.0, min(1.0, self.trust_score + delta))
    
    def update_suspicion_level(self, delta: float) -> None:
        """更新可疑度"""
        self.suspicion_level = max(0.0, min(1.0, self.suspicion_level + delta))
    
    def add_role_history(self, role: str) -> None:
        """添加角色历史"""
        if role not in self.role_history:
            self.role_history.append(role)
    
    def get_recent_actions(self, count: int = 10) -> List[PlayerAction]:
        """获取最近的行为记录"""
        return self.actions[-count:] if self.actions else []
    
    def analyze_voting_patterns(self) -> Dict[str, Any]:
        """分析投票模式"""
        vote_actions = [a for a in self.actions if a.action_type == "vote"]
        if not vote_actions:
            return {}
        
        # 统计投票目标
        vote_targets = defaultdict(int)
        for action in vote_actions:
            if action.target:
                vote_targets[action.target] += 1
        
        # 分析投票一致性
        recent_votes = vote_actions[-5:] if len(vote_actions) >= 5 else vote_actions
        
        return {
            "total_votes": len(vote_actions),
            "vote_targets": dict(vote_targets),
            "most_voted_target": max(vote_targets.items(), key=lambda x: x[1])[0] if vote_targets else None,
            "recent_consistency": len(set(v.target for v in recent_votes if v.target)) <= 2 if recent_votes else True
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "trust_score": self.trust_score,
            "suspicion_level": self.suspicion_level,
            "role_history": self.role_history,
            "actions": [action.to_dict() for action in self.actions],
            "behavior_analysis": self.behavior_analysis,
            "last_seen": self.last_seen
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PlayerProfile":
        """从字典创建实例"""
        actions = [PlayerAction.from_dict(a) for a in data.get("actions", [])]
        return cls(
            name=data["name"],
            trust_score=data.get("trust_score", 0.5),
            suspicion_level=data.get("suspicion_level", 0.5),
            role_history=data.get("role_history", []),
            actions=actions,
            behavior_analysis=data.get("behavior_analysis", {}),
            last_seen=data.get("last_seen", time.time())
        )


@dataclass
class GameReflection:
    """游戏反思记录"""
    timestamp: float
    game_result: str  # win/lose
    role_performance: Dict[str, Any]
    lessons_learned: List[str]
    strategy_adjustments: List[str]
    opponent_analysis: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GameReflection":
        """从字典创建实例"""
        return cls(**data)


class OpponentProfiler:
    """对手分析器"""
    
    def __init__(self):
        self.profiles: Dict[str, PlayerProfile] = {}
        self.reflection_log: List[GameReflection] = []
        self.game_history: List[Dict[str, Any]] = []
    
    def get_or_create_profile(self, player_name: str) -> PlayerProfile:
        """获取或创建玩家画像"""
        if player_name not in self.profiles:
            self.profiles[player_name] = PlayerProfile(name=player_name)
        return self.profiles[player_name]
    
    def record_action(self, player_name: str, action: PlayerAction) -> None:
        """记录玩家行为"""
        profile = self.get_or_create_profile(player_name)
        profile.add_action(action)
        
        # 根据行为类型更新画像
        self._analyze_action_impact(profile, action)
    
    def update_role_history(self, player_name: str, role: str) -> None:
        """更新角色历史"""
        profile = self.get_or_create_profile(player_name)
        profile.add_role_history(role)
    
    def update_trust_score(self, player_name: str, delta: float) -> None:
        """更新信任度"""
        profile = self.get_or_create_profile(player_name)
        profile.update_trust_score(delta)
    
    def update_suspicion_level(self, player_name: str, delta: float) -> None:
        """更新可疑度"""
        profile = self.get_or_create_profile(player_name)
        profile.update_suspicion_level(delta)
    
    def _analyze_action_impact(self, profile: PlayerProfile, action: PlayerAction) -> None:
        """分析行为影响"""
        if action.action_type == "speak":
            # 分析发言内容
            if action.content:
                self._analyze_speech_content(profile, action.content)
        elif action.action_type == "vote":
            # 分析投票行为
            self._analyze_voting_behavior(profile, action)
    
    def _analyze_speech_content(self, profile: PlayerProfile, content: str) -> None:
        """分析发言内容"""
        content_lower = content.lower()
        
        # 检测攻击性言论
        aggressive_words = ["狼人", "坏人", "投票", "淘汰", "怀疑"]
        aggressive_count = sum(1 for word in aggressive_words if word in content_lower)
        
        if aggressive_count > 2:
            profile.update_suspicion_level(0.1)
        elif "分析" in content_lower or "逻辑" in content_lower:
            profile.update_trust_score(0.05)
        
        # 更新行为分析
        profile.behavior_analysis["speech_aggressiveness"] = profile.behavior_analysis.get("speech_aggressiveness", 0) + aggressive_count * 0.1
        profile.behavior_analysis["speech_analytical"] = profile.behavior_analysis.get("speech_analytical", 0) + (0.1 if "分析" in content_lower else 0)
    
    def _analyze_voting_behavior(self, profile: PlayerProfile, action: PlayerAction) -> None:
        """分析投票行为"""
        # 分析投票模式
        voting_patterns = profile.analyze_voting_patterns()
        profile.behavior_analysis.update(voting_patterns)
    
    def add_reflection(self, reflection: GameReflection) -> None:
        """添加反思记录"""
        self.reflection_log.append(reflection)
        # 保持最近20条反思
        if len(self.reflection_log) > 20:
            self.reflection_log = self.reflection_log[-20:]
    
    def get_top_suspicious_players(self, count: int = 3) -> List[tuple]:
        """获取最可疑的玩家"""
        sorted_players = sorted(
            [(name, profile.suspicion_level) for name, profile in self.profiles.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_players[:count]
    
    def get_most_trusted_players(self, count: int = 3) -> List[tuple]:
        """获取最信任的玩家"""
        sorted_players = sorted(
            [(name, profile.trust_score) for name, profile in self.profiles.items()],
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_players[:count]
    
    def export_profiles(self) -> Dict[str, Any]:
        """导出所有画像"""
        return {
            "profiles": {name: profile.to_dict() for name, profile in self.profiles.items()},
            "reflections": [r.to_dict() for r in self.reflection_log],
            "game_history": self.game_history
        }
    
    def import_profiles(self, data: Dict[str, Any]) -> None:
        """导入画像数据"""
        profiles_data = data.get("profiles", {})
        self.profiles = {name: PlayerProfile.from_dict(profile_data) for name, profile_data in profiles_data.items()}
        
        reflections_data = data.get("reflections", [])
        self.reflection_log = [GameReflection.from_dict(r) for r in reflections_data]
        
        self.game_history = data.get("game_history", [])


class MemoryManager:
    """记忆管理器"""
    
    def __init__(self):
        self.profiler = OpponentProfiler()
        self.game_state = {}
        self.conversation_history = deque(maxlen=100)  # 最近100条对话
        self.strategic_memory = {}  # 策略记忆
        self.emotional_state = {
            "confidence": 0.5,
            "stress": 0.5,
            "focus": 0.5
        }
    
    def update_game_state(self, env_info: Dict[str, Any]) -> None:
        """更新游戏状态"""
        self.game_state.update(env_info)
        
        # 记录重要事件
        if "phase" in env_info:
            self.conversation_history.append({
                "timestamp": time.time(),
                "type": "phase_change",
                "phase": env_info["phase"]
            })
        
        if "round" in env_info:
            self.conversation_history.append({
                "timestamp": time.time(),
                "type": "round_change",
                "round": env_info["round"]
            })
    
    def add_conversation(self, speaker: str, content: str, round_num: int = 0) -> None:
        """添加对话记录"""
        self.conversation_history.append({
            "timestamp": time.time(),
            "type": "conversation",
            "speaker": speaker,
            "content": content,
            "round": round_num
        })
        
        # 记录到画像中
        action = PlayerAction(
            timestamp=time.time(),
            action_type="speak",
            content=content,
            round=round_num
        )
        self.profiler.record_action(speaker, action)
    
    def get_recent_conversations(self, count: int = 10) -> List[Dict[str, Any]]:
        """获取最近的对话"""
        return list(self.conversation_history)[-count:] if self.conversation_history else []
    
    def update_strategic_memory(self, key: str, value: Any) -> None:
        """更新策略记忆"""
        self.strategic_memory[key] = value
        self.strategic_memory["last_updated"] = time.time()
    
    def get_strategic_memory(self, key: str) -> Any:
        """获取策略记忆"""
        return self.strategic_memory.get(key)
    
    def update_emotional_state(self, **kwargs) -> None:
        """更新情绪状态"""
        for key, value in kwargs.items():
            if key in self.emotional_state:
                self.emotional_state[key] = max(0.0, min(1.0, value))
    
    def get_emotional_state(self) -> Dict[str, float]:
        """获取情绪状态"""
        return self.emotional_state.copy()
    
    def export_memory(self) -> Dict[str, Any]:
        """导出记忆数据"""
        return {
            "profiler": self.profiler.export_profiles(),
            "game_state": self.game_state,
            "conversation_history": list(self.conversation_history),
            "strategic_memory": self.strategic_memory,
            "emotional_state": self.emotional_state
        }
    
    def import_memory(self, data: Dict[str, Any]) -> None:
        """导入记忆数据"""
        if "profiler" in data:
            self.profiler.import_profiles(data["profiler"])
        
        self.game_state = data.get("game_state", {})
        
        conversation_data = data.get("conversation_history", [])
        self.conversation_history = deque(conversation_data, maxlen=100)
        
        self.strategic_memory = data.get("strategic_memory", {})
        self.emotional_state = data.get("emotional_state", {
            "confidence": 0.5,
            "stress": 0.5,
            "focus": 0.5
        })
    
    def clear_temporary_memory(self) -> None:
        """清除临时记忆"""
        self.conversation_history.clear()
        self.emotional_state = {
            "confidence": 0.5,
            "stress": 0.5,
            "focus": 0.5
        }
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """获取记忆摘要"""
        return {
            "total_profiles": len(self.profiler.profiles),
            "total_conversations": len(self.conversation_history),
            "total_reflections": len(self.profiler.reflection_log),
            "games_played": len(self.profiler.game_history),
            "emotional_state": self.emotional_state,
            "strategic_keys": list(self.strategic_memory.keys())
        }


# 导出的类和函数
__all__ = [
    'MemoryManager',
    'PlayerAction', 
    'PlayerProfile', 
    'GameReflection', 
    'OpponentProfiler'
]
