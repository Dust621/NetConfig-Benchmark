#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
华为IP路由配置示例IPv4/IPv6分类脚本
通过检查JSON文件内容中是否包含IPv6地址来进行分类
"""

import os
import json
import re
import shutil
from pathlib import Path

def get_ipv6_patterns():
    """定义IPv6地址检测的正则表达式模式"""
    patterns = [
        # 标准IPv6地址格式: 8组4位十六进制数，用冒号分隔
        r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b',
        
        # 压缩格式IPv6地址: 包含::的地址
        r'\b(?:[0-9a-fA-F]{1,4}:)*::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4})*\b',
        r'\b::[0-9a-fA-F]{1,4}(?::[0-9a-fA-F]{1,4})*\b',
        r'\b(?:[0-9a-fA-F]{1,4}:)*::\b',
        
        # IPv6回环地址
        r'\b::1\b',
        
        # 链路本地地址 (fe80::/10)
        r'\bfe80::[0-9a-fA-F:]*\b',
        
        # IPv6地址后跟网络前缀
        r'\b(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}/\d{1,3}\b',
        r'\b(?:[0-9a-fA-F]{1,4}:)*::[0-9a-fA-F:]*(?:/\d{1,3})?\b',
        
        # 混合IPv4-IPv6格式
        r'\b(?:[0-9a-fA-F]{1,4}:){6}(?:\d{1,3}\.){3}\d{1,3}\b',
        r'\b::ffff:(?:\d{1,3}\.){3}\d{1,3}\b',
        
        # IPv6 zone ID格式 (带%符号)
        r'\b(?:[0-9a-fA-F]{1,4}:)*::[0-9a-fA-F:]*%\w+\b',
        
        # 其他常见IPv6格式
        r'\b2001:db8:[0-9a-fA-F:]*\b',  # 文档用途IPv6地址
    ]
    
    # 编译所有正则表达式模式
    compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    return compiled_patterns

def contains_ipv6_address(text):
    """检查文本中是否包含IPv6地址"""
    if not text:
        return False
    
    # 获取IPv6检测模式
    ipv6_patterns = get_ipv6_patterns()
    
    # 逐个检查模式
    for pattern in ipv6_patterns:
        if pattern.search(text):
            return True
    
    # 额外检查一些IPv6相关的关键词
    ipv6_keywords = [
        'ipv6', 'IPv6', 'IPV6',
        'ospfv3', 'OSPFv3', 'OSPFV3',
        'ripng', 'RIPng', 'RIPNG',
        'bgp4+', 'BGP4+', 'BGP4\+',
        'ndp', 'NDP'
    ]
    
    for keyword in ipv6_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
            return True
    
    return False

def analyze_json_file(file_path):
    """分析JSON文件，检查是否包含IPv6相关内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 将整个JSON对象转换为字符串进行检查
        json_text = json.dumps(data, ensure_ascii=False)
        
        # 检查是否包含IPv6地址或相关内容
        has_ipv6 = contains_ipv6_address(json_text)
        
        # 额外检查文件名是否包含IPv6相关标识
        filename = os.path.basename(file_path)
        if contains_ipv6_address(filename):
            has_ipv6 = True
        
        return has_ipv6, data
        
    except Exception as e:
        print(f"分析文件 {file_path} 时出错: {e}")
        return False, None

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

def classify_files(source_dir, output_base_dir):
    """对JSON文件按IPv4/IPv6进行分类"""
    source_path = Path(source_dir)
    output_path = Path(output_base_dir)
    
    # 确保源目录存在
    if not source_path.exists():
        print(f"源目录不存在: {source_dir}")
        return
    
    # 创建输出目录
    ipv4_dir = output_path / "IPv4配置"
    ipv6_dir = output_path / "IPv6配置"
    mixed_dir = output_path / "混合配置"  # 既包含IPv4又包含IPv6的文件
    
    ipv4_dir.mkdir(parents=True, exist_ok=True)
    ipv6_dir.mkdir(parents=True, exist_ok=True)
    mixed_dir.mkdir(parents=True, exist_ok=True)
    
    # 统计信息
    stats = {
        'total_files': 0,
        'ipv4_files': 0,
        'ipv6_files': 0,
        'mixed_files': 0,
        'error_files': 0
    }
    
    # 存储检测结果详情
    detection_details = {
        'ipv4_only': [],
        'ipv6_only': [],
        'mixed': [],
        'errors': []
    }
    
    # 遍历源目录中的所有JSON文件
    for json_file in source_path.glob('*.json'):
        stats['total_files'] += 1
        filename = json_file.name
        
        print(f"分析文件: {filename}")
        
        # 分析文件内容
        has_ipv6, json_data = analyze_json_file(json_file)
        
        if json_data is None:
            stats['error_files'] += 1
            detection_details['errors'].append(filename)
            continue
        
        # 清理JSON内容
        cleaned_data = clean_json_content(json_data)
        
        # 简化文件名（去掉复杂序号）
        new_filename = filename
        # pattern = r'^(\d+\.\d+\.\d+\.(\d+))\s+(.+)\.json$'
        # match = re.match(pattern, filename)
        # if match:
        #     last_number = match.group(2)
        #     description = match.group(3)
        #     new_filename = f"{last_number} {description}.json"
        
        # 根据检测结果确定目标目录
        if has_ipv6:
            target_dir = ipv6_dir
            stats['ipv6_files'] += 1
            detection_details['ipv6_only'].append(new_filename)
            print(f"  → IPv6配置: {new_filename}")
        else:
            target_dir = ipv4_dir
            stats['ipv4_files'] += 1
            detection_details['ipv4_only'].append(new_filename)
            print(f"  → IPv4配置: {new_filename}")
        
        # 检查目标文件是否已存在，避免覆盖
        target_file = target_dir / new_filename
        counter = 1
        original_filename = new_filename
        while target_file.exists():
            name_parts = original_filename.rsplit('.', 1)
            new_filename = f"{name_parts[0]}_{counter}.{name_parts[1]}"
            target_file = target_dir / new_filename
            counter += 1
        
        # 写入分类后的文件
        try:
            with open(target_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  错误: 保存文件失败 - {e}")
            stats['error_files'] += 1
            detection_details['errors'].append(filename)
    
    # 打印统计结果
    print("\n" + "="*60)
    print("IPv4/IPv6 分类统计结果")
    print("="*60)
    print(f"总文件数: {stats['total_files']}")
    print(f"IPv4配置: {stats['ipv4_files']} 个文件")
    print(f"IPv6配置: {stats['ipv6_files']} 个文件")
    print(f"处理错误: {stats['error_files']} 个文件")
    
    print(f"\nIPv4配置文件列表:")
    for filename in sorted(detection_details['ipv4_only']):
        print(f"  - {filename}")
    
    print(f"\nIPv6配置文件列表:")
    for filename in sorted(detection_details['ipv6_only']):
        print(f"  - {filename}")
    
    if detection_details['errors']:
        print(f"\n处理错误的文件:")
        for filename in detection_details['errors']:
            print(f"  - {filename}")

def main():
    """主函数"""
    source_dir = "datasets/Huawei/IP路由配置示例"
    output_dir = "datasets/Huawei/IP路由配置示例_IPv4_IPv6分类"
    
    print("华为IP路由配置示例 IPv4/IPv6 分类工具")
    print(f"源目录: {source_dir}")
    print(f"输出目录: {output_dir}")
    print("="*60)
    
    # 执行分类
    classify_files(source_dir, output_dir)
    
    print(f"\n分类完成! 结果保存在: {output_dir}")

if __name__ == "__main__":
    main()