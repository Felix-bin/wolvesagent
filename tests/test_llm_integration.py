# -*- coding: utf-8 -*-
"""测试LLM服务集成"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_import_llm_service():
    """测试LLM服务模块导入"""
    try:
        from services.llm import LLMClient, LLMProvider, BaseLLMClient
        print("[通过] LLM服务模块导入成功")
        print(f"  - LLMClient: {LLMClient}")
        print(f"  - LLMProvider: {LLMProvider}")
        print(f"  - BaseLLMClient: {BaseLLMClient}")
        return True
    except Exception as e:
        print(f"[失败] LLM服务模块导入失败: {e}")
        return False


def test_enhanced_model_config():
    """测试增强的模型配置"""
    try:
        from config.models import EnhancedModelConfig, create_llm_client, get_enhanced_config
        print("[通过] 增强模型配置导入成功")
        print(f"  - EnhancedModelConfig: {EnhancedModelConfig}")
        print(f"  - create_llm_client: {create_llm_client}")
        print(f"  - get_enhanced_config: {get_enhanced_config}")
        return True
    except Exception as e:
        print(f"[失败] 增强模型配置导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_backward_compatibility():
    """测试向后兼容性"""
    try:
        from config.models import ModelConfig, get_model, model_config
        print("[通过] 原有接口向后兼容")
        print(f"  - ModelConfig: {ModelConfig}")
        print(f"  - get_model: {get_model}")
        print(f"  - model_config: {model_config}")
        return True
    except Exception as e:
        print(f"[失败] 向后兼容性测试失败: {e}")
        return False


def test_enhanced_config_creation():
    """测试增强配置创建（不需要API key）"""
    try:
        from config.models import EnhancedModelConfig
        
        # 手动创建配置（不依赖环境变量）
        config = EnhancedModelConfig(
            model_name="qwen-max",
            provider="dashscope",
            api_key="test_key",
            temperature=0.7,
        )
        
        print("[通过] 增强配置创建成功")
        print(f"  - model_name: {config.model_name}")
        print(f"  - provider: {config.provider}")
        print(f"  - temperature: {config.temperature}")
        return True
    except Exception as e:
        print(f"[失败] 增强配置创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_llm_provider_enum():
    """测试LLM提供商枚举"""
    try:
        from services.llm import LLMProvider
        
        providers = [p.value for p in LLMProvider]
        print("[通过] LLM提供商枚举测试成功")
        print(f"  - 支持的提供商: {providers}")
        
        assert "dashscope" in providers
        assert "openai" in providers
        assert "anthropic" in providers
        
        return True
    except Exception as e:
        print(f"[失败] LLM提供商枚举测试失败: {e}")
        return False


def test_file_structure():
    """测试文件结构"""
    try:
        import os
        
        required_files = [
            "services/__init__.py",
            "services/llm/__init__.py",
            "services/llm/base.py",
            "services/llm/client.py",
            "services/llm/dashscope.py",
            "services/llm/README.md",
            "docs/LLM_SERVICE_INTEGRATION.md",
        ]
        
        all_exist = True
        for file_path in required_files:
            full_path = os.path.join(os.path.dirname(__file__), '..', file_path)
            if os.path.exists(full_path):
                print(f"  [OK] {file_path}")
            else:
                print(f"  [NG] {file_path} (缺失)")
                all_exist = False
        
        if all_exist:
            print("[通过] 文件结构完整")
            return True
        else:
            print("[失败] 部分文件缺失")
            return False
            
    except Exception as e:
        print(f"[失败] 文件结构测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "="*60)
    print("LLM服务集成测试")
    print("="*60 + "\n")
    
    tests = [
        ("文件结构", test_file_structure),
        ("LLM服务模块导入", test_import_llm_service),
        ("增强模型配置", test_enhanced_model_config),
        ("向后兼容性", test_backward_compatibility),
        ("增强配置创建", test_enhanced_config_creation),
        ("LLM提供商枚举", test_llm_provider_enum),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        print("-" * 60)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"[错误] {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试汇总")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{status:4s} | {test_name}")
    
    print("-" * 60)
    print(f"总计: {passed}/{total} 测试通过 ({passed*100//total}%)")
    
    if passed == total:
        print("\n所有测试通过！LLM服务集成成功。")
        return True
    else:
        print(f"\n警告: 有 {total - passed} 个测试失败。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

