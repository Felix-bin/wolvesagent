# -*- coding: utf-8 -*-
"""策略管理器 - 负责根据角色选择和切换策略"""

from typing import Dict, Optional, Any
from strategies.base_strategy import BaseStrategy
from strategies.werewolf_strategy import WerewolfStrategy
from strategies.seer_strategy import SeerStrategy
from strategies.witch_strategy import WitchStrategy
from strategies.hunter_strategy import HunterStrategy
from strategies.villager_strategy import VillagerStrategy
from utils.logger import WerewolfLogger


class StrategyManager:
    """策略管理器 - 根据角色动态选择策略"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.logger = WerewolfLogger(agent_name)
        self.current_role: Optional[str] = None
        self.current_strategy: Optional[BaseStrategy] = None
        
        # 策略缓存（避免重复创建）
        self._strategy_cache: Dict[str, BaseStrategy] = {}
    
    def set_role(self, role: str) -> None:
        """设置角色并切换策略
        
        Args:
            role: 角色名称 (werewolf, seer, witch, hunter, villager)
        """
        if role == self.current_role:
            return
        
        self.logger.info(f"角色切换: {self.current_role} -> {role}")
        self.current_role = role
        self.current_strategy = self._get_strategy(role)
    
    def _get_strategy(self, role: str) -> BaseStrategy:
        """获取角色对应的策略
        
        Args:
            role: 角色名称
            
        Returns:
            对应的策略实例
        """
        # 如果缓存中有，直接返回
        if role in self._strategy_cache:
            return self._strategy_cache[role]
        
        # 创建新策略实例
        strategy_map = {
            'werewolf': WerewolfStrategy,
            'seer': SeerStrategy,
            'witch': WitchStrategy,
            'hunter': HunterStrategy,
            'villager': VillagerStrategy
        }
        
        strategy_class = strategy_map.get(role, VillagerStrategy)
        strategy = strategy_class(self.agent_name, self.logger)
        
        # 缓存策略
        self._strategy_cache[role] = strategy
        
        return strategy
    
    def get_current_strategy(self) -> Optional[BaseStrategy]:
        """获取当前策略"""
        return self.current_strategy
    
    def has_strategy(self) -> bool:
        """检查是否已设置策略"""
        return self.current_strategy is not None
    
    def get_current_role(self) -> Optional[str]:
        """获取当前角色"""
        return self.current_role
    
    def reset(self) -> None:
        """重置策略管理器（新游戏开始时调用）"""
        self.current_role = None
        self.current_strategy = None
        # 注意：不清空缓存，保留跨局的策略实例和学习数据
    
    def export_state(self) -> Dict[str, Any]:
        """导出策略状态（用于持久化）"""
        state = {
            'current_role': self.current_role,
            'strategies': {}
        }
        
        # 导出每个策略的状态
        for role, strategy in self._strategy_cache.items():
            state['strategies'][role] = {
                'strategy_state': strategy.strategy_state,
                'player_info': {
                    name: {
                        'role': info.role,
                        'trust_score': info.trust_score,
                        'suspicion_level': info.suspicion_level,
                        'voting_history': info.voting_history
                    }
                    for name, info in strategy.player_info.items()
                }
            }
        
        return state
    
    def load_state(self, state: Dict[str, Any]) -> None:
        """加载策略状态（用于恢复）"""
        if not state:
            return
        
        self.current_role = state.get('current_role')
        
        # 加载每个策略的状态
        strategies_state = state.get('strategies', {})
        for role, strategy_state in strategies_state.items():
            # 先获取或创建策略实例
            strategy = self._get_strategy(role)
            
            # 恢复策略状态
            if 'strategy_state' in strategy_state:
                strategy.strategy_state.update(strategy_state['strategy_state'])
            
            # 恢复玩家信息
            if 'player_info' in strategy_state:
                from models.reasoning import PlayerInfo
                for name, info_dict in strategy_state['player_info'].items():
                    strategy.player_info[name] = PlayerInfo(
                        name=name,
                        role=info_dict.get('role'),
                        trust_score=info_dict.get('trust_score', 0.5),
                        suspicion_level=info_dict.get('suspicion_level', 0.3),
                        voting_history=info_dict.get('voting_history', [])
                    )
        
        # 恢复当前策略
        if self.current_role:
            self.current_strategy = self._get_strategy(self.current_role)

