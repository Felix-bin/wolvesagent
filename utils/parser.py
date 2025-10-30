# -*- coding: utf-8 -*-
"""法官信息 (env_info) 解析器"""

import re
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from models.reasoning import GameObservation, PlayerInfo


class EnvInfoParser:
    """环境信息解析器"""
    
    def __init__(self):
        self.current_phase = "unknown"
        self.current_round = 0
        self.alive_players = []
        self.dead_players = []
        self.player_roles = {}  # 已知的角色信息
        self.game_history = []
        
    def parse_env_info(self, env_info: Any) -> GameObservation:
        """解析环境信息为结构化数据
        
        Args:
            env_info: 环境信息（可能是字典、字符串或消息对象）
            
        Returns:
            GameObservation: 结构化的游戏观察信息
        """
        # 标准化输入
        if isinstance(env_info, dict):
            info_dict = env_info
        elif isinstance(env_info, str):
            info_dict = self._parse_string_to_dict(env_info)
        else:
            # 尝试转换为字符串再解析
            info_dict = self._parse_string_to_dict(str(env_info))
        
        # 解析各个字段
        phase = self._extract_phase(info_dict)
        round_num = self._extract_round(info_dict)
        alive_players = self._extract_alive_players(info_dict)
        dead_players = self._extract_dead_players(info_dict)
        current_speaker = self._extract_current_speaker(info_dict)
        game_status = self._extract_game_status(info_dict)
        winner = self._extract_winner(info_dict)
        
        # 更新内部状态
        self.current_phase = phase
        self.current_round = round_num
        self.alive_players = alive_players
        self.dead_players = dead_players
        
        # 创建观察对象
        observation = GameObservation(
            phase=phase,
            round=round_num,
            alive_players=alive_players,
            dead_players=dead_players,
            current_speaker=current_speaker
        )
        
        # 记录到历史
        self._record_to_history(observation, info_dict)
        
        return observation
    
    def _parse_string_to_dict(self, text: str) -> Dict[str, Any]:
        """将字符串解析为字典"""
        # 尝试JSON解析
        if text.strip().startswith('{') and text.strip().endswith('}'):
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
        
        # 使用正则表达式提取关键信息
        result = {}
        
        # 提取阶段信息
        phase_patterns = [
            r'阶段[：:]\s*(\w+)',
            r'phase[：:]\s*(\w+)',
            r'(\w+)阶段',
            r'(\w+)phase'
        ]
        for pattern in phase_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result['phase'] = match.group(1).lower()
                break
        
        # 提取回合信息
        round_patterns = [
            r'第(\d+)轮',
            r'round\s*(\d+)',
            r'回合[：:]\s*(\d+)'
        ]
        for pattern in round_patterns:
            match = re.search(pattern, text)
            if match:
                result['round'] = int(match.group(1))
                break
        
        # 提取存活玩家
        alive_patterns = [
            r'存活[：:]\s*([^。\n]+)',
            r'alive[：:]\s*([^。\n]+)',
            r'存活玩家[：:]\s*([^。\n]+)'
        ]
        for pattern in alive_patterns:
            match = re.search(pattern, text)
            if match:
                players_text = match.group(1)
                result['alive_players'] = self._parse_player_list(players_text)
                break
        
        # 提取死亡玩家
        dead_patterns = [
            r'死亡[：:]\s*([^。\n]+)',
            r'dead[：:]\s*([^。\n]+)',
            r'死亡玩家[：:]\s*([^。\n]+)'
        ]
        for pattern in dead_patterns:
            match = re.search(pattern, text)
            if match:
                players_text = match.group(1)
                result['dead_players'] = self._parse_player_list(players_text)
                break
        
        # 提取当前发言者
        speaker_patterns = [
            r'(\w+)发言',
            r'(\w+)speaking',
            r'当前发言[：:]\s*(\w+)'
        ]
        for pattern in speaker_patterns:
            match = re.search(pattern, text)
            if match:
                result['current_speaker'] = match.group(1)
                break
        
        # 提取游戏状态
        if '游戏结束' in text or 'game over' in text.lower():
            result['game_status'] = 'ended'
        elif '进行中' in text or 'ongoing' in text.lower():
            result['game_status'] = 'ongoing'
        else:
            result['game_status'] = 'unknown'
        
        # 提取获胜者
        winner_patterns = [
            r'(\w+)获胜',
            r'(\w+)胜利',
            r'winner[：:]\s*(\w+)'
        ]
        for pattern in winner_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result['winner'] = match.group(1)
                break
        
        return result
    
    def _parse_player_list(self, text: str) -> List[str]:
        """解析玩家列表"""
        # 移除常见的分隔符和标点
        cleaned = re.sub(r'[，,、\s]+', ' ', text)
        cleaned = cleaned.strip()
        
        if not cleaned:
            return []
        
        # 分割玩家名称
        players = [player.strip() for player in cleaned.split(' ') if player.strip()]
        
        # 过滤掉非玩家名称的词汇
        filtered_players = []
        for player in players:
            if len(player) > 0 and not player in ['玩家', 'player', '等', 'etc']:
                filtered_players.append(player)
        
        return filtered_players
    
    def _extract_phase(self, info_dict: Dict[str, Any]) -> str:
        """提取游戏阶段"""
        phase_keys = ['phase', '阶段', 'stage']
        for key in phase_keys:
            if key in info_dict:
                phase = str(info_dict[key]).lower()
                if 'night' in phase or '夜晚' in phase:
                    return 'night'
                elif 'day' in phase or '白天' in phase:
                    return 'day'
                else:
                    return phase
        return 'unknown'
    
    def _extract_round(self, info_dict: Dict[str, Any]) -> int:
        """提取回合数"""
        round_keys = ['round', '回合', '轮次']
        for key in round_keys:
            if key in info_dict:
                try:
                    return int(info_dict[key])
                except (ValueError, TypeError):
                    continue
        return self.current_round
    
    def _extract_alive_players(self, info_dict: Dict[str, Any]) -> List[str]:
        """提取存活玩家列表"""
        alive_keys = ['alive_players', 'alive', '存活玩家', '存活']
        for key in alive_keys:
            if key in info_dict:
                players = info_dict[key]
                if isinstance(players, list):
                    return [str(p) for p in players]
                elif isinstance(players, str):
                    return self._parse_player_list(players)
        return self.alive_players
    
    def _extract_dead_players(self, info_dict: Dict[str, Any]) -> List[str]:
        """提取死亡玩家列表"""
        dead_keys = ['dead_players', 'dead', '死亡玩家', '死亡']
        for key in dead_keys:
            if key in info_dict:
                players = info_dict[key]
                if isinstance(players, list):
                    return [str(p) for p in players]
                elif isinstance(players, str):
                    return self._parse_player_list(players)
        return self.dead_players
    
    def _extract_current_speaker(self, info_dict: Dict[str, Any]) -> Optional[str]:
        """提取当前发言者"""
        speaker_keys = ['current_speaker', 'speaker', '当前发言者', '发言者']
        for key in speaker_keys:
            if key in info_dict:
                return str(info_dict[key])
        return None
    
    def _extract_game_status(self, info_dict: Dict[str, Any]) -> str:
        """提取游戏状态"""
        status_keys = ['game_status', 'status', '游戏状态']
        for key in status_keys:
            if key in info_dict:
                return str(info_dict[key]).lower()
        
        # 根据其他信息推断状态
        if 'winner' in info_dict or '获胜' in str(info_dict):
            return 'ended'
        elif self.alive_players:
            return 'ongoing'
        else:
            return 'unknown'
    
    def _extract_winner(self, info_dict: Dict[str, Any]) -> Optional[str]:
        """提取获胜者"""
        winner_keys = ['winner', '获胜者', '胜利阵营']
        for key in winner_keys:
            if key in info_dict:
                return str(info_dict[key])
        return None
    
    def _record_to_history(self, observation: GameObservation, raw_info: Dict[str, Any]) -> None:
        """记录到历史"""
        # 手动构建字典，因为GameObservation没有dict方法
        observation_dict = {
            'phase': observation.phase.value if hasattr(observation.phase, 'value') else str(observation.phase),
            'round': observation.round,
            'alive_players': observation.alive_players,
            'dead_players': observation.dead_players,
            'current_speaker': observation.current_speaker
        }
        
        history_entry = {
            'timestamp': time.time(),
            'observation': observation_dict,
            'raw_info': raw_info
        }
        self.game_history.append(history_entry)
        
        # 限制历史长度
        if len(self.game_history) > 1000:
            self.game_history = self.game_history[-500:]
    
    def get_player_info(self, player_name: str) -> PlayerInfo:
        """获取玩家信息"""
        is_alive = player_name in self.alive_players
        is_dead = player_name in self.dead_players
        
        # 从历史中查找角色信息
        role = self.player_roles.get(player_name)
        
        # 计算信任分数（基于历史行为）
        trust_score = self._calculate_trust_score(player_name)
        
        # 计算可疑程度
        suspicion_level = self._calculate_suspicion_level(player_name)
        
        # 获取最后行动
        last_action = self._get_last_action(player_name)
        
        # 获取投票历史
        voting_history = self._get_voting_history(player_name)
        
        return PlayerInfo(
            name=player_name,
            role=role,
            status='alive' if is_alive else 'dead' if is_dead else 'unknown',
            trust_score=trust_score,
            suspicion_level=suspicion_level,
            last_action=last_action,
            voting_history=voting_history
        )
    
    def _calculate_trust_score(self, player_name: str) -> float:
        """计算信任分数"""
        # 基础分数
        base_score = 0.5
        
        # 根据历史行为调整
        for entry in self.game_history[-20:]:  # 只看最近20条记录
            raw_info = entry.get('raw_info', {})
            # 这里可以根据具体的行为模式调整信任分数
            # 暂时返回基础分数
            pass
        
        return base_score
    
    def _calculate_suspicion_level(self, player_name: str) -> float:
        """计算可疑程度"""
        # 基础可疑程度
        base_suspicion = 0.3
        
        # 根据行为模式调整
        # 暂时返回基础值
        return base_suspicion
    
    def _get_last_action(self, player_name: str) -> Optional[str]:
        """获取最后行动"""
        # 从历史中查找该玩家的最后行动
        for entry in reversed(self.game_history[-10:]):
            raw_info = entry.get('raw_info', {})
            if 'actions' in raw_info and player_name in raw_info['actions']:
                return str(raw_info['actions'][player_name])
        return None
    
    def _get_voting_history(self, player_name: str) -> List[str]:
        """获取投票历史"""
        voting_history = []
        for entry in self.game_history:
            raw_info = entry.get('raw_info', {})
            if 'votes' in raw_info and player_name in raw_info['votes']:
                voting_history.append(str(raw_info['votes'][player_name]))
        return voting_history
    
    def update_role_info(self, player_name: str, role: str) -> None:
        """更新角色信息"""
        self.player_roles[player_name] = role
    
    def get_game_summary(self) -> Dict[str, Any]:
        """获取游戏摘要"""
        return {
            'current_phase': self.current_phase,
            'current_round': self.current_round,
            'alive_count': len(self.alive_players),
            'dead_count': len(self.dead_players),
            'alive_players': self.alive_players.copy(),
            'dead_players': self.dead_players.copy(),
            'known_roles': self.player_roles.copy()
        }
