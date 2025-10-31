# -*- coding: utf-8 -*-
"""思维链推理模块 - Chain of Thought (CoT)"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ReasoningStep(Enum):
    """推理步骤类型"""
    OBSERVATION = "观察"  # 观察当前局势
    ANALYSIS = "分析"    # 分析信息
    DEDUCTION = "推理"   # 逻辑推理
    PLANNING = "规划"    # 制定计划
    DECISION = "决策"    # 最终决策


@dataclass
class ThoughtStep:
    """单个思维步骤"""
    step_type: ReasoningStep
    content: str
    confidence: float = 0.5  # 0-1
    evidence: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'step_type': self.step_type.value,
            'content': self.content,
            'confidence': self.confidence,
            'evidence': self.evidence
        }


@dataclass
class ChainOfThought:
    """思维链 - 完整的推理过程"""
    steps: List[ThoughtStep] = field(default_factory=list)
    final_conclusion: str = ""
    overall_confidence: float = 0.5
    
    def add_step(self, step_type: ReasoningStep, content: str, 
                 confidence: float = 0.5, evidence: List[str] = None) -> None:
        """添加推理步骤"""
        step = ThoughtStep(
            step_type=step_type,
            content=content,
            confidence=confidence,
            evidence=evidence or []
        )
        self.steps.append(step)
    
    def get_reasoning_summary(self) -> str:
        """获取推理摘要"""
        if not self.steps:
            return "无推理过程"
        
        summary = []
        for i, step in enumerate(self.steps, 1):
            summary.append(f"{i}. {step.step_type.value}: {step.content}")
        
        if self.final_conclusion:
            summary.append(f"\n结论: {self.final_conclusion}")
        
        return "\n".join(summary)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            'steps': [step.to_dict() for step in self.steps],
            'final_conclusion': self.final_conclusion,
            'overall_confidence': self.overall_confidence
        }
    
    def to_prompt(self) -> str:
        """转换为提示词格式（用于让大模型进行推理）"""
        prompt = "请进行逐步推理，按照以下步骤思考：\n\n"
        
        if not self.steps:
            prompt += "1. 观察：当前游戏局势如何？\n"
            prompt += "2. 分析：有哪些关键信息？\n"
            prompt += "3. 推理：基于信息可以得出什么结论？\n"
            prompt += "4. 规划：应该采取什么策略？\n"
            prompt += "5. 决策：最终决定是什么？\n"
        else:
            for i, step in enumerate(self.steps, 1):
                prompt += f"{i}. {step.step_type.value}：{step.content}\n"
        
        return prompt


class ChainOfThoughtBuilder:
    """思维链构建器 - 帮助构建结构化的推理过程"""
    
    @staticmethod
    def build_voting_cot(
        my_role: str,
        alive_players: List[str],
        suspected_players: Dict[str, float],
        trusted_players: Dict[str, float],
        recent_events: List[str]
    ) -> ChainOfThought:
        """构建投票决策的思维链
        
        Args:
            my_role: 我的角色
            alive_players: 存活玩家列表
            suspected_players: 可疑玩家及可疑度
            trusted_players: 信任玩家及信任度
            recent_events: 最近的游戏事件
            
        Returns:
            思维链对象
        """
        cot = ChainOfThought()
        
        # 1. 观察阶段
        observation = f"当前有{len(alive_players)}名玩家存活。"
        if recent_events:
            observation += f" 最近发生：{', '.join(recent_events[-3:])}。"
        cot.add_step(
            ReasoningStep.OBSERVATION,
            observation,
            confidence=1.0,
            evidence=recent_events
        )
        
        # 2. 分析阶段
        analysis_parts = []
        if suspected_players:
            top_suspect = max(suspected_players.items(), key=lambda x: x[1])
            analysis_parts.append(f"{top_suspect[0]}的可疑度最高({top_suspect[1]:.2f})")
        
        if trusted_players:
            most_trusted = max(trusted_players.items(), key=lambda x: x[1])
            analysis_parts.append(f"{most_trusted[0]}的可信度最高({most_trusted[1]:.2f})")
        
        if not analysis_parts:
            analysis_parts.append("信息不足，需要更多观察")
        
        cot.add_step(
            ReasoningStep.ANALYSIS,
            "、".join(analysis_parts),
            confidence=0.7
        )
        
        # 3. 推理阶段
        if my_role == "werewolf":
            reasoning = "作为狼人，应该投票给对狼人阵营威胁最大的好人"
        elif my_role == "seer":
            reasoning = "作为先知，应该投票给已确认的狼人或最可疑的玩家"
        elif my_role in ["witch", "hunter"]:
            reasoning = "作为特殊角色，应该投票给威胁最大的可疑玩家"
        else:  # villager
            reasoning = "作为村民，应该跟随可信玩家的判断或投票给最可疑者"
        
        cot.add_step(
            ReasoningStep.DEDUCTION,
            reasoning,
            confidence=0.8
        )
        
        # 4. 规划阶段
        if suspected_players:
            target = max(suspected_players.items(), key=lambda x: x[1])[0]
            planning = f"选择投票目标：{target}"
        else:
            target = alive_players[0] if alive_players else "Player1"
            planning = f"信息不足，暂时选择：{target}"
        
        cot.add_step(
            ReasoningStep.PLANNING,
            planning,
            confidence=0.6
        )
        
        # 5. 决策阶段
        decision = f"最终决定投票给：{target}"
        cot.add_step(
            ReasoningStep.DECISION,
            decision,
            confidence=0.7
        )
        
        cot.final_conclusion = decision
        cot.overall_confidence = 0.7
        
        return cot
    
    @staticmethod
    def build_seer_check_cot(
        checked_players: List[str],
        alive_players: List[str],
        suspected_players: Dict[str, float],
        priority_targets: List[str]
    ) -> ChainOfThought:
        """构建先知查验的思维链"""
        cot = ChainOfThought()
        
        # 1. 观察
        unchecked = [p for p in alive_players if p not in checked_players]
        observation = f"还有{len(unchecked)}名玩家未查验"
        cot.add_step(
            ReasoningStep.OBSERVATION,
            observation,
            confidence=1.0
        )
        
        # 2. 分析
        if priority_targets:
            analysis = f"优先查验目标：{', '.join(priority_targets[:3])}"
        else:
            analysis = "无明确优先目标，需要根据发言和行为判断"
        cot.add_step(
            ReasoningStep.ANALYSIS,
            analysis,
            confidence=0.8
        )
        
        # 3. 推理
        reasoning = "查验策略：优先查验可疑度高、发言积极、行为异常的玩家"
        cot.add_step(
            ReasoningStep.DEDUCTION,
            reasoning,
            confidence=0.8
        )
        
        # 4. 规划
        if priority_targets and priority_targets[0] in unchecked:
            target = priority_targets[0]
        elif unchecked:
            # 选择最可疑的未查验玩家
            unchecked_suspects = {p: suspected_players.get(p, 0.3) 
                                for p in unchecked}
            target = max(unchecked_suspects.items(), key=lambda x: x[1])[0]
        else:
            target = alive_players[0] if alive_players else "Player1"
        
        planning = f"本轮查验目标：{target}"
        cot.add_step(
            ReasoningStep.PLANNING,
            planning,
            confidence=0.7
        )
        
        # 5. 决策
        decision = f"决定查验：{target}"
        cot.add_step(
            ReasoningStep.DECISION,
            decision,
            confidence=0.8
        )
        
        cot.final_conclusion = decision
        cot.overall_confidence = 0.8
        
        return cot
    
    @staticmethod
    def build_speech_cot(
        my_role: str,
        game_phase: str,
        key_information: List[str],
        speaking_goal: str
    ) -> ChainOfThought:
        """构建发言的思维链
        
        Args:
            my_role: 我的角色
            game_phase: 游戏阶段
            key_information: 关键信息列表
            speaking_goal: 发言目标（如"隐藏身份"、"揭露狼人"等）
        """
        cot = ChainOfThought()
        
        # 1. 观察
        observation = f"当前阶段：{game_phase}，我的角色：{my_role}"
        cot.add_step(
            ReasoningStep.OBSERVATION,
            observation,
            confidence=1.0
        )
        
        # 2. 分析
        if key_information:
            analysis = f"关键信息：{'; '.join(key_information[:3])}"
        else:
            analysis = "暂无明确信息，需要谨慎发言"
        cot.add_step(
            ReasoningStep.ANALYSIS,
            analysis,
            confidence=0.7
        )
        
        # 3. 推理
        role_strategies = {
            "werewolf": "需要隐藏身份，混淆视听，保护队友",
            "seer": "需要适时公布信息，引导好人投票",
            "witch": "需要合理解释用药，不过早暴露",
            "hunter": "需要隐藏身份，关键时刻威慑",
            "villager": "需要逻辑分析，识破狼人谎言"
        }
        reasoning = role_strategies.get(my_role, "需要仔细观察，理性分析")
        cot.add_step(
            ReasoningStep.DEDUCTION,
            reasoning,
            confidence=0.8
        )
        
        # 4. 规划
        planning = f"发言目标：{speaking_goal}。采用适当的语气和内容。"
        cot.add_step(
            ReasoningStep.PLANNING,
            planning,
            confidence=0.7
        )
        
        # 5. 决策
        decision = "根据以上分析生成具体发言内容"
        cot.add_step(
            ReasoningStep.DECISION,
            decision,
            confidence=0.7
        )
        
        cot.final_conclusion = speaking_goal
        cot.overall_confidence = 0.7
        
        return cot


# 导出
__all__ = [
    'ReasoningStep',
    'ThoughtStep',
    'ChainOfThought',
    'ChainOfThoughtBuilder'
]

