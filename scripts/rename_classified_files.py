#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对已分类的华为IP路由配置示例文件进行重命名
删除文件名前的复杂序号（如1.10.62.1），只保留最后一位数字作为序号
"""

import os
import json
import re
from pathlib import Path

def extract_last_number_and_create_new_name(filename):
    """从文件名中提取最后一位数字并生成新的文件名"""
    if not filename.endswith('.json'):
        return None
    
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
        return new_filename
    
    return None

def process_classified_directory(base_dir):
    """处理已分类目录下的所有文件"""
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"目录不存在: {base_dir}")
        return
    
    stats = {
        'total_files': 0,
        'processed_files': 0,
        'categories': {}
    }
    
    # 遍历所有分类目录
    for category_dir in base_path.iterdir():
        if not category_dir.is_dir():
            continue
            
        category_name = category_dir.name
        print(f"\n处理分类: {category_name}")
        
        # 遍历该分类目录下的所有JSON文件
        json_files = list(category_dir.glob('*.json'))
        stats['categories'][category_name] = len(json_files)
        
        for json_file in json_files:
            stats['total_files'] += 1
            old_filename = json_file.name
            
            # 生成新的文件名
            new_filename = extract_last_number_and_create_new_name(old_filename)
            if not new_filename:
                print(f"  跳过: {old_filename} (无法处理)")
                continue
                
            # 检查新文件名是否与旧文件名相同
            if new_filename == old_filename:
                print(f"  跳过: {old_filename} (文件名无需更改)")
                continue
            
            # 确保新文件名不会冲突
            new_file_path = category_dir / new_filename
            counter = 1
            original_new_filename = new_filename
            while new_file_path.exists() and new_file_path != json_file:
                name_parts = original_new_filename.rsplit('.', 1)
                new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                new_file_path = category_dir / new_filename
                counter += 1
            
            try:
                # 重命名文件
                json_file.rename(new_file_path)
                stats['processed_files'] += 1
                print(f"  重命名: {old_filename} -> {new_filename}")
                
            except Exception as e:
                print(f"  错误: 重命名 {old_filename} 失败: {e}")
    
    # 打印统计信息
    print("\n=== 处理统计 ===")
    print(f"总文件数: {stats['total_files']}")
    print(f"已处理: {stats['processed_files']}")
    print("\n各分类文件数:")
    for category, count in sorted(stats['categories'].items()):
        print(f"  {category}: {count} 个文件")

def main():
    """主函数"""
    base_dir = "datasets/Huawei/IP路由配置示例_分类"
    
    print("华为IP路由配置示例文件重命名工具")
    print(f"处理目录: {base_dir}")
    print("=" * 50)
    
    # 执行处理
    process_classified_directory(base_dir)
    
    print("\n重命名完成!")

if __name__ == "__main__":
    main()