# -*- coding: utf-8 -*-
"""策略基类模块"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from agentscope.message import Msg
from models.reasoning import (
    ActionDecision, 
    GameObservation, 
    PlayerInfo, 
    StrategicPlan,
    RoleSpecificReasoning
)
from utils.logger import WerewolfLogger


class BaseStrategy(ABC):
    """策略基类"""
    
    def __init__(self, agent_name: str, logger: WerewolfLogger):
        """初始化策略
        
        Args:
            agent_name: 智能体名称
            logger: 日志器
        """
        self.agent_name = agent_name
        self.logger = logger
        self.current_observation: Optional[GameObservation] = None
        self.player_info: Dict[str, PlayerInfo] = {}
        self.strategy_state: Dict[str, Any] = {}
        
    @abstractmethod
    def get_role_name(self) -> str:
        """获取角色名称"""
        pass
    
    @abstractmethod
    def generate_night_action(self, observation: GameObservation) -> Optional[ActionDecision]:
        """生成夜晚行动决策"""
        pass
    
    @abstractmethod
    def generate_day_speech(self, observation: GameObservation, context: Dict[str, Any]) -> str:
        """生成白天发言内容"""
        pass
    
    @abstractmethod
    def generate_voting_decision(self, observation: GameObservation, context: Dict[str, Any]) -> ActionDecision:
        """生成投票决策"""
        pass
    
    @abstractmethod
    def analyze_situation(self, observation: GameObservation) -> RoleSpecificReasoning:
        """分析当前局势"""
        pass
    
    def update_observation(self, observation: GameObservation) -> None:
        """更新观察信息"""
        self.current_observation = observation
        self._update_player_info(observation)
        self.logger.debug(f"策略更新观察: {self.get_role_name()}", {
            "phase": observation.phase,
            "round": observation.round,
            "alive_count": len(observation.alive_players)
        })
    
    def _update_player_info(self, observation: GameObservation) -> None:
        """更新玩家信息"""
        # 更新存活玩家信息
        for player_name in observation.alive_players:
            if player_name not in self.player_info:
                self.player_info[player_name] = PlayerInfo(
                    name=player_name,
                    role=None,
                    status="alive",
                    trust_score=0.5,
                    suspicion_level=0.3,
                    last_action=None,
                    voting_history=[]
                )
            else:
                self.player_info[player_name].status = "alive"
        
        # 更新死亡玩家信息
        for player_name in observation.dead_players:
            if player_name in self.player_info:
                self.player_info[player_name].status = "dead"
    
    def get_alive_players(self) -> List[str]:
        """获取存活玩家列表"""
        if not self.current_observation:
            return []
        return [p for p in self.current_observation.alive_players if p != self.agent_name]
    
    def get_dead_players(self) -> List[str]:
        """获取死亡玩家列表"""
        if not self.current_observation:
            return []
        return self.current_observation.dead_players
    
    def get_player_info(self, player_name: str) -> Optional[PlayerInfo]:
        """获取玩家信息"""
        return self.player_info.get(player_name)
    
    def update_trust_score(self, player_name: str, score_change: float) -> None:
        """更新信任分数"""
        if player_name in self.player_info:
            old_score = self.player_info[player_name].trust_score
            new_score = max(0.0, min(1.0, old_score + score_change))
            self.player_info[player_name].trust_score = new_score
            
            self.logger.debug(f"更新信任分数: {player_name} {old_score:.2f}->{new_score:.2f}")
    
    def update_suspicion_level(self, player_name: str, level_change: float) -> None:
        """更新可疑程度"""
        if player_name in self.player_info:
            old_level = self.player_info[player_name].suspicion_level
            new_level = max(0.0, min(1.0, old_level + level_change))
            self.player_info[player_name].suspicion_level = new_level
            
            self.logger.debug(f"更新可疑程度: {player_name} {old_level:.2f}->{new_level:.2f}")
    
    def get_most_suspicious_players(self, count: int = 3) -> List[str]:
        """获取最可疑的玩家"""
        alive_players = self.get_alive_players()
        suspicious_players = [
            (name, info.suspicion_level) 
            for name, info in self.player_info.items() 
            if name in alive_players
        ]
        
        # 按可疑程度排序
        suspicious_players.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in suspicious_players[:count]]
    
    def get_most_trusted_players(self, count: int = 3) -> List[str]:
        """获取最可信的玩家"""
        alive_players = self.get_alive_players()
        trusted_players = [
            (name, info.trust_score) 
            for name, info in self.player_info.items() 
            if name in alive_players
        ]
        
        # 按信任分数排序
        trusted_players.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in trusted_players[:count]]
    
    def analyze_speech_patterns(self, player_name: str, speech: str) -> Dict[str, Any]:
        """分析发言模式"""
        analysis = {
            "length": len(speech),
            "word_count": len(speech.split()),
            "mentions_werewolf": "狼人" in speech or "werewolf" in speech.lower(),
            "mentions_vote": "投票" in speech or "vote" in speech.lower(),
            "accusation": "怀疑" in speech or "可疑" in speech or "accuse" in speech.lower(),
            "defense": "不是" in speech or "清白" in speech or "innocent" in speech.lower(),
            "emotional": any(word in speech for word in ["愤怒", "激动", "生气", "angry", "emotional"])
        }
        
        self.logger.debug(f"发言模式分析: {player_name}", analysis)
        return analysis
    
    def calculate_voting_risk(self, target_player: str) -> float:
        """计算投票风险"""
        if target_player not in self.player_info:
            return 0.5
        
        player_info = self.player_info[target_player]
        
        # 基础风险
        risk = 0.3
        
        # 根据可疑程度调整
        risk += player_info.suspicion_level * 0.4
        
        # 根据信任分数调整
        risk -= player_info.trust_score * 0.3
        
        # 根据玩家数量调整
        alive_count = len(self.get_alive_players())
        if alive_count <= 4:
            risk += 0.2  # 玩家少时风险更高
        
        return max(0.0, min(1.0, risk))
    
    def should_reveal_role(self) -> bool:
        """判断是否应该暴露身份"""
        # 基础策略：通常不应该暴露身份
        return False
    
    def create_action_decision(
        self, 
        action_type: str, 
        target: Optional[str] = None, 
        reasoning: str = "", 
        confidence: float = 0.5,
        priority: int = 5,
        content: str = ""
    ) -> ActionDecision:
        """创建行动决策"""
        return ActionDecision(
            action_type=action_type,
            target=target,
            reasoning=reasoning,
            confidence=confidence,
            priority=priority,
            content=content
        )
    
    def format_response(self, decision: ActionDecision) -> str:
        """格式化响应"""
        if decision.action_type == "speak":
            return decision.content
        elif decision.action_type == "vote":
            return f"我选择投票给{decision.target}。{decision.reasoning}"
        elif decision.action_type in ["kill", "check", "heal", "poison", "shoot"]:
            return f"我决定{decision.action_type}{decision.target if decision.target else ''}。{decision.reasoning}"
        else:
            return decision.content
    
    def handle_emergency_situation(self, observation: GameObservation) -> Optional[ActionDecision]:
        """处理紧急情况"""
        # 检查是否处于危险境地
        alive_count = len(observation.alive_players)
        
        # 如果存活玩家很少，采取紧急策略
        if alive_count <= 4:
            return self._emergency_strategy(observation)
        
        return None
    
    def _emergency_strategy(self, observation: GameObservation) -> ActionDecision:
        """紧急策略"""
        # 基础紧急策略：投票给最可疑的玩家
        most_suspicious = self.get_most_suspicious_players(1)
        if most_suspicious:
            return self.create_action_decision(
                action_type="vote",
                target=most_suspicious[0],
                reasoning="紧急情况下，投票给最可疑的玩家",
                confidence=0.6,
                priority=8
            )
        
        # 如果没有可疑玩家，随机选择
        alive_players = self.get_alive_players()
        if alive_players:
            import random
            target = random.choice(alive_players)
            return self.create_action_decision(
                action_type="vote",
                target=target,
                reasoning="紧急情况下随机投票",
                confidence=0.3,
                priority=5
            )
        
        # 默认行动
        return self.create_action_decision(
            action_type="speak",
            content="我需要更多信息来做决定。",
            confidence=0.2,
            priority=1
        )
    
    def reset_strategy_state(self) -> None:
        """重置策略状态"""
        self.strategy_state.clear()
        self.logger.debug(f"重置策略状态: {self.get_role_name()}")
    
    def get_strategy_summary(self) -> Dict[str, Any]:
        """获取策略摘要"""
        return {
            "role": self.get_role_name(),
            "strategy_state": self.strategy_state.copy(),
            "player_count": len(self.player_info),
            "alive_players": len(self.get_alive_players()),
            "dead_players": len(self.get_dead_players())
        }
    
    def validate_decision(self, decision: ActionDecision) -> bool:
        """验证决策的有效性"""
        # 检查行动类型
        valid_actions = ["speak", "vote", "kill", "check", "heal", "poison", "shoot"]
        if decision.action_type not in valid_actions:
            self.logger.warning(f"无效的行动类型: {decision.action_type}")
            return False
        
        # 检查目标有效性
        if decision.target and decision.target not in self.player_info:
            self.logger.warning(f"无效的目标: {decision.target}")
            return False
        
        # 检查置信度范围
        if not 0.0 <= decision.confidence <= 1.0:
            self.logger.warning(f"无效的置信度: {decision.confidence}")
            return False
        
        # 检查优先级范围
        if not 1 <= decision.priority <= 10:
            self.logger.warning(f"无效的优先级: {decision.priority}")
            return False
        
        return True
