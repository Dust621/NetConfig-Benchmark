#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为IP路由配置示例分类脚本
根据文件名序号将JSON文件分类到对应的目录中，并清理JSON文件内容
"""

import os
import json
import shutil
from pathlib import Path

def get_category_mapping():
    """定义分类映射关系"""
    return {
        "1.2": "IP路由基础配置",
        "1.3": "IPv4静态路由配置", 
        "1.4": "IPv6静态路由配置",
        "1.5": "OSPF配置",
        "1.6": "OSPFv3配置", 
        "1.7": "RIP配置",
        "1.8": "RIPng配置",
        "1.9": "IS-IS配置",
        "1.10": "BGP配置",
        "1.11": "BGP4+配置", 
        "1.12": "路由策略配置"
    }

def extract_sequence_number(filename):
    """从文件名中提取序号"""
    if not filename.endswith('.json'):
        return None
    
    # 提取前面的数字序号部分，如 "1.10.62.1" 
    parts = filename.split(' ')[0].split('.')
    if len(parts) >= 2:
        return f"{parts[0]}.{parts[1]}"
    return None

def clean_json_content(json_data):
    """清理JSON内容：删除topology_original字段，去除related_images中的空格"""
    # 删除topology_original字段
    if 'topology_original' in json_data:
        del json_data['topology_original']
    
    # 清理related_images数组中的空格
    if 'related_images' in json_data and isinstance(json_data['related_images'], list):
        cleaned_images = []
        for image in json_data['related_images']:
            if isinstance(image, str):
                cleaned_images.append(image.strip())
            else:
                cleaned_images.append(image)
        json_data['related_images'] = cleaned_images
    
    return json_data

def classify_files(source_dir, output_base_dir):
    """分类文件到对应目录"""
    source_path = Path(source_dir)
    output_path = Path(output_base_dir)
    
    # 确保源目录存在
    if not source_path.exists():
        print(f"源目录不存在: {source_dir}")
        return
    
    category_mapping = get_category_mapping()
    
    # 创建输出基目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    stats = {
        'total_files': 0,
        'processed_files': 0,
        'categories': {}
    }
    
    # 遍历源目录中的所有JSON文件
    for json_file in source_path.glob('*.json'):
        stats['total_files'] += 1
        filename = json_file.name
        
        # 提取序号
        seq_num = extract_sequence_number(filename)
        if not seq_num:
            print(f"无法提取序号: {filename}")
            continue
        
        # 查找对应的分类
        category = category_mapping.get(seq_num)
        if not category:
            print(f"未找到分类 ({seq_num}): {filename}")
            continue
        
        # 创建目标目录
        target_dir = output_path / category
        target_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            # 读取JSON文件
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # 清理JSON内容
            cleaned_data = clean_json_content(json_data)
            
            # 写入目标文件
            target_file = target_dir / filename
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            
            stats['processed_files'] += 1
            if category not in stats['categories']:
                stats['categories'][category] = 0
            stats['categories'][category] += 1
            
            print(f"已处理: {filename} -> {category}/")
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
    
    # 打印统计信息
    print("\n=== 分类统计 ===")
    print(f"总文件数: {stats['total_files']}")
    print(f"已处理: {stats['processed_files']}")
    print("\n各分类文件数:")
    for category, count in sorted(stats['categories'].items()):
        print(f"  {category}: {count} 个文件")

def main():
    """主函数"""
    # 设置路径
    source_dir = "datasets/Huawei/IP路由配置示例"
    output_dir = "datasets/Huawei/IP路由配置示例_分类"
    
    print("华为IP路由配置示例分类工具")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("=" * 50)
    
    # 执行分类
    classify_files(source_dir, output_dir)
    
    print("\n分类完成!")

if __name__ == "__main__":
    main()