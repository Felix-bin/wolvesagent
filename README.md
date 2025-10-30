# 狼人杀AI智能体

基于AgentScope 1.0框架开发的智能狼人杀Agent，完全符合狼人杀Agent挑战赛要求，支持多角色策略和跨局学习。

## 🎯 项目状态

| 指标 | 状态 |
|------|------|
| **版本** | v0.2.1 |
| **规则符合性** | ✅ 100% |
| **测试通过率** | ✅ 100% (18/18) |
| **最后更新** | 2025-10-30 |

## ✨ 核心特性

### 🏆 竞赛合规性
- ✅ **完全符合比赛要求**：严格遵循所有强制技术规范
- ✅ **基于AgentScope 1.0**：继承自ReActAgent基类
- ✅ **官方兼容性**：通过官方测试环境验证
- ✅ **解耦架构设计**：模块化实现，易于维护和扩展

### 🤖 智能化能力
- ✅ **多角色支持**：狼人、村民、先知、女巫、猎人五种角色专门策略
- ✅ **跨局学习**：完整的对手画像系统和状态持久化
- ✅ **结构化推理**：基于Pydantic BaseModel的稳定输出
- ✅ **自适应策略**：根据游戏状态和角色动态调整

### 🛡️ 安全保障
- ✅ **时间控制**：30秒超时保护和自动降级
- ✅ **长度限制**：2048字符自动截断
- ✅ **错误处理**：多层异常处理和优雅降级
- ✅ **隐私保护**：无硬编码密钥，环境变量管理

## 📁 项目结构

```
wolf/
├── agent.py                    # 🎯 官方入口文件
├── requirements.txt             # 📦 项目依赖
├── README.md                   # 📖 项目说明
│
├── agents/                     # 🤖 智能体模块
│   └── player_agent.py         # PlayerAgent核心实现
│
├── core/                       # ⚙️ 核心组件
│   ├── message_handler.py      # 消息处理器
│   ├── strategy_manager.py     # 策略管理器
│   ├── response_generator.py   # 响应生成器
│   └── intelligent_responder.py # 智能响应器
│
├── strategies/                 # 🎭 角色策略
│   ├── base_strategy.py        # 策略基类
│   ├── werewolf_strategy.py    # 狼人策略
│   ├── seer_strategy.py        # 先知策略
│   ├── witch_strategy.py       # 女巫策略
│   ├── hunter_strategy.py      # 猎人策略
│   └── villager_strategy.py    # 村民策略
│
├── models/                     # 🧠 数据模型
│   ├── memory.py               # 记忆管理
│   ├── reasoning.py            # 推理模型
│   ├── structured_models.py    # 结构化输出模型
│   └── chain_of_thought.py     # 思维链模型
│
├── utils/                      # 🔧 工具模块
│   ├── parser.py               # 消息解析器
│   ├── logger.py               # 日志系统
│   └── official_compatibility.py # 官方兼容性
│
├── config/                     # ⚙️ 配置管理
│   ├── model_config.yaml       # 模型配置
│   ├── models.py               # 模型工厂
│   └── env_config.py           # 环境配置
│
├── services/                   # 🌐 服务模块
│   └── llm/                    # LLM服务
│       ├── base.py             # 基类定义
│       ├── client.py           # 客户端
│       ├── dashscope.py        # DashScope实现
│       └── README.md           # API文档
│
├── tests/                      # 🧪 测试套件
│   ├── test_basic_functionality.py
│   ├── test_strategy_integration.py
│   ├── test_comprehensive_strategy.py
│   ├── test_llm_integration.py
│   ├── test_nine_agents_battle.py
│   ├── test_official_game.py
│   ├── run_game.py             # 游戏运行脚本
│   └── check_env.py            # 环境检查
│
├── docs/                       # 📚 文档
│   ├── COMPLIANCE_CHECK.md     # 规则符合性检查
│   
│  
│
└── werewolves/                 # 🏛️ 官方测试环境
    ├── game.py
    ├── main.py
    └── ...
```

## 🚀 快速开始

### 1. 环境准备

**系统要求**:
- Python 3.8+
- Windows/Linux/macOS

**依赖安装**:
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

创建`.env`文件（或设置环境变量）：

```env
# 必需：DashScope API密钥
DASHSCOPE_API_KEY=your_api_key_here

# 可选：模型配置
DASHSCOPE_MODEL_NAME=qwen-max
MODEL_TEMPERATURE=0.7
MODEL_MAX_TOKENS=2048
```

**获取API密钥**：
- 访问 [阿里云DashScope](https://dashscope.console.aliyun.com/apiKey)
- 注册并获取API密钥

### 3. 运行测试

**基础功能测试**:
```bash
python tests/test_basic_functionality.py
```

**环境检查**:
```bash
python tests/check_env.py
```

**完整游戏测试**:
```bash
python tests/test_nine_agents_battle.py
```

### 4. 集成到官方测试环境

```python
from agent import PlayerAgent

# 创建智能体
agent = PlayerAgent(name="Player1")

# 在官方测试程序中使用
players = [PlayerAgent(name=f"Player{i+1}") for i in range(9)]
```

## 🎮 使用说明

### 基础使用

```python
from agent import PlayerAgent
from agentscope.message import Msg

# 创建智能体
agent = PlayerAgent(name="TestPlayer")

# 接收游戏信息
role_msg = Msg(
    name="Moderator",
    content="[TestPlayer ONLY] TestPlayer, your role is werewolf.",
    role="system"
)
await agent.observe(role_msg)

# 生成响应
response = await agent(Msg(
    name="Moderator",
    content="Please introduce yourself.",
    role="user"
))

print(response.content)
```

### 状态持久化

```python
# 保存状态（跨局学习）
state = agent.state_dict()

# 加载状态
new_agent = PlayerAgent(name="TestPlayer")
new_agent.load_state_dict(state)
```

### 结构化输出

```python
from models.structured_models import VoteModel

# 使用结构化模型
response = await agent(
    msg=vote_msg,
    structured_model=VoteModel
)
```

## 🧪 测试指南

### 测试套件

| 测试文件 | 功能 | 运行命令 |
|---------|------|---------|
| `check_env.py` | 环境检查 | `python tests/check_env.py` |
| `test_basic_functionality.py` | 基础功能 | `python tests/test_basic_functionality.py` |
| `test_strategy_integration.py` | 策略集成 | `python tests/test_strategy_integration.py` |
| `test_llm_integration.py` | LLM集成 | `python tests/test_llm_integration.py` |
| `test_nine_agents_battle.py` | 9人对战 | `python tests/test_nine_agents_battle.py` |
| `test_official_game.py` | 官方兼容 | `python tests/test_official_game.py` |

### 快速测试流程

```bash
# 1. 环境检查
python tests/check_env.py

# 2. 基础功能测试
python tests/test_basic_functionality.py

# 3. 完整游戏测试
python tests/run_game.py
```

## 📊 技术实现

### 核心接口

#### 1. observe函数
```python
async def observe(self, msg) -> None:
    """接收游戏环境信息并更新内部状态
    
    - 处理法官指令
    - 记录玩家发言
    - 更新游戏状态
    - 识别角色分配
    """
```

#### 2. __call__函数
```python
async def __call__(self, msg: Optional[Msg] = None, **kwargs) -> Msg:
    """处理消息并生成响应
    
    严格限制：
    - 时间限制：≤ 30秒
    - 长度限制：≤ 2048字符
    - 返回合法Msg对象
    """
```

#### 3. 状态管理
```python
def state_dict(self) -> dict:
    """保存完整状态（跨局学习）"""

def load_state_dict(self, state: dict) -> None:
    """恢复状态（对手画像、历史记录）"""
```

### 角色策略

每个角色都有专门的策略实现：

- **狼人**：伪装、配合、欺骗（支持自刀、悍跳等高级战术框架）
- **先知**：查验、警徽流、信息公开
- **女巫**：药水使用决策、关键角色保护
- **猎人**：技能使用时机、目标选择
- **村民**：逻辑分析、信息收集、投票跟随

### 记忆系统

```python
# 对话记忆
memory_manager.add_conversation(player, content)
recent = memory_manager.get_recent_conversations(5)

# 对手画像
memory_manager.update_player_profile(player, role_guess, trust_score)
profile = memory_manager.get_player_profile(player)

# 游戏历史
memory_manager.add_game_record(game_num, result, role)
history = memory_manager.get_game_history()
```


## 🎯 竞赛符合性

### 强制要求 ✅

| 要求项 | 状态 | 说明 |
|--------|------|------|
| 基于AgentScope 1.0 | ✅ | 继承ReActAgent |
| observe函数 | ✅ | 完整实现 |
| __call__函数 | ✅ | 30s + 2048字符限制 |
| state_dict/load_state_dict | ✅ | 跨局状态管理 |
| BaseModel结构化输出 | ✅ | 完整支持 |
| 类名PlayerAgent | ✅ | 符合规范 |
| 构造函数name参数 | ✅ | 只接受name |
| requirements.txt | ✅ | 仅自定义依赖 |

详细检查报告：[docs/COMPLIANCE_CHECK.md](docs/COMPLIANCE_CHECK.md)

### 提交文件清单

```
提交包/
├── agent.py              # 必需：入口文件
├── agents/               # 智能体实现
├── core/                 # 核心组件
├── strategies/           # 角色策略
├── models/               # 数据模型
├── utils/                # 工具模块
├── config/               # 配置文件
├── services/             # 服务模块
├── requirements.txt      # 必需：依赖列表
└── README.md            # 项目说明
```

## 🔧 配置选项

### 支持的模型

在`config/model_config.yaml`中配置：

```yaml
models:
  glm-4.5-air:          # GLM-4.5-Air
  qwen-max:             # Qwen-Max
  qwen3-max:            # Qwen3-Max  
  deepseek-v3:          # DeepSeek-V3
  deepseek-v3.2-exp:    # DeepSeek-V3.2-Exp
```

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| DASHSCOPE_API_KEY | API密钥 | 必需 |
| DASHSCOPE_MODEL_NAME | 模型名称 | qwen-max |
| MODEL_TEMPERATURE | 温度参数 | 0.7 |
| MODEL_MAX_TOKENS | 最大令牌数 | 2048 |
| MODEL_STREAM | 流式输出 | false |
| LOG_LEVEL | 日志级别 | INFO |

## 🐛 问题排查

### 常见问题

**1. API连接失败**
```bash
# 检查环境变量
python tests/check_env.py

# 确认API密钥设置
echo $DASHSCOPE_API_KEY
```

**2. 响应超时**
- 检查网络连接
- 尝试更换模型（glm-4.5-air响应更快）
- 简化输入内容


## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 平均响应时间 | < 5秒 |
| 最大响应时间 | < 30秒 |
| 响应长度 | ≤ 2048字符 |
| 内存使用 | < 500MB |
| 测试通过率 | 100% |

## 🤝 贡献与支持

### 项目维护

- 定期更新依赖版本
- 修复已知问题
- 优化策略性能


## 📄 许可证

本项目遵循狼人杀Agent挑战赛的规则和要求。

## 🎉 致谢

感谢AgentScope团队提供的优秀框架和官方测试环境。


