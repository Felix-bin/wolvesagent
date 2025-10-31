# -*- coding: utf-8 -*-
"""狼人杀AI智能体具体实现 - 重构版本"""

import time
import os
from typing import Dict, List, Any, Optional
from agentscope.agent import ReActAgent
from agentscope.message import Msg
from agentscope.formatter import DashScopeMultiAgentFormatter
from agentscope.model import DashScopeChatModel

# 导入核心组件
from core.message_handler import MessageHandler
from core.strategy_manager import StrategyManager
from core.response_generator import ResponseGenerator
from core.intelligent_responder import IntelligentResponder
from models.memory import MemoryManager
from utils.logger import WerewolfLogger


class PlayerAgent(ReActAgent):
    """狼人杀AI智能体（重构版）
    
    基于AgentScope 1.0框架开发，完全兼容官方比赛测试程序。
    
    核心改进：
    1. 模块化架构：消息处理、策略管理、响应生成分离
    2. 严格的时间和字符限制控制
    3. 正确的结构化输出支持
    4. 跨局学习和记忆管理
    5. 动态策略切换
    """

    def __init__(self, name: str):
        """初始化智能体
        
        Args:
            name: 智能体名称，由系统分配的固定字符串
        """
        # 基础属性
        self.name = name
        
        # 初始化系统提示词
        system_prompt = self._build_system_prompt()
        
        # 初始化模型
        model = DashScopeChatModel(
            api_key=os.environ.get("DASHSCOPE_API_KEY"),
            model_name="qwen-max",
        )
        
        # 初始化ReActAgent父类
        super().__init__(
            name=name,
            sys_prompt=system_prompt,
            model=model,
            formatter=DashScopeMultiAgentFormatter(),
        )
        
        # 初始化核心组件
        self.message_handler = MessageHandler(name)
        self.strategy_manager = StrategyManager(name)
        self.response_generator = ResponseGenerator(name, model)
        self.memory_manager = MemoryManager()
        self.logger = WerewolfLogger(name)
        
        # 初始化智能响应器（集成策略系统）
        self.intelligent_responder = IntelligentResponder(
            agent_name=name,
            model=model,
            strategy_manager=self.strategy_manager,
            message_handler=self.message_handler,
            memory_manager=self.memory_manager
        )
        
        # 游戏状态
        self.current_round = 0
        self.reflection_log = []

    def _build_system_prompt(self) -> str:
        """构建系统提示词"""
        return f"""你是狼人杀游戏玩家 {self.name}。

# 核心目标
你的目标是与队友合作，尽可能赢得游戏胜利。

# 游戏规则
- 9人局配置：3狼人、3村民、1先知、1女巫、1猎人
- 狼人阵营：夜晚杀人，白天隐藏身份
- 好人阵营：找出并投票淘汰狼人
- 游戏流程：夜晚行动 → 白天讨论 → 投票淘汰

# 行动准则
1. 严格遵守时间限制：每次响应不超过30秒
2. 控制发言长度：不超过2048字符
3. 根据角色身份制定相应策略
4. 观察其他玩家行为，建立对手画像
5. 在长期游戏中学习和适应

# 角色策略指导
## 狼人策略
- 隐藏身份，伪装成好人
- 与狼队友配合，统一行动
- 可以自刀骗取女巫解药
- 悍跳预言家误导好人
- 保护狼队友，攻击威胁角色

## 预言家策略  
- 谨慎查验，避免过早暴露
- 建立警徽流，规划查验顺序
- 适时公布查验结果
- 引导好人投票

## 女巫策略
- 合理使用解药和毒药
- 第一晚通常不使用解药
- 毒药用于确认的狼人
- 注意保护特殊角色

## 猎人策略
- 谨慎使用开枪技能
- 死亡时带走威胁目标
- 可以不开枪保存实力

## 村民策略
- 逻辑分析，识别狼人
- 保护特殊角色
- 跟随可信玩家投票

# 重要提醒
- 基于已有信息进行推理，不要编造信息
- 发言要简洁明了，逻辑清晰
- 注意观察投票模式和发言习惯
- 在游戏结束后进行反思总结
"""

    async def observe(self, msg) -> None:
        """接收游戏环境信息并更新内部状态（重构版）
        
        严格按照赛题要求实现observe函数：
        - 接收游戏环境信息（如法官指令、其他玩家发言、投票结果等）
        - 更新智能体内部状态
        - 支持跨局学习和记忆管理
        
        Args:
            msg: 来自游戏环境的消息或消息列表
        """
        try:
            if msg is None:
                return
            
            # 使用MessageHandler处理消息
            parsed_info = self.message_handler.process_message(msg)
            
            # 处理角色分配
            if parsed_info['role_assigned']:
                role = parsed_info['role_assigned']
                self.logger.info(f"获得角色: {role}")
                
                # 设置策略
                self.strategy_manager.set_role(role)
            
            # 更新记忆管理器
            for msg_data in parsed_info['messages']:
                sender = msg_data['sender']
                content = msg_data['content']
                
                # 添加到对话历史
                self.memory_manager.add_conversation(
                    speaker=sender,
                    content=content,
                    round_num=self.current_round
                )
            
            # 处理死亡信息
            if parsed_info['player_died']:
                for dead_player in parsed_info['player_died']:
                    self.logger.info(f"玩家死亡: {dead_player}")
                    # 更新策略中的玩家状态
                    if self.strategy_manager.has_strategy():
                        strategy = self.strategy_manager.get_current_strategy()
                        if dead_player in strategy.player_info:
                            strategy.player_info[dead_player].status = "dead"
            
            # 更新游戏轮次
            if parsed_info['phase_change']:
                phase = parsed_info['phase_change']
                self.logger.debug(f"阶段变化: {phase}")
                if phase == 'night':
                    self.current_round += 1
            
        except Exception as e:
            # 记录错误但不中断游戏
            self.logger.error(f"observe错误: {e}")

    async def __call__(self, msg: Optional[Msg] = None, **kwargs) -> Msg:
        """处理消息并生成响应（策略集成版）
        
        严格按照赛题要求：
        - 函数签名：async def __call__(self, msg: Msg) -> Msg
        - 函数开始到返回总时间不能超过30秒
        - 返回的Msg内容长度不能超过2048字符
        
        Args:
            msg: 输入消息
            **kwargs: 关键字参数，可能包含structured_model
            
        Returns:
            Msg对象
        """
        start_time = time.time()
        MAX_TIME = 30
        MAX_CHARS = 2048
        
        try:
            # 提取参数
            structured_model = kwargs.get('structured_model')
            
            # 处理位置参数兼容性
            if msg is None and len(kwargs) == 0:
                # 没有参数，返回默认响应
                return Msg(
                    name=self.name,
                    content="等待指令。",
                    role="assistant"
                )
            
            # 如果msg为None但有structured_model，创建空消息
            if msg is None and structured_model:
                msg = Msg(name="System", content="", role="user")
            
            # 使用智能响应器生成响应（集成策略系统）
            response = await self.intelligent_responder.generate_intelligent_response(
                msg=msg,
                structured_model=structured_model
            )
            
            # 检查响应时间
            elapsed = time.time() - start_time
            if elapsed > MAX_TIME:
                self.logger.warning(f"响应超时({elapsed:.2f}s)")
                return Msg(
                    name=self.name,
                    content="思考超时，暂时跳过。",
                    role="assistant"
                )
            
            # 检查响应长度
            if response and response.content and len(response.content) > MAX_CHARS:
                self.logger.warning(f"响应超长({len(response.content)}字符)，截断")
                response.content = response.content[:MAX_CHARS - 3] + "..."
            
            return response
            
        except Exception as e:
            self.logger.error(f"__call__错误: {e}")
            import traceback
            traceback.print_exc()
            # 返回安全的错误响应
            return Msg(
                name=self.name,
                content="遇到问题，需要重新评估。",
                role="assistant"
            )
    

    def state_dict(self) -> dict:
        """保存智能体状态（重构版 - 完整的跨局学习支持）
        
        严格按照赛题要求实现state_dict函数：
        - 将当前智能体的完整状态（如记忆、分析结果、策略参数）序列化为字典
        - 用于跨局保存，支持对手画像和策略学习
        
        Returns:
            dict: 包含智能体完整状态的字典
        """
        state = {
            'name': self.name,
            'current_round': self.current_round,
            'reflection_log': self.reflection_log,
            'timestamp': time.time(),
            'games_played': len(self.reflection_log)
        }
        
        # 保存策略管理器状态（包括所有角色的学习数据）
        if self.strategy_manager:
            state['strategy_manager'] = self.strategy_manager.export_state()
        
        # 保存记忆管理器状态（包括对手画像）
        if self.memory_manager:
            state['memory'] = self.memory_manager.export_memory()
        
        # 保存消息处理器的游戏状态
        if self.message_handler:
            state['game_state'] = self.message_handler.get_game_state()
        
        self.logger.info(f"状态已保存，已进行{state['games_played']}局游戏")
        return state

    def load_state_dict(self, state: dict) -> None:
        """加载智能体状态（重构版 - 完整的跨局学习恢复）
        
        严格按照赛题要求实现load_state_dict函数：
        - 从字典中加载状态，恢复上一局游戏结束时的所有记忆和分析
        - 恢复对手画像、策略学习数据等
        
        Args:
            state: 包含智能体状态的字典
        """
        if not state:
            self.logger.warning("加载的状态为空")
            return
        
        try:
            self.name = state.get('name', self.name)
            self.current_round = state.get('current_round', 0)
            self.reflection_log = state.get('reflection_log', [])
            
            # 恢复策略管理器状态
            if 'strategy_manager' in state and self.strategy_manager:
                self.strategy_manager.load_state(state['strategy_manager'])
                self.logger.info("策略管理器状态已恢复")
            
            # 恢复记忆管理器状态
            if 'memory' in state and self.memory_manager:
                self.memory_manager.import_memory(state['memory'])
                self.logger.info("记忆管理器状态已恢复")
            
            # 恢复游戏状态
            if 'game_state' in state and self.message_handler:
                game_state = state['game_state']
                self.message_handler.game_state.update(game_state)
                self.logger.info("游戏状态已恢复")
            
            games_played = state.get('games_played', 0)
            self.logger.info(f"状态已加载，历史游戏数：{games_played}")
            
        except Exception as e:
            self.logger.error(f"加载状态失败: {e}")
