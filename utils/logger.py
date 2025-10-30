# -*- coding: utf-8 -*-
"""日志工具模块"""

import logging
import time
import os
from typing import Any, Dict, Optional
from datetime import datetime


class WerewolfLogger:
    """狼人杀游戏专用日志器"""
    
    def __init__(self, name: str = "werewolf", log_level: str = "INFO", log_file: Optional[str] = None):
        """初始化日志器
        
        Args:
            name: 日志器名称
            log_level: 日志级别
            log_file: 日志文件路径，如果为None则只输出到控制台
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # 清除已有的处理器
        self.logger.handlers.clear()
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 文件处理器（如果指定了文件）
        if log_file:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """记录调试信息"""
        self._log(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """记录一般信息"""
        self._log(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """记录警告信息"""
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """记录错误信息"""
        self._log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """记录严重错误信息"""
        self._log(logging.CRITICAL, message, extra)
    
    def _log(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """内部日志记录方法"""
        if extra:
            # 将额外信息添加到消息中
            extra_str = " | ".join([f"{k}={v}" for k, v in extra.items()])
            full_message = f"{message} | {extra_str}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_game_event(self, event_type: str, details: Dict[str, Any]) -> None:
        """记录游戏事件"""
        timestamp = datetime.now().isoformat()
        self.info(f"游戏事件: {event_type}", {"timestamp": timestamp, **details})
    
    def log_player_action(self, player_name: str, action: str, details: Dict[str, Any] = None) -> None:
        """记录玩家行动"""
        self.info(f"玩家行动: {player_name} - {action}", details or {})
    
    def log_role_assignment(self, player_name: str, role: str) -> None:
        """记录角色分配"""
        self.info(f"角色分配: {player_name} -> {role}")
    
    def log_voting_result(self, round_num: int, votes: Dict[str, str], eliminated: Optional[str] = None) -> None:
        """记录投票结果"""
        vote_details = ", ".join([f"{voter}->{target}" for voter, target in votes.items()])
        message = f"第{round_num}轮投票结果: {vote_details}"
        if eliminated:
            message += f" | 淘汰: {eliminated}"
        self.info(message)
    
    def log_night_action(self, round_num: int, action_type: str, actor: str, target: Optional[str] = None) -> None:
        """记录夜晚行动"""
        message = f"第{round_num}轮夜晚行动: {actor} 使用 {action_type}"
        if target:
            message += f" 目标: {target}"
        self.info(message)
    
    def log_game_result(self, winner: str, rounds: int, final_state: Dict[str, Any]) -> None:
        """记录游戏结果"""
        self.info(f"游戏结束: {winner}获胜 | 总轮次: {round_num}", final_state)
    
    def log_agent_thinking(self, agent_name: str, role: str, thinking_process: str) -> None:
        """记录智能体思考过程"""
        self.debug(f"智能体思考: {agent_name}({role})", {"thinking": thinking_process})
    
    def log_model_response(self, model_name: str, prompt_length: int, response_length: int, response_time: float) -> None:
        """记录模型响应信息"""
        self.debug(f"模型响应: {model_name}", {
            "prompt_length": prompt_length,
            "response_length": response_length,
            "response_time": f"{response_time:.2f}s"
        })
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]) -> None:
        """记录带上下文的错误"""
        self.error(f"错误: {type(error).__name__}: {str(error)}", context)
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = "") -> None:
        """记录性能指标"""
        message = f"性能指标: {metric_name}={value}"
        if unit:
            message += unit
        self.info(message)
    
    def log_memory_operation(self, operation: str, details: Dict[str, Any]) -> None:
        """记录记忆操作"""
        self.debug(f"记忆操作: {operation}", details)
    
    def log_strategy_execution(self, agent_name: str, strategy: str, action: str, success: bool) -> None:
        """记录策略执行"""
        status = "成功" if success else "失败"
        self.info(f"策略执行: {agent_name} - {strategy} - {action} - {status}")
    
    def log_state_transition(self, agent_name: str, from_state: str, to_state: str, trigger: str) -> None:
        """记录状态转换"""
        self.debug(f"状态转换: {agent_name} {from_state}->{to_state} 触发: {trigger}")
    
    def log_timeout_event(self, agent_name: str, operation: str, timeout_limit: float, actual_time: float) -> None:
        """记录超时事件"""
        self.warning(f"超时事件: {agent_name} - {operation} | 限制: {timeout_limit}s | 实际: {actual_time:.2f}s")
    
    def log_api_call(self, api_name: str, params: Dict[str, Any], success: bool, response_time: float) -> None:
        """记录API调用"""
        status = "成功" if success else "失败"
        self.debug(f"API调用: {api_name} - {status} - {response_time:.2f}s", params)
    
    def create_session_logger(self, session_id: str) -> 'WerewolfLogger':
        """创建会话专用日志器"""
        session_name = f"werewolf_{session_id}"
        log_file = f"logs/werewolf_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        return WerewolfLogger(session_name, log_file=log_file)


class GameMetrics:
    """游戏指标收集器"""
    
    def __init__(self, logger: WerewolfLogger):
        self.logger = logger
        self.metrics = {
            'total_games': 0,
            'wins': 0,
            'losses': 0,
            'role_performance': {},
            'average_response_time': 0.0,
            'timeout_count': 0,
            'error_count': 0
        }
        self.current_game_metrics = {}
    
    def start_game(self, game_id: str) -> None:
        """开始游戏指标收集"""
        self.current_game_metrics = {
            'game_id': game_id,
            'start_time': time.time(),
            'response_times': [],
            'timeouts': 0,
            'errors': 0,
            'role': None
        }
        self.logger.info(f"开始游戏指标收集: {game_id}")
    
    def end_game(self, result: str, role: str) -> None:
        """结束游戏指标收集"""
        if not self.current_game_metrics:
            return
        
        end_time = time.time()
        duration = end_time - self.current_game_metrics['start_time']
        
        # 更新总体指标
        self.metrics['total_games'] += 1
        
        if 'win' in result.lower() or '胜利' in result:
            self.metrics['wins'] += 1
        else:
            self.metrics['losses'] += 1
        
        # 更新角色表现
        if role not in self.metrics['role_performance']:
            self.metrics['role_performance'][role] = {'wins': 0, 'losses': 0, 'games': 0}
        
        self.metrics['role_performance'][role]['games'] += 1
        if 'win' in result.lower() or '胜利' in result:
            self.metrics['role_performance'][role]['wins'] += 1
        else:
            self.metrics['role_performance'][role]['losses'] += 1
        
        # 更新响应时间指标
        if self.current_game_metrics['response_times']:
            avg_response_time = sum(self.current_game_metrics['response_times']) / len(self.current_game_metrics['response_times'])
            self.metrics['average_response_time'] = (
                (self.metrics['average_response_time'] * (self.metrics['total_games'] - 1) + avg_response_time) 
                / self.metrics['total_games']
            )
        
        # 更新超时和错误计数
        self.metrics['timeout_count'] += self.current_game_metrics['timeouts']
        self.metrics['error_count'] += self.current_game_metrics['errors']
        
        # 记录游戏指标
        self.logger.log_game_result(result, int(duration), {
            'game_id': self.current_game_metrics['game_id'],
            'role': role,
            'avg_response_time': avg_response_time if self.current_game_metrics['response_times'] else 0,
            'timeouts': self.current_game_metrics['timeouts'],
            'errors': self.current_game_metrics['errors']
        })
        
        self.current_game_metrics = {}
    
    def record_response_time(self, response_time: float) -> None:
        """记录响应时间"""
        if self.current_game_metrics:
            self.current_game_metrics['response_times'].append(response_time)
    
    def record_timeout(self) -> None:
        """记录超时"""
        if self.current_game_metrics:
            self.current_game_metrics['timeouts'] += 1
    
    def record_error(self) -> None:
        """记录错误"""
        if self.current_game_metrics:
            self.current_game_metrics['errors'] += 1
    
    def set_role(self, role: str) -> None:
        """设置当前角色"""
        if self.current_game_metrics:
            self.current_game_metrics['role'] = role
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """获取指标摘要"""
        win_rate = self.metrics['wins'] / max(1, self.metrics['total_games']) * 100
        
        return {
            'total_games': self.metrics['total_games'],
            'wins': self.metrics['wins'],
            'losses': self.metrics['losses'],
            'win_rate': f"{win_rate:.1f}%",
            'average_response_time': f"{self.metrics['average_response_time']:.2f}s",
            'timeout_count': self.metrics['timeout_count'],
            'error_count': self.metrics['error_count'],
            'role_performance': self.metrics['role_performance']
        }


# 全局日志器实例
default_logger = WerewolfLogger("werewolf")
