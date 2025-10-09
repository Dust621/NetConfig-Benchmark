#!/usr/bin/env python3
"""
华为NE40E数据分类整理脚本
将integrate_huawei_data.py生成的json文件按协议类型分类整理
模仿datasets/Huawei/HCIP_datacom的目录结构
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List

class HuaweiDataOrganizer:
    def __init__(self, source_dir: str = "datasets/Huawei/integrated_data", output_dir: str = "datasets/Huawei/NE40E_examples"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        
        # 协议分类映射
        self.protocol_categories = {
            "OSPF": {
                "keywords": ["ospf", "1.5.30"],
                "folder": "1_OSPF实验"
            },
            "OSPFv3": {
                "keywords": ["ospfv3", "1.6.28"],
                "folder": "2_OSPFv3实验"
            },
            "RIP": {
                "keywords": ["rip", "1.7.14"],
                "folder": "3_RIP实验"
            },
            "RIPng": {
                "keywords": ["ripng", "1.8.11"],
                "folder": "4_RIPng实验"
            },
            "BGP": {
                "keywords": ["bgp", "1.10.62"],
                "folder": "5_BGP实验"
            },
            "IS-IS": {
                "keywords": ["isis", "1.9.45"],
                "folder": "6_IS-IS实验"
            },
            "静态路由": {
                "keywords": ["静态路由", "1.3.8", "1.4.7"],
                "folder": "7_静态路由实验"
            },
            "路由策略": {
                "keywords": ["路由策略", "1.12.14"],
                "folder": "8_路由策略实验"
            },
            "路由监控": {
                "keywords": ["路由监控", "1.14.4"],
                "folder": "9_路由监控实验"
            },
            "FRR": {
                "keywords": ["frr", "1.2.22"],
                "folder": "10_FRR实验"
            },
            "其他": {
                "keywords": ["公共语句", "条件语句", "1.13.9"],
                "folder": "11_其他实验"
            }
        }
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True, parents=True)
    
    def classify_file(self, filename: str) -> str:
        """根据文件名分类"""
        filename_lower = filename.lower()
        
        for category, info in self.protocol_categories.items():
            for keyword in info["keywords"]:
                if keyword.lower() in filename_lower:
                    return category
        
        return "其他"
    
    def generate_summary_file(self, category_dir: Path, files: List[Path]):
        """为每个类别生成总结文件"""
        summary = {
            "category": category_dir.name,
            "total_files": len(files),
            "files": []
        }
        
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                file_info = {
                    "filename": file_path.name,
                    "title": file_path.stem,
                    "topology_summary": data.get("topology", "")[:100] + "..." if len(data.get("topology", "")) > 100 else data.get("topology", ""),
                    "device_count": len(data.get("configs", {}))
                }
                summary["files"].append(file_info)
                
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
        
        # 保存总结文件
        summary_path = category_dir / "_category_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"  -> 生成类别总结: {summary_path}")
    
    def create_readme_for_category(self, category_dir: Path, category: str, files: List[Path]):
        """为每个类别创建README文件"""
        readme_content = f"""# {category_dir.name}

## 概述
本目录包含华为NE40E设备手册中关于{category}的配置示例。

## 实验列表
共包含 {len(files)} 个配置示例：

"""
        
        for i, file_path in enumerate(files, 1):
            readme_content += f"{i}. {file_path.stem}\n"
        
        readme_content += f"""
## 文件说明
- 每个.json文件包含完整的实验配置，包括：
  - topology: 网络拓扑描述
  - requirement: 组网需求
  - steps: 配置步骤
  - configs: 各设备配置
  - related_images: 相关拓扑图片（如有）

## 使用方法
可以直接读取json文件获取完整的实验配置信息，用于网络配置学习或测试。
"""
        
        readme_path = category_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"  -> 生成README: {readme_path}")
    
    def organize_files(self):
        """整理文件到分类目录"""
        if not self.source_dir.exists():
            print(f"源目录不存在: {self.source_dir}")
            return
        
        # 统计各类别的文件
        category_files = {}
        
        for json_file in self.source_dir.glob("*.json"):
            category = self.classify_file(json_file.name)
            
            if category not in category_files:
                category_files[category] = []
            category_files[category].append(json_file)
        
        # 为每个类别创建目录并复制文件
        total_files = 0
        for category, files in category_files.items():
            if not files:
                continue
            
            folder_name = self.protocol_categories[category]["folder"]
            category_dir = self.output_dir / folder_name
            category_dir.mkdir(exist_ok=True, parents=True)
            
            print(f"\n处理 {category} 类别 ({len(files)} 个文件):")
            
            copied_files = []
            for file_path in files:
                dest_path = category_dir / file_path.name
                shutil.copy2(file_path, dest_path)
                copied_files.append(dest_path)
                print(f"  -> 复制: {file_path.name}")
            
            # 生成类别总结和README
            self.generate_summary_file(category_dir, copied_files)
            self.create_readme_for_category(category_dir, category, copied_files)
            
            total_files += len(files)
        
        # 生成总体统计
        self.generate_overall_summary(category_files, total_files)
        
        print(f"\n整理完成! 共处理了 {total_files} 个文件")
        print(f"输出目录: {self.output_dir}")
    
    def generate_overall_summary(self, category_files: Dict, total_files: int):
        """生成总体统计信息"""
        overall_summary = {
            "title": "华为NE40E设备配置示例集",
            "total_files": total_files,
            "categories": {}
        }
        
        for category, files in category_files.items():
            if files:
                folder_name = self.protocol_categories[category]["folder"]
                overall_summary["categories"][folder_name] = {
                    "category": category,
                    "file_count": len(files),
                    "description": f"{category}相关配置示例"
                }
        
        # 保存总体统计
        summary_path = self.output_dir / "_overall_summary.json"
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(overall_summary, f, ensure_ascii=False, indent=2)
        
        # 创建主README
        readme_content = f"""# 华为NE40E设备配置示例集

## 概述
本数据集包含从华为NE40E设备手册中提取和整理的网络配置示例，共 {total_files} 个实验配置。

## 目录结构

"""
        
        for folder_name, info in overall_summary["categories"].items():
            readme_content += f"- **{folder_name}** ({info['file_count']} 个文件): {info['description']}\n"
        
        readme_content += f"""
## 数据格式
每个实验配置为JSON格式，包含以下字段：
- `topology`: 网络拓扑描述
- `requirement`: 组网需求和实验目标
- `steps`: 配置步骤列表
- `configs`: 各设备的完整配置
- `related_images`: 相关拓扑图片路径（如有）

## 使用示例
```python
import json

# 读取配置文件
with open('1_OSPF实验/1.5.30.1 配置OSPF 基本功能示例.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print("拓扑描述:", config['topology'])
print("配置步骤:", config['steps'])
print("设备配置:", config['configs'])
```

## 数据来源
数据提取自华为NE40E系列路由器配置指南，包含真实的网络配置场景和最佳实践。

## 更新时间
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        readme_path = self.output_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n生成总体统计: {summary_path}")
        print(f"生成主README: {readme_path}")

def main():
    """主函数"""
    organizer = HuaweiDataOrganizer()
    organizer.organize_files()

if __name__ == "__main__":
    main()