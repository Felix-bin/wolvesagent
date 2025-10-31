"""
狼人杀游戏的结构化输出模型
基于比赛要求实现BaseModel，确保与AgentScope完全兼容
"""

from typing import Literal, Optional, List, Dict, Any
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class BaseStructuredModel(BaseModel, ABC):
    """基础结构化模型类
    
    严格按照赛题要求实现BaseModel相关功能，确保与AgentScope完全兼容
    """
    
    class Config:
        """Pydantic配置"""
        extra = "forbid"  # 禁止额外字段
        validate_assignment = True  # 赋值时验证
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        pass
    
    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseStructuredModel":
        """从字典创建实例"""
        pass
    
    def model_dump_json(self, **kwargs) -> str:
        """兼容AgentScope的JSON序列化"""
        try:
            return super().model_dump_json(**kwargs)
        except AttributeError:
            # 兼容旧版本pydantic
            return self.json(**kwargs)
    
    def model_dump(self, **kwargs) -> Dict[str, Any]:
        """兼容AgentScope的字典序列化"""
        try:
            return super().model_dump(**kwargs)
        except AttributeError:
            # 兼容旧版本pydantic
            return self.dict(**kwargs)


class DiscussionModel(BaseStructuredModel):
    """讨论阶段的输出格式"""
    
    reach_agreement: bool = Field(
        description="是否达成共识",
        default=False
    )
    
    discussion_content: str = Field(
        description="讨论内容",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "reach_agreement": self.reach_agreement,
            "discussion_content": self.discussion_content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DiscussionModel":
        """从字典创建实例"""
        return cls(
            reach_agreement=data.get("reach_agreement", False),
            discussion_content=data.get("discussion_content", "")
        )


class VoteModel(BaseStructuredModel):
    """投票阶段的输出格式"""
    
    vote: str = Field(
        description="投票的目标玩家名称",
        default=""
    )
    
    reason: str = Field(
        description="投票理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "vote": self.vote,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VoteModel":
        """从字典创建实例"""
        return cls(
            vote=data.get("vote", ""),
            reason=data.get("reason", "")
        )


class WitchResurrectModel(BaseStructuredModel):
    """女巫复活行动的输出格式"""
    
    resurrect: bool = Field(
        description="是否使用解药复活玩家",
        default=False
    )
    
    reason: str = Field(
        description="复活/不复活的决定理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "resurrect": self.resurrect,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WitchResurrectModel":
        """从字典创建实例"""
        return cls(
            resurrect=data.get("resurrect", False),
            reason=data.get("reason", "")
        )


class WitchPoisonModel(BaseStructuredModel):
    """女巫毒药行动的输出格式"""
    
    poison: bool = Field(
        description="是否使用毒药",
        default=False
    )
    
    target: Optional[str] = Field(
        description="毒药的目标玩家名称，如果不使用毒药则为None",
        default=None
    )
    
    reason: str = Field(
        description="使用/不使用毒药的决定理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "poison": self.poison,
            "target": self.target,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WitchPoisonModel":
        """从字典创建实例"""
        return cls(
            poison=data.get("poison", False),
            target=data.get("target"),
            reason=data.get("reason", "")
        )


class SeerModel(BaseStructuredModel):
    """预言家查验行动的输出格式"""
    
    check: str = Field(
        description="查验的目标玩家名称",
        default=""
    )
    
    reason: str = Field(
        description="选择该玩家的理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "check": self.check,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SeerModel":
        """从字典创建实例"""
        return cls(
            check=data.get("check", ""),
            reason=data.get("reason", "")
        )


class HunterModel(BaseStructuredModel):
    """猎人开枪行动的输出格式"""
    
    shoot: bool = Field(
        description="是否开枪",
        default=False
    )
    
    target: Optional[str] = Field(
        description="开枪的目标玩家名称，如果不开枪则为None",
        default=None
    )
    
    reason: str = Field(
        description="开枪/不开枪的决定理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "shoot": self.shoot,
            "target": self.target,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HunterModel":
        """从字典创建实例"""
        return cls(
            shoot=data.get("shoot", False),
            target=data.get("target"),
            reason=data.get("reason", "")
        )


class WerewolfKillModel(BaseStructuredModel):
    """狼人击杀行动的输出格式"""
    
    target: str = Field(
        description="击杀的目标玩家名称",
        default=""
    )
    
    reason: str = Field(
        description="选择该玩家的理由",
        default=""
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "target": self.target,
            "reason": self.reason
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WerewolfKillModel":
        """从字典创建实例"""
        return cls(
            target=data.get("target", ""),
            reason=data.get("reason", "")
        )


class DaySpeechModel(BaseStructuredModel):
    """白天发言的输出格式"""
    
    content: str = Field(
        description="发言内容",
        default=""
    )
    
    target: Optional[str] = Field(
        description="发言针对的目标玩家名称，如果没有特定目标则为None",
        default=None
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "content": self.content,
            "target": self.target
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DaySpeechModel":
        """从字典创建实例"""
        return cls(
            content=data.get("content", ""),
            target=data.get("target")
        )


class StructuredModelFactory:
    """结构化模型工厂类"""
    
    @staticmethod
    def create_discussion_model() -> type[BaseModel]:
        """创建讨论模型"""
        return DiscussionModel
    
    @staticmethod
    def create_vote_model(valid_players: List[str]) -> type[BaseModel]:
        """创建投票模型"""
        class DynamicVoteModel(BaseStructuredModel):
            vote: Literal[tuple(valid_players)] = Field(  # type: ignore
                description="投票的目标玩家名称",
                default=valid_players[0] if valid_players else ""
            )
            
            reason: str = Field(
                description="投票理由",
                default=""
            )
            
            def to_dict(self) -> Dict[str, Any]:
                """转换为字典"""
                return {
                    "vote": self.vote,
                    "reason": self.reason
                }
            
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> "DynamicVoteModel":
                """从字典创建实例"""
                return cls(
                    vote=data.get("vote", valid_players[0] if valid_players else ""),
                    reason=data.get("reason", "")
                )
        
        return DynamicVoteModel
    
    @staticmethod
    def create_witch_resurrect_model() -> type[BaseModel]:
        """创建女巫复活模型"""
        return WitchResurrectModel
    
    @staticmethod
    def create_witch_poison_model(valid_players: List[str]) -> type[BaseModel]:
        """创建女巫毒药模型"""
        class DynamicWitchPoisonModel(BaseStructuredModel):
            poison: bool = Field(
                description="是否使用毒药",
                default=False
            )
            
            target: Optional[Literal[tuple(valid_players)]] = Field(  # type: ignore
                description="毒药的目标玩家名称，如果不使用毒药则为None",
                default=None
            )
            
            reason: str = Field(
                description="使用/不使用毒药的决定理由",
                default=""
            )
            
            def to_dict(self) -> Dict[str, Any]:
                """转换为字典"""
                return {
                    "poison": self.poison,
                    "target": self.target,
                    "reason": self.reason
                }
            
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> "DynamicWitchPoisonModel":
                """从字典创建实例"""
                return cls(
                    poison=data.get("poison", False),
                    target=data.get("target"),
                    reason=data.get("reason", "")
                )
        
        return DynamicWitchPoisonModel
    
    @staticmethod
    def create_seer_model(valid_players: List[str]) -> type[BaseModel]:
        """创建预言家模型"""
        class DynamicSeerModel(BaseStructuredModel):
            check: Literal[tuple(valid_players)] = Field(  # type: ignore
                description="查验的目标玩家名称",
                default=valid_players[0] if valid_players else ""
            )
            
            reason: str = Field(
                description="选择该玩家的理由",
                default=""
            )
            
            def to_dict(self) -> Dict[str, Any]:
                """转换为字典"""
                return {
                    "check": self.check,
                    "reason": self.reason
                }
            
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> "DynamicSeerModel":
                """从字典创建实例"""
                return cls(
                    check=data.get("check", valid_players[0] if valid_players else ""),
                    reason=data.get("reason", "")
                )
        
        return DynamicSeerModel
    
    @staticmethod
    def create_hunter_model(valid_players: List[str]) -> type[BaseModel]:
        """创建猎人模型"""
        class DynamicHunterModel(BaseStructuredModel):
            shoot: bool = Field(
                description="是否开枪",
                default=False
            )
            
            target: Optional[Literal[tuple(valid_players)]] = Field(  # type: ignore
                description="开枪的目标玩家名称，如果不开枪则为None",
                default=None
            )
            
            reason: str = Field(
                description="开枪/不开枪的决定理由",
                default=""
            )
            
            def to_dict(self) -> Dict[str, Any]:
                """转换为字典"""
                return {
                    "shoot": self.shoot,
                    "target": self.target,
                    "reason": self.reason
                }
            
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> "DynamicHunterModel":
                """从字典创建实例"""
                return cls(
                    shoot=data.get("shoot", False),
                    target=data.get("target"),
                    reason=data.get("reason", "")
                )
        
        return DynamicHunterModel
    
    @staticmethod
    def create_werewolf_kill_model(valid_players: List[str]) -> type[BaseModel]:
        """创建狼人击杀模型"""
        class DynamicWerewolfKillModel(BaseStructuredModel):
            target: Literal[tuple(valid_players)] = Field(  # type: ignore
                description="击杀的目标玩家名称",
                default=valid_players[0] if valid_players else ""
            )
            
            reason: str = Field(
                description="选择该玩家的理由",
                default=""
            )
            
            def to_dict(self) -> Dict[str, Any]:
                """转换为字典"""
                return {
                    "target": self.target,
                    "reason": self.reason
                }
            
            @classmethod
            def from_dict(cls, data: Dict[str, Any]) -> "DynamicWerewolfKillModel":
                """从字典创建实例"""
                return cls(
                    target=data.get("target", valid_players[0] if valid_players else ""),
                    reason=data.get("reason", "")
                )
        
        return DynamicWerewolfKillModel
    
    @staticmethod
    def create_day_speech_model() -> type[BaseModel]:
        """创建白天发言模型"""
        return DaySpeechModel
