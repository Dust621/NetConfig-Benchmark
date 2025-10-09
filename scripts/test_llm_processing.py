#!/usr/bin/env python3
"""
测试LLM处理单个文件的效果
"""

from integrate_huawei_data_llm import HuaweiDataLLMIntegrator
import json
import os
from pathlib import Path

def test_single_file():
    """测试处理单个文件"""
    
    # 检查API密钥
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("请设置 OPENAI_API_KEY 环境变量")
        print("例如: export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # 创建处理器实例
    integrator = HuaweiDataLLMIntegrator(api_key=api_key)
    
    # 选择一个测试文件（我们知道这个文件之前处理有问题的）
    test_file = Path("datasets/Huawei/example/1.5.30.1 配置OSPF 基本功能示例.md")
    
    if not test_file.exists():
        print(f"测试文件不存在: {test_file}")
        # 列出可用文件
        example_dir = Path("datasets/Huawei/example")
        if example_dir.exists():
            print("\\n可用文件:")
            for md_file in example_dir.glob("*.md"):
                print(f"  - {md_file.name}")
        return
    
    print(f"测试文件: {test_file}")
    print("=" * 50)
    
    # 处理文件
    result = integrator.process_md_file(test_file)
    
    if result:
        print("\\n✅ LLM处理成功!")
        print("\\n处理结果:")
        print("=" * 50)
        
        # 打印结果的各个部分
        print(f"📍 拓扑: {result.get('topology', 'N/A')}")
        print(f"\\n📋 需求: {result.get('requirement', 'N/A')}")
        
        print(f"\\n🔄 配置步骤 ({len(result.get('steps', []))}):")
        for i, step in enumerate(result.get('steps', []), 1):
            print(f"  {i}. {step}")
        
        print(f"\\n🖥️  设备配置 ({len(result.get('configs', {}))}):")
        for device_name in result.get('configs', {}):
            print(f"  - {device_name}")
        
        print(f"\\n🖼️  相关图片 ({len(result.get('related_images', []))}):")
        for image in result.get('related_images', []):
            print(f"  - {image}")
        
        # 保存测试结果
        output_path = Path("test_llm_output.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\\n💾 结果已保存到: {output_path}")
        
        # 与原始脚本结果比较
        original_file = Path("datasets/Huawei/NE40E_examples/1_OSPF实验/1.5.30.1 配置OSPF 基本功能示例.json")
        if original_file.exists():
            with open(original_file, 'r', encoding='utf-8') as f:
                original_result = json.load(f)
            
            print("\\n🔍 与原始结果对比:")
            print("=" * 30)
            
            # 比较图片匹配
            original_images = set(original_result.get('related_images', []))
            llm_images = set(result.get('related_images', []))
            
            print(f"原始图片: {original_images}")
            print(f"LLM图片:  {llm_images}")
            
            if llm_images == original_images:
                print("✅ 图片匹配完全一致")
            else:
                print("⚠️  图片匹配有差异")
                print(f"  仅原始有: {original_images - llm_images}")
                print(f"  仅LLM有:  {llm_images - original_images}")
    
    else:
        print("❌ LLM处理失败")

if __name__ == "__main__":
    test_single_file()