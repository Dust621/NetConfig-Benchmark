#!/usr/bin/env python3
"""
测试多模态拓扑增强功能
"""

import os
import json
from pathlib import Path
from enhance_topology_with_images import TopologyEnhancer

def test_multimodal_enhancement():
    """测试多模态拓扑增强功能"""
    
    print("🧪 测试多模态拓扑增强功能")
    print("=" * 50)
    
    # 检查API密钥
    providers = {
        "openai": {
            "env": "OPENAI_API_KEY",
            "model": "gpt-4o",
            "description": "OpenAI GPT-4o"
        },
        "claude": {
            "env": "ANTHROPIC_API_KEY", 
            "model": "claude-3-sonnet-20240229",
            "description": "Claude 3 Sonnet"
        },
        "gemini": {
            "env": "GOOGLE_API_KEY",
            "model": "gemini-1.5-pro", 
            "description": "Google Gemini 1.5 Pro"
        }
    }
    
    # 选择可用的提供商
    available_provider = None
    for provider, config in providers.items():
        if os.getenv(config["env"]):
            available_provider = provider
            print(f"✅ 使用{config['description']}")
            break
    
    if not available_provider:
        print("❌ 请设置以下环境变量之一:")
        for provider, config in providers.items():
            print(f"  - {config['env']} (for {config['description']})")
        return
    
    # 创建增强器
    enhancer = TopologyEnhancer(provider=available_provider)
    
    # 查找测试文件
    test_dirs = [
        "datasets/Huawei/llm_integrated_data",
        "datasets/Huawei/NE40E_examples"
    ]
    
    test_file = None
    for test_dir in test_dirs:
        test_dir_path = Path(test_dir)
        if test_dir_path.exists():
            # 查找有图片的JSON文件
            json_files = list(test_dir_path.glob("**/*.json"))
            for json_file in json_files:
                if json_file.name.startswith("_"):  # 跳过统计文件
                    continue
                
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # 检查是否有相关图片
                    related_images = data.get("related_images", [])
                    if related_images and len(related_images) > 0:
                        # 验证图片文件是否存在
                        has_valid_images = False
                        for img_path in related_images:
                            if isinstance(img_path, str):
                                if img_path.startswith("datasets/"):
                                    img_file = Path(img_path)
                                else:
                                    img_file = Path("datasets/Huawei/extracted_images") / Path(img_path).name
                                
                                if img_file.exists():
                                    has_valid_images = True
                                    break
                        
                        if has_valid_images:
                            test_file = json_file
                            break
                            
                except:
                    continue
            
            if test_file:
                break
    
    if not test_file:
        print("❌ 没有找到包含有效图片的JSON测试文件")
        print("\\n可用的JSON文件:")
        for test_dir in test_dirs:
            test_dir_path = Path(test_dir)
            if test_dir_path.exists():
                for json_file in list(test_dir_path.glob("**/*.json"))[:5]:
                    print(f"  - {json_file}")
        return
    
    print(f"📄 测试文件: {test_file}")
    
    # 读取文件内容
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\\n📊 文件信息:")
    print(f"   当前拓扑长度: {len(data.get('topology', ''))} 字符")
    print(f"   相关图片数量: {len(data.get('related_images', []))}")
    
    # 显示相关图片
    print(f"\\n🖼️  相关图片:")
    for i, img_path in enumerate(data.get('related_images', [])[:3]):
        img_name = Path(img_path).name if isinstance(img_path, str) else str(img_path)
        print(f"   {i+1}. {img_name}")
    
    print(f"\\n📝 当前拓扑描述:")
    current_topology = data.get('topology', '')
    print(f"   {current_topology[:150]}{'...' if len(current_topology) > 150 else ''}")
    
    # 创建测试副本
    test_copy_path = test_file.parent / f"test_enhanced_{test_file.name}"
    with open(test_copy_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\\n🚀 开始多模态增强...")
    print("=" * 30)
    
    # 执行增强
    success = enhancer.enhance_single_json(test_copy_path)
    
    if success:
        # 读取增强后的结果
        with open(test_copy_path, 'r', encoding='utf-8') as f:
            enhanced_data = json.load(f)
        
        print(f"\\n✅ 增强完成!")
        print(f"\\n📈 增强效果对比:")
        print("=" * 30)
        
        original_topology = enhanced_data.get('topology_original', '')
        enhanced_topology = enhanced_data.get('topology', '')
        
        print(f"原始描述 ({len(original_topology)} 字符):")
        print(f"   {original_topology[:100]}{'...' if len(original_topology) > 100 else ''}")
        print(f"\\n增强描述 ({len(enhanced_topology)} 字符):")
        print(f"   {enhanced_topology[:200]}{'...' if len(enhanced_topology) > 200 else ''}")
        
        # 计算增强倍数
        if len(original_topology) > 0:
            enhancement_ratio = len(enhanced_topology) / len(original_topology)
            print(f"\\n📊 增强倍数: {enhancement_ratio:.2f}x")
        
        print(f"\\n💾 增强结果已保存到: {test_copy_path}")
        
        # 显示完整的增强描述
        print(f"\\n📋 完整增强描述:")
        print("=" * 30)
        print(enhanced_topology)
        
    else:
        print(f"❌ 增强失败")
        # 删除测试副本
        if test_copy_path.exists():
            test_copy_path.unlink()

def show_multimodal_models():
    """显示支持多模态的模型列表"""
    print("\\n🤖 支持多模态API的模型:")
    print("=" * 40)
    
    models = [
        {
            "provider": "OpenAI",
            "models": ["gpt-4o", "gpt-4o-mini"],
            "env": "OPENAI_API_KEY",
            "features": "图片理解最稳定，支持高分辨率",
            "cost": "中等"
        },
        {
            "provider": "Claude",
            "models": ["claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
            "env": "ANTHROPIC_API_KEY", 
            "features": "理解能力强，输出质量高",
            "cost": "中等"
        },
        {
            "provider": "Google Gemini",
            "models": ["gemini-1.5-pro", "gemini-1.5-flash"],
            "env": "GOOGLE_API_KEY",
            "features": "性价比高，支持长上下文",
            "cost": "低"
        },
        {
            "provider": "阿里云",
            "models": ["qwen-vl-max", "qwen-vl-plus"],
            "env": "DASHSCOPE_API_KEY",
            "features": "中文理解好，价格便宜",
            "cost": "很低"
        }
    ]
    
    for model_info in models:
        print(f"🔸 {model_info['provider']}")
        print(f"   模型: {', '.join(model_info['models'])}")
        print(f"   环境变量: {model_info['env']}")
        print(f"   特点: {model_info['features']}")
        print(f"   成本: {model_info['cost']}")
        print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--models":
        show_multimodal_models()
    else:
        test_multimodal_enhancement()