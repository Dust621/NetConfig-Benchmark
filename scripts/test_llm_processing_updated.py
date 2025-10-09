#!/usr/bin/env python3
"""
测试更新后的LLM处理单个文件的效果
使用集成的LLMClient支持DeepSeek、Claude等多种模型
"""

from integrate_huawei_data_llm import HuaweiDataLLMIntegrator
import json
import os
from pathlib import Path

def test_single_file():
    """测试处理单个文件"""
    
    print("🚀 测试LLM文档处理功能")
    print("=" * 50)
    
    # 检查API密钥
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    claude_key = os.getenv("ANTHROPIC_API_KEY") 
    openai_key = os.getenv("OPENAI_API_KEY")
    
    # 选择可用的提供商
    provider_config = None
    if deepseek_key:
        provider_config = {
            "api_key": deepseek_key,
            "base_url": "https://api.deepseek.com",
            "model": "deepseek-chat"
        }
        print("✅ 使用DeepSeek提供商")
    elif claude_key:
        provider_config = {
            "api_key": claude_key,
            "base_url": "https://chat.cloudapi.vip/v1/",
            "model": "claude-sonnet-4-20250514"
        }
        print("✅ 使用Claude提供商")
    elif openai_key:
        provider_config = {
            "api_key": openai_key,
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4"
        }
        print("✅ 使用OpenAI提供商")
    else:
        print("❌ 请设置以下环境变量之一:")
        print("  - DEEPSEEK_API_KEY")
        print("  - ANTHROPIC_API_KEY")
        print("  - OPENAI_API_KEY")
        return
    
    # 创建处理器实例
    integrator = HuaweiDataLLMIntegrator(**provider_config)
    
    # 选择一个测试文件
    test_files = [
        "1.5.30.1 配置OSPF 基本功能示例.md",
        "1.10.62.12 配置BGP 非等值负载分担示例.md", 
        "1.7.14.1 配置RIP 基本功能示例.md"
    ]
    
    example_dir = Path("datasets/Huawei/example")
    if not example_dir.exists():
        print(f"❌ 测试目录不存在: {example_dir}")
        return
    
    # 找到可用的测试文件
    test_file = None
    for filename in test_files:
        filepath = example_dir / filename
        if filepath.exists():
            test_file = filepath
            break
    
    if not test_file:
        print("❌ 没有找到测试文件，列出可用文件:")
        for md_file in example_dir.glob("*.md"):
            print(f"  - {md_file.name}")
        return
    
    print(f"📄 测试文件: {test_file.name}")
    print("=" * 50)
    
    # 处理文件
    result = integrator.process_md_file(test_file)
    
    if result:
        print("\\n✅ LLM处理成功!")
        print("\\n📊 处理结果分析:")
        print("=" * 50)
        
        # 打印结果的各个部分
        topology = result.get('topology', 'N/A')
        print(f"📍 拓扑描述 ({len(topology)} 字符):")
        print(f"   {topology[:100]}{'...' if len(topology) > 100 else ''}")
        
        requirement = result.get('requirement', 'N/A')
        print(f"\\n📋 组网需求 ({len(requirement)} 字符):")
        print(f"   {requirement[:100]}{'...' if len(requirement) > 100 else ''}")
        
        steps = result.get('steps', [])
        print(f"\\n🔄 配置步骤 ({len(steps)} 步):")
        for i, step in enumerate(steps[:3], 1):  # 只显示前3步
            print(f"   {i}. {step[:60]}{'...' if len(step) > 60 else ''}")
        if len(steps) > 3:
            print(f"   ... 还有 {len(steps) - 3} 步")
        
        configs = result.get('configs', {})
        print(f"\\n🖥️  设备配置 ({len(configs)} 个设备):")
        for device_name, config in list(configs.items())[:3]:  # 只显示前3个设备
            config_lines = len(config.split('\\n'))
            print(f"   - {device_name}: {config_lines} 行配置")
        if len(configs) > 3:
            print(f"   ... 还有 {len(configs) - 3} 个设备")
        
        images = result.get('related_images', [])
        print(f"\\n🖼️  相关图片 ({len(images)} 张):")
        for image in images[:3]:  # 只显示前3张
            image_name = Path(image).name
            print(f"   - {image_name}")
        if len(images) > 3:
            print(f"   ... 还有 {len(images) - 3} 张图片")
        
        # 保存测试结果
        output_path = Path("test_llm_output_updated.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\\n💾 完整结果已保存到: {output_path}")
        
        # 与原始脚本结果比较
        print("\\n🔍 与原始结果对比:")
        print("=" * 30)
        
        original_file = None
        possible_paths = [
            f"datasets/Huawei/NE40E_examples/1_OSPF实验/{test_file.stem}.json",
            f"datasets/Huawei/NE40E_examples/5_BGP实验/{test_file.stem}.json", 
            f"datasets/Huawei/NE40E_examples/3_RIP实验/{test_file.stem}.json"
        ]
        
        for path in possible_paths:
            if Path(path).exists():
                original_file = Path(path)
                break
        
        if original_file:
            with open(original_file, 'r', encoding='utf-8') as f:
                original_result = json.load(f)
            
            # 比较图片匹配
            original_images = set(original_result.get('related_images', []))
            llm_images = set(result.get('related_images', []))
            
            print(f"原始方法图片: {len(original_images)} 张")
            print(f"LLM方法图片:  {len(llm_images)} 张")
            
            if llm_images == original_images:
                print("✅ 图片匹配完全一致")
            else:
                print("⚠️  图片匹配有差异")
                if original_images - llm_images:
                    print("  原始方法独有:")
                    for img in list(original_images - llm_images)[:2]:
                        print(f"    - {Path(img).name}")
                if llm_images - original_images:
                    print("  LLM方法独有:")
                    for img in list(llm_images - original_images)[:2]:
                        print(f"    - {Path(img).name}")
            
            # 比较配置数量
            orig_configs = len(original_result.get('configs', {}))
            llm_configs = len(result.get('configs', {}))
            print(f"\\n配置设备数: 原始 {orig_configs} vs LLM {llm_configs}")
            
            # 比较步骤数量
            orig_steps = len(original_result.get('steps', []))
            llm_steps = len(result.get('steps', []))
            print(f"配置步骤数: 原始 {orig_steps} vs LLM {llm_steps}")
        
        else:
            print("⚠️  未找到对应的原始处理结果进行比较")
    
    else:
        print("❌ LLM处理失败")
        print("可能的原因:")
        print("1. API密钥无效")
        print("2. 网络连接问题")
        print("3. API服务不可用")
        print("4. 文档格式问题")

def test_multiple_files():
    """测试处理多个文件"""
    print("\\n🔬 批量测试模式")
    print("=" * 30)
    
    # 这里可以添加批量测试逻辑
    print("提示: 使用 python integrate_huawei_data_llm.py --limit 3 进行批量测试")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        test_multiple_files()
    else:
        test_single_file()