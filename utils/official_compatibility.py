# -*- coding: utf-8 -*-
"""官方测试程序兼容性模块"""

from typing import List, Optional, Any
from agentscope.agent import AgentBase
from models.structured_models import BaseStructuredModel, StructuredModelFactory


class OfficialCompatibilityAdapter:
    """官方测试程序兼容性适配器"""
    
    @staticmethod
    def convert_official_model_to_our_model(official_model_class, valid_players: Optional[List[str]] = None):
        """
        将官方模型类转换为我们的模型类
        
        Args:
            official_model_class: 官方模型类
            valid_players: 有效玩家列表
            
        Returns:
            我们的模型类
        """
        model_name = getattr(official_model_class, '__name__', 'Unknown')
        
        if model_name == 'DiscussionModel':
            return StructuredModelFactory.create_discussion_model()
        elif 'VoteModel' in model_name:
            # 从官方模型中提取玩家列表
            if valid_players:
                return StructuredModelFactory.create_vote_model(valid_players)
            else:
                # 如果没有提供玩家列表，使用默认列表
                return StructuredModelFactory.create_vote_model(["Player1", "Player2", "Player3"])
        elif model_name == 'WitchResurrectModel':
            return StructuredModelFactory.create_witch_resurrect_model()
        elif 'WitchPoisonModel' in model_name:
            if valid_players:
                return StructuredModelFactory.create_witch_poison_model(valid_players)
            else:
                return StructuredModelFactory.create_witch_poison_model(["Player1", "Player2", "Player3"])
        elif 'SeerModel' in model_name:
            if valid_players:
                return StructuredModelFactory.create_seer_model(valid_players)
            else:
                return StructuredModelFactory.create_seer_model(["Player1", "Player2", "Player3"])
        elif 'HunterModel' in model_name:
            if valid_players:
                return StructuredModelFactory.create_hunter_model(valid_players)
            else:
                return StructuredModelFactory.create_hunter_model(["Player1", "Player2", "Player3"])
        else:
            # 如果不是官方模型，直接返回
            return official_model_class
    
    @staticmethod
    def convert_our_response_to_official(our_model_instance, official_model_class, valid_players: Optional[List[str]] = None):
        """
        将我们的模型响应转换为官方模型格式
        
        Args:
            our_model_instance: 我们的模型实例
            official_model_class: 官方模型类
            valid_players: 有效玩家列表
            
        Returns:
            官方模型实例
        """
        model_name = getattr(official_model_class, '__name__', 'Unknown')
        
        try:
            if model_name == 'DiscussionModel':
                return official_model_class(reach_agreement=our_model_instance.reach_agreement)
            elif 'VoteModel' in model_name:
                return official_model_class(vote=our_model_instance.vote)
            elif model_name == 'WitchResurrectModel':
                return official_model_class(resurrect=our_model_instance.resurrect)
            elif 'WitchPoisonModel' in model_name:
                return official_model_class(poison=our_model_instance.poison, name=our_model_instance.target)
            elif 'SeerModel' in model_name:
                return official_model_class(name=our_model_instance.check)
            elif 'HunterModel' in model_name:
                return official_model_class(shoot=our_model_instance.shoot, name=our_model_instance.target)
            else:
                # 如果不是官方模型，直接返回
                return our_model_instance
        except Exception as e:
            print(f"转换官方模型时出错: {e}")
            # 返回默认响应
            return OfficialCompatibilityAdapter._create_default_official_response(official_model_class, valid_players)
    
    @staticmethod
    def _create_default_official_response(official_model_class, valid_players: Optional[List[str]] = None):
        """创建默认的官方模型响应"""
        model_name = getattr(official_model_class, '__name__', 'Unknown')
        
        if model_name == 'DiscussionModel':
            return official_model_class(reach_agreement=False)
        elif 'VoteModel' in model_name:
            # 选择第一个玩家作为默认投票
            if valid_players and len(valid_players) > 0:
                return official_model_class(vote=valid_players[0])
            else:
                # 使用空字符串而不是"Player1"，避免验证错误
                return official_model_class(vote="")
        elif model_name == 'WitchResurrectModel':
            return official_model_class(resurrect=False)
        elif 'WitchPoisonModel' in model_name:
            return official_model_class(poison=False, name=None)
        elif 'SeerModel' in model_name:
            if valid_players and len(valid_players) > 0:
                return official_model_class(name=valid_players[0])
            else:
                # 使用空字符串而不是"Player1"，避免验证错误
                return official_model_class(name="")
        elif 'HunterModel' in model_name:
            return official_model_class(shoot=False, name=None)
        else:
            # 如果不是官方模型，返回None
            return None
    
    @staticmethod
    def extract_valid_players_from_agents(agents: List[AgentBase]) -> List[str]:
        """
        从智能体列表中提取玩家名称
        
        Args:
            agents: 智能体列表
            
        Returns:
            玩家名称列表
        """
        return [agent.name for agent in agents]
    
    @staticmethod
    def create_official_response_wrapper(text: str, official_model_instance):
        """
        创建官方响应包装器
        
        Args:
            text: 响应文本
            official_model_instance: 官方模型实例
            
        Returns:
            包装后的响应对象
        """
        class OfficialResponse:
            def __init__(self, text, official_model):
                self.text = text
                self.parsed = official_model
        
        return OfficialResponse(text, official_model_instance)


class OfficialModelFactory:
    """官方模型工厂，用于创建与官方测试程序兼容的模型"""
    
    @staticmethod
    def create_discussion_model():
        """创建讨论模型"""
        from werewolves.structured_model import DiscussionModel
        return DiscussionModel
    
    @staticmethod
    def create_vote_model(agents: List[AgentBase]):
        """创建投票模型"""
        from werewolves.structured_model import get_vote_model
        return get_vote_model(agents)
    
    @staticmethod
    def create_witch_resurrect_model():
        """创建女巫复活模型"""
        from werewolves.structured_model import WitchResurrectModel
        return WitchResurrectModel
    
    @staticmethod
    def create_witch_poison_model(agents: List[AgentBase]):
        """创建女巫毒药模型"""
        from werewolves.structured_model import get_poison_model
        return get_poison_model(agents)
    
    @staticmethod
    def create_seer_model(agents: List[AgentBase]):
        """创建预言家模型"""
        from werewolves.structured_model import get_seer_model
        return get_seer_model(agents)
    
    @staticmethod
    def create_hunter_model(agents: List[AgentBase]):
        """创建猎人模型"""
        from werewolves.structured_model import get_hunter_model
        return get_hunter_model(agents)