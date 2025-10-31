# -*- coding: utf-8 -*-
"""消息处理器 - 负责解析游戏环境消息"""

import re
import time
from typing import Dict, List, Any, Optional
from agentscope.message import Msg


class MessageHandler:
    """消息处理器 - 统一处理各种游戏消息"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.game_state = {
            'phase': 'unknown',  # night, day, discussion, voting
            'round': 0,
            'role': None,
            'alive_players': [],
            'dead_players': [],
            'last_night_result': {}
        }
    
    def process_message(self, msg) -> Dict[str, Any]:
        """处理消息并更新游戏状态
        
        Args:
            msg: 消息对象，可以是Msg、list、dict或str
            
        Returns:
            解析后的消息信息
        """
        messages = self._normalize_message(msg)
        
        parsed_info = {
            'messages': [],
            'phase_change': None,
            'role_assigned': None,
            'player_died': [],
            'voting_result': None
        }
        
        for single_msg in messages:
            content = self._extract_content(single_msg)
            sender = self._extract_sender(single_msg)
            
            if not content:
                continue
            
            # 保存消息
            parsed_info['messages'].append({
                'sender': sender,
                'content': content,
                'timestamp': time.time()
            })
            
            # 解析特殊信息
            self._parse_role_assignment(content, parsed_info)
            self._parse_phase_change(content, parsed_info)
            self._parse_death_info(content, parsed_info)
            self._parse_voting_info(content, parsed_info)
        
        return parsed_info
    
    def _normalize_message(self, msg) -> List:
        """规范化消息为列表"""
        if msg is None:
            return []
        
        if isinstance(msg, list):
            return msg
        else:
            return [msg]
    
    def _extract_content(self, msg) -> str:
        """提取消息内容"""
        if isinstance(msg, Msg):
            return msg.content
        elif isinstance(msg, dict):
            return msg.get('content', '')
        elif isinstance(msg, str):
            return msg
        elif hasattr(msg, 'content'):
            return msg.content
        else:
            return str(msg)
    
    def _extract_sender(self, msg) -> str:
        """提取发送者"""
        if isinstance(msg, Msg):
            return msg.name
        elif isinstance(msg, dict):
            return msg.get('name', 'Unknown')
        elif hasattr(msg, 'name'):
            return msg.name
        else:
            return 'Unknown'
    
    def _parse_role_assignment(self, content: str, parsed_info: Dict) -> None:
        """解析角色分配（支持多种格式）"""
        # 格式1: [Player1 ONLY] your role is werewolf
        pattern1 = rf"\[{self.agent_name} ONLY\].*your role is (\w+)"
        match = re.search(pattern1, content, re.IGNORECASE)
        
        if match:
            role = match.group(1).lower()
            parsed_info['role_assigned'] = role
            self.game_state['role'] = role
            return
        
        # 格式2: Player1，你的角色是狼人
        pattern2 = rf"{self.agent_name}.*?角色是(\S+)"
        match = re.search(pattern2, content)
        
        if match:
            role_cn = match.group(1).strip('。')
            # 中文角色映射到英文
            role_map = {
                '狼人': 'werewolf',
                '先知': 'seer',
                '女巫': 'witch',
                '猎人': 'hunter',
                '村民': 'villager'
            }
            role = role_map.get(role_cn, role_cn)
            parsed_info['role_assigned'] = role
            self.game_state['role'] = role
            return
        
        # 格式3: your role is werewolf (不带玩家名)
        pattern3 = r"your role is (\w+)"
        match = re.search(pattern3, content, re.IGNORECASE)
        
        if match:
            role = match.group(1).lower()
            parsed_info['role_assigned'] = role
            self.game_state['role'] = role
    
    def _parse_phase_change(self, content: str, parsed_info: Dict) -> None:
        """解析阶段变化"""
        content_lower = content.lower()
        
        if "night has fallen" in content_lower or "天黑了" in content:
            parsed_info['phase_change'] = 'night'
            self.game_state['phase'] = 'night'
        elif "the day is coming" in content_lower or "天亮了" in content:
            parsed_info['phase_change'] = 'day'
            self.game_state['phase'] = 'day'
        elif "discuss" in content_lower or "讨论" in content:
            parsed_info['phase_change'] = 'discussion'
            self.game_state['phase'] = 'discussion'
        elif "vote" in content_lower or "投票" in content:
            if "result" not in content_lower and "结果" not in content:
                parsed_info['phase_change'] = 'voting'
                self.game_state['phase'] = 'voting'
    
    def _parse_death_info(self, content: str, parsed_info: Dict) -> None:
        """解析死亡信息"""
        # 匹配: "Player1 was eliminated" or "Player1 died"
        death_patterns = [
            r"(\w+) (?:was eliminated|died|被淘汰|死亡)",
            r"(?:eliminated|died|淘汰|死亡).*?(\w+)"
        ]
        
        for pattern in death_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                player_name = match.group(1)
                if player_name and player_name not in parsed_info['player_died']:
                    parsed_info['player_died'].append(player_name)
                    if player_name not in self.game_state['dead_players']:
                        self.game_state['dead_players'].append(player_name)
                    if player_name in self.game_state['alive_players']:
                        self.game_state['alive_players'].remove(player_name)
    
    def _parse_voting_info(self, content: str, parsed_info: Dict) -> None:
        """解析投票信息"""
        # 匹配投票结果
        vote_pattern = r"(?:voted for|投给了|vote:)\s*(\w+)"
        match = re.search(vote_pattern, content)
        
        if match:
            target = match.group(1)
            parsed_info['voting_result'] = target
    
    def get_game_state(self) -> Dict[str, Any]:
        """获取当前游戏状态"""
        return self.game_state.copy()
    
    def update_alive_players(self, players: List[str]) -> None:
        """更新存活玩家列表"""
        self.game_state['alive_players'] = [p for p in players if p != self.agent_name]
    
    def get_current_role(self) -> Optional[str]:
        """获取当前角色"""
        return self.game_state.get('role')
    
    def get_current_phase(self) -> str:
        """获取当前阶段"""
        return self.game_state.get('phase', 'unknown')

