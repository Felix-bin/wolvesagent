# 测试文档

本目录包含LLM服务模块的测试代码。

## 环境配置

### 1. 创建 .env 文件

在项目根目录创建 `.env` 文件（可以从 `.env.example` 复制）：

```bash
cp .env.example .env
```

### 2. 配置环境变量

编辑 `.env` 文件，填入你的配置：

```env
# DashScope API 配置
DASHSCOPE_API_KEY=你的API密钥

# 模型选择
DASHSCOPE_MODEL=qwen3-max

# 可选配置
# TEMPERATURE=0.7
# MAX_TOKENS=2000
```

### 3. 安装依赖

```bash
# 如果使用 uv
uv sync

# 或使用 pip
pip install -e .
```

## 运行测试

### 运行所有测试

```bash
# 使用 pytest
pytest tests/

# 或者显示详细信息
pytest tests/ -v

# 显示测试覆盖率
pytest tests/ --cov=services/llm
```

### 运行特定测试

```bash
# 运行 LLM 服务测试
pytest tests/test_llm_service.py -v

# 运行特定测试类
pytest tests/test_llm_service.py::TestDashScopeLLMService -v

# 运行特定测试方法
pytest tests/test_llm_service.py::TestDashScopeLLMService::test_initialization_with_explicit_api_key -v
```

### 直接运行测试文件

```bash
python tests/test_llm_service.py
```

## 测试结构

### test_llm_service.py

包含以下测试类：

1. **TestBaseLLMService**: 测试基础LLM服务类
   - 测试抽象类不能直接实例化
   - 测试配置管理功能

2. **TestDashScopeLLMService**: 测试DashScope服务
   - 测试初始化（显式API密钥、环境变量）
   - 测试配置验证
   - 测试模型列表获取
   - 测试自定义配置参数

3. **TestDashScopeLLMServiceIntegration**: 集成测试
   - 测试模型创建（需要有效的API密钥）
   - 测试自定义配置的模型创建
   - 测试无效配置处理

## 注意事项

### 集成测试

集成测试类 `TestDashScopeLLMServiceIntegration` 需要有效的 API 密钥才能运行。如果没有设置 `DASHSCOPE_API_KEY` 环境变量，这些测试会自动跳过。

### 跳过集成测试

如果只想运行单元测试，可以使用标记：

```bash
pytest tests/test_llm_service.py -v -k "not Integration"
```

### 测试覆盖率

要生成测试覆盖率报告，首先安装 pytest-cov：

```bash
pip install pytest-cov
```

然后运行：

```bash
# 生成终端报告
pytest tests/ --cov=services/llm --cov-report=term

# 生成HTML报告
pytest tests/ --cov=services/llm --cov-report=html

# 查看HTML报告
open htmlcov/index.html
```

## 添加新测试

在 `tests/` 目录下创建新的测试文件，遵循以下规范：

1. 文件名以 `test_` 开头
2. 测试类以 `Test` 开头
3. 测试方法以 `test_` 开头
4. 使用中文注释说明测试目的
5. 使用类型提示

示例：

```python
# -*- coding: utf-8 -*-
"""新功能测试模块"""
import pytest

class TestNewFeature:
    """新功能测试类"""
    
    def test_something(self) -> None:
        """测试某个功能"""
        assert True
```

## 常见问题

### Q: 提示 "未设置 DASHSCOPE_API_KEY 环境变量"

**A**: 确保在项目根目录创建了 `.env` 文件并配置了正确的 API 密钥。

### Q: 导入模块失败

**A**: 确保已经安装了项目依赖：
```bash
uv sync
# 或
pip install -e .
```

### Q: pytest 命令不存在

**A**: 安装 pytest：
```bash
pip install pytest
```

## 持续集成

可以在 CI/CD 流程中运行测试。示例 GitHub Actions 配置：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          pip install -e .
      - name: Run tests
        run: |
          pytest tests/ -v
        env:
          DASHSCOPE_API_KEY: ${{ secrets.DASHSCOPE_API_KEY }}
```

