#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为IP路由配置示例重命名和分类脚本
删除文件名前的复杂序号，只保留最后一位数字作为序号，并重新分类
"""

import os
import json
import re
from pathlib import Path

def get_category_mapping():
    """定义基于最后一位序号的分类映射关系"""
    return {
        1: "IP路由基础配置",        # 序号1的文件
        2: "IPv4静态路由配置",      # 序号2的文件 
        3: "IPv6静态路由配置",      # 序号3的文件
        4: "OSPF配置",             # 序号4的文件
        5: "OSPFv3配置",           # 序号5的文件
        6: "RIP配置",              # 序号6的文件
        7: "RIPng配置",            # 序号7的文件
        8: "IS-IS配置",            # 序号8的文件
        9: "BGP配置",              # 序号9的文件
        10: "BGP配置",             # 序号10的文件归到BGP配置
        11: "BGP配置",             # 序号11的文件归到BGP配置
        12: "BGP配置",             # 序号12的文件归到BGP配置
        13: "BGP配置",             # 序号13的文件归到BGP配置
        14: "BGP配置",             # 序号14的文件归到BGP配置
        15: "BGP配置",             # 序号15的文件归到BGP配置
        16: "BGP配置",             # 序号16的文件归到BGP配置
        17: "BGP配置",             # 序号17的文件归到BGP配置
        18: "BGP4+配置",           # 序号18的文件归到BGP4+配置
        19: "BGP配置",             # 序号19的文件归到BGP配置
        20: "BGP配置",             # 序号20的文件归到BGP配置
        21: "BGP配置",             # 序号21的文件归到BGP配置
        22: "BGP配置",             # 序号22的文件归到BGP配置
        23: "BGP配置",             # 序号23的文件归到BGP配置
        24: "BGP配置",             # 序号24的文件归到BGP配置
        25: "BGP配置",             # 序号25的文件归到BGP配置
        26: "BGP配置",             # 序号26的文件归到BGP配置
        27: "BGP配置",             # 序号27的文件归到BGP配置
        # 处理路由策略相关的序号
        1: "路由策略配置",          # 1.12.14.1 对应序号1 -> 路由策略配置
        2: "路由策略配置",          # 1.12.14.2 对应序号2 -> 路由策略配置  
        3: "路由策略配置"           # 1.12.14.3 对应序号3 -> 路由策略配置
    }

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
    
    category_mapping = get_category_mapping()
    
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
        
        # 提取最后一位数字并生成新文件名
        last_number, new_filename = extract_last_number_and_create_new_name(filename)
        if last_number is None or new_filename is None:
            print(f"无法处理文件名: {filename}")
            continue
        
        # 查找对应的分类
        category = category_mapping.get(last_number)
        if not category:
            print(f"未找到分类 (序号{last_number}): {filename}")
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
    
    print("华为IP路由配置示例重命名和重新分类工具")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)
    
    # 执行处理
    process_files(source_dir, output_dir)
    
    print("\n处理完成!")

if __name__ == "__main__":
    main()