#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为IP路由配置示例设备数量分类脚本
统计每个JSON文件中configs字段下的设备数量，并根据设备数量进行分类
"""

import os
import json
import shutil
from pathlib import Path
from collections import defaultdict

def count_devices_in_configs(json_data):
    """统计JSON文件中configs字段的设备数量"""
    if not json_data or 'configs' not in json_data:
        return 0
    
    configs = json_data['configs']
    if not isinstance(configs, dict):
        return 0
    
    # 统计configs字典中的设备数量
    device_count = len(configs)
    return device_count

def get_device_names(json_data):
    """获取JSON文件中configs字段的设备名称列表"""
    if not json_data or 'configs' not in json_data:
        return []
    
    configs = json_data['configs']
    if not isinstance(configs, dict):
        return []
    
    return list(configs.keys())

def clean_json_content(json_data):
    """清理JSON内容：删除topology_original字段，去除related_images中的空格"""
    if not json_data:
        return json_data
    
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

def analyze_source_directory(source_dir):
    """分析源目录，统计所有JSON文件的设备数量分布"""
    source_path = Path(source_dir)
    device_count_stats = defaultdict(list)
    total_files = 0
    error_files = []
    
    print("正在分析源目录中的所有JSON文件...")
    print("="*60)
    
    # 递归遍历所有子目录中的JSON文件
    for json_file in source_path.rglob('*.json'):
        total_files += 1
        relative_path = json_file.relative_to(source_path)
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            device_count = count_devices_in_configs(json_data)
            device_names = get_device_names(json_data)
            
            # 存储文件信息
            file_info = {
                'file_path': json_file,
                'relative_path': relative_path,
                'filename': json_file.name,
                'device_count': device_count,
                'device_names': device_names,
                'json_data': json_data
            }
            
            device_count_stats[device_count].append(file_info)
            
            print(f"✓ {relative_path}: {device_count} 个设备 {device_names}")
            
        except Exception as e:
            error_files.append(str(relative_path))
            print(f"✗ {relative_path}: 分析失败 - {e}")
    
    return device_count_stats, total_files, error_files

def classify_by_device_count(source_dir, output_base_dir):
    """根据设备数量对JSON文件进行分类"""
    output_path = Path(output_base_dir)
    
    # 分析源目录
    device_count_stats, total_files, error_files = analyze_source_directory(source_dir)
    
    if not device_count_stats:
        print("未找到任何有效的JSON文件！")
        return
    
    # 创建输出基目录
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    processed_files = 0
    classification_stats = {}
    
    print(f"\n{'='*60}")
    print("开始按设备数量分类...")
    print("="*60)
    
    # 按设备数量分类
    for device_count, file_list in sorted(device_count_stats.items()):
        if device_count == 0:
            category_name = "0_无设备配置"
        elif device_count == 1:
            category_name = "1_单设备配置"
        elif device_count == 2:
            category_name = "2_双设备配置"
        elif device_count == 3:
            category_name = "3_三设备配置"
        elif device_count == 4:
            category_name = "4_四设备配置"
        else:
            category_name = f"{device_count}_多设备配置"
        
        # 创建分类目录
        category_dir = output_path / category_name
        category_dir.mkdir(parents=True, exist_ok=True)
        
        classification_stats[category_name] = len(file_list)
        
        print(f"\n处理 {category_name} ({len(file_list)} 个文件):")
        
        for file_info in file_list:
            try:
                # 清理JSON内容
                cleaned_data = clean_json_content(file_info['json_data'])
                
                # 简化文件名（去除复杂序号前缀）
                filename = file_info['filename']
                new_filename = filename
                
                import re
                pattern = r'^(\d+\.\d+\.\d+\.(\d+))\s+(.+)\.json$'
                match = re.match(pattern, filename)
                if match:
                    last_number = match.group(2)
                    description = match.group(3)
                    new_filename = f"{last_number} {description}.json"
                
                # 检查目标文件是否已存在，避免覆盖
                target_file = category_dir / new_filename
                counter = 1
                original_filename = new_filename
                while target_file.exists():
                    name_parts = original_filename.rsplit('.', 1)
                    new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
                    target_file = category_dir / new_filename
                    counter += 1
                
                # 写入分类后的文件
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
                
                processed_files += 1
                device_names_str = ', '.join(file_info['device_names'])
                print(f"  ✓ {filename} → {new_filename} (设备: {device_names_str})")
                
            except Exception as e:
                print(f"  ✗ {filename}: 处理失败 - {e}")
    
    # 打印最终统计结果
    print(f"\n{'='*60}")
    print("设备数量分类统计结果")
    print("="*60)
    print(f"总文件数: {total_files}")
    print(f"处理成功: {processed_files}")
    print(f"处理失败: {len(error_files)}")
    
    print(f"\n各分类统计:")
    for category, count in sorted(classification_stats.items(), key=lambda x: int(x[0].split('_')[0])):
        print(f"  {category}: {count} 个文件")
    
    if error_files:
        print(f"\n处理失败的文件:")
        for error_file in error_files:
            print(f"  - {error_file}")
    
    # 分析设备数量分布
    print(f"\n设备数量分布分析:")
    for device_count, file_list in sorted(device_count_stats.items()):
        if device_count > 0:
            print(f"  {device_count}个设备: {len(file_list)} 个配置示例")
            # 显示一些设备名称示例
            all_device_names = set()
            for file_info in file_list[:5]:  # 只显示前5个文件的设备名称
                all_device_names.update(file_info['device_names'])
            if all_device_names:
                sample_devices = ', '.join(sorted(list(all_device_names))[:10])
                print(f"    设备示例: {sample_devices}")

def main():
    """主函数"""
    source_dir = "datasets/Huawei/IP路由配置示例_IPv4_IPv6分类"
    output_dir = "datasets/Huawei/IP路由配置示例_设备数量分类"
    
    print("华为IP路由配置示例 设备数量分类工具")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("="*60)
    
    # 执行分类
    classify_by_device_count(source_dir, output_dir)
    
    print(f"\n分类完成! 结果保存在: {output_dir}")

if __name__ == "__main__":
    main()