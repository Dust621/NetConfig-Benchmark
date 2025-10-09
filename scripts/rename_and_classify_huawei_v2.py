#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为IP路由配置示例重命名和分类脚本 v2
删除文件名前的复杂序号，只保留最后一位数字作为序号，并根据原始分类重新分类
"""

import os
import json
import re
from pathlib import Path

def get_category_by_original_prefix(filename):
    """根据原始文件名前缀确定分类"""
    # 提取原始前缀（前两个数字段）
    pattern = r'^(\d+\.\d+)'
    match = re.match(pattern, filename)
    if not match:
        return None
    
    prefix = match.group(1)
    
    # 根据原始分类规则映射
    category_mapping = {
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
    
    return category_mapping.get(prefix)

def extract_last_number_and_create_new_name(filename):
    """从文件名中提取最后一位数字并生成新的文件名"""
    if not filename.endswith('.json'):
        return None, None
    
    # 使用正则表达式匹配文件名格式：数字.数字.数字.数字 空格 中文描述.json
    # 例如: "1.10.62.1 配置BGP 的基本功能示例.json"
    pattern = r'^(\d+\.\d+\.\d+\.(\d+))\s+(.+)\.json$'
    match = re.match(pattern, filename)
    
    if match:
        full_number = match.group(1)  # "1.10.62.1"
        last_number = int(match.group(2))  # "1" 
        description = match.group(3)  # "配置BGP 的基本功能示例"
        
        # 生成新的文件名：只保留最后一位数字
        new_filename = f"{last_number} {description}.json"
        return last_number, new_filename
    
    return None, None

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

def process_files(source_dir, output_base_dir):
    """处理文件：重命名并分类到对应目录"""
    source_path = Path(source_dir)
    output_path = Path(output_base_dir)
    
    # 确保源目录存在
    if not source_path.exists():
        print(f"源目录不存在: {source_dir}")
        return
    
    # 创建输出基目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    stats = {
        'total_files': 0,
        'processed_files': 0,
        'categories': {},
        'sequence_stats': {}
    }
    
    # 遍历源目录中的所有JSON文件
    for json_file in source_path.glob('*.json'):
        stats['total_files'] += 1
        filename = json_file.name
        
        # 根据原始前缀确定分类
        category = get_category_by_original_prefix(filename)
        if not category:
            print(f"无法确定分类: {filename}")
            continue
        
        # 提取最后一位数字并生成新文件名
        last_number, new_filename = extract_last_number_and_create_new_name(filename)
        if last_number is None or new_filename is None:
            print(f"无法处理文件名: {filename}")
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
            
            # 检查目标文件是否已存在，如果存在则添加后缀
            target_file = target_dir / new_filename
            counter = 1
            original_name = new_filename
            while target_file.exists():
                name_parts = original_name.rsplit('.', 1)  # 分离文件名和扩展名
                new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                target_file = target_dir / new_filename
                counter += 1
            
            # 写入目标文件
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
            
            stats['processed_files'] += 1
            if category not in stats['categories']:
                stats['categories'][category] = 0
            stats['categories'][category] += 1
            
            if last_number not in stats['sequence_stats']:
                stats['sequence_stats'][last_number] = 0
            stats['sequence_stats'][last_number] += 1
            
            print(f"已处理: {filename} -> {new_filename} -> {category}/")
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
    
    # 打印统计信息
    print("\n=== 处理统计 ===")
    print(f"总文件数: {stats['total_files']}")
    print(f"已处理: {stats['processed_files']}")
    
    print("\n按序号统计:")
    for seq_num in sorted(stats['sequence_stats'].keys()):
        print(f"  序号{seq_num}: {stats['sequence_stats'][seq_num]} 个文件")
    
    print("\n各分类文件数:")
    for category, count in sorted(stats['categories'].items()):
        print(f"  {category}: {count} 个文件")

def main():
    """主函数"""
    # 设置路径
    source_dir = "datasets/Huawei/IP路由配置示例"
    output_dir = "datasets/Huawei/IP路由配置示例_重新分类"
    
    print("华为IP路由配置示例重命名和重新分类工具 v2")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)
    
    # 执行处理
    process_files(source_dir, output_dir)
    
    print("\n处理完成!")

if __name__ == "__main__":
    main()