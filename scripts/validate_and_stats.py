#!/usr/bin/env python3
"""
华为NE40E数据验证和统计脚本
验证生成的json文件质量并生成详细统计信息
"""

import json
import os
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Any

class DataValidator:
    def __init__(self, data_dir: str = "datasets/Huawei/NE40E_examples"):
        self.data_dir = Path(data_dir)
        self.stats = {
            "total_files": 0,
            "valid_files": 0,
            "invalid_files": [],
            "categories": {},
            "device_types": Counter(),
            "config_lengths": [],
            "step_counts": [],
            "topology_lengths": [],
            "requirement_lengths": [],
            "image_counts": []
        }
    
    def validate_json_structure(self, data: Dict[str, Any], filename: str) -> bool:
        """验证JSON结构是否符合要求"""
        required_fields = ["topology", "requirement", "steps", "configs"]
        
        for field in required_fields:
            if field not in data:
                print(f"  ❌ 缺少必需字段: {field}")
                return False
        
        # 验证字段类型
        if not isinstance(data["topology"], str):
            print(f"  ❌ topology字段应为字符串")
            return False
        
        if not isinstance(data["requirement"], str):
            print(f"  ❌ requirement字段应为字符串")
            return False
        
        if not isinstance(data["steps"], list):
            print(f"  ❌ steps字段应为列表")
            return False
        
        if not isinstance(data["configs"], dict):
            print(f"  ❌ configs字段应为字典")
            return False
        
        # 验证内容质量
        if len(data["topology"].strip()) < 10:
            print(f"  ⚠️  topology内容过短")
        
        if len(data["requirement"].strip()) < 10:
            print(f"  ⚠️  requirement内容过短")
        
        if len(data["steps"]) == 0:
            print(f"  ⚠️  没有配置步骤")
        
        if len(data["configs"]) == 0:
            print(f"  ⚠️  没有设备配置")
        
        return True
    
    def collect_statistics(self, data: Dict[str, Any], category: str):
        """收集统计信息"""
        # 设备类型统计
        for device_name in data["configs"].keys():
            self.stats["device_types"][device_name] += 1
        
        # 配置长度统计
        total_config_length = sum(len(config) for config in data["configs"].values())
        self.stats["config_lengths"].append(total_config_length)
        
        # 步骤数量统计
        self.stats["step_counts"].append(len(data["steps"]))
        
        # 文本长度统计
        self.stats["topology_lengths"].append(len(data["topology"]))
        self.stats["requirement_lengths"].append(len(data["requirement"]))
        
        # 图片数量统计
        image_count = len(data.get("related_images", []))
        self.stats["image_counts"].append(image_count)
        
        # 类别统计
        if category not in self.stats["categories"]:
            self.stats["categories"][category] = {
                "file_count": 0,
                "device_count": 0,
                "total_config_length": 0,
                "avg_steps": 0,
                "avg_topology_length": 0,
                "avg_requirement_length": 0
            }
        
        cat_stats = self.stats["categories"][category]
        cat_stats["file_count"] += 1
        cat_stats["device_count"] += len(data["configs"])
        cat_stats["total_config_length"] += total_config_length
    
    def validate_all_files(self):
        """验证所有文件"""
        print("🔍 开始验证数据文件...")
        
        for category_dir in self.data_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('_'):
                continue
            
            category_name = category_dir.name
            print(f"\n📁 验证类别: {category_name}")
            
            for json_file in category_dir.glob("*.json"):
                if json_file.name.startswith('_'):
                    continue
                
                self.stats["total_files"] += 1
                print(f"  📄 验证文件: {json_file.name}")
                
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if self.validate_json_structure(data, json_file.name):
                        self.stats["valid_files"] += 1
                        self.collect_statistics(data, category_name)
                        print(f"    ✅ 验证通过")
                    else:
                        self.stats["invalid_files"].append(str(json_file))
                        print(f"    ❌ 验证失败")
                
                except json.JSONDecodeError as e:
                    self.stats["invalid_files"].append(str(json_file))
                    print(f"    ❌ JSON解析错误: {e}")
                except Exception as e:
                    self.stats["invalid_files"].append(str(json_file))
                    print(f"    ❌ 其他错误: {e}")
    
    def calculate_summary_stats(self):
        """计算汇总统计"""
        if self.stats["config_lengths"]:
            self.stats["avg_config_length"] = sum(self.stats["config_lengths"]) / len(self.stats["config_lengths"])
            self.stats["max_config_length"] = max(self.stats["config_lengths"])
            self.stats["min_config_length"] = min(self.stats["config_lengths"])
        
        if self.stats["step_counts"]:
            self.stats["avg_steps"] = sum(self.stats["step_counts"]) / len(self.stats["step_counts"])
            self.stats["max_steps"] = max(self.stats["step_counts"])
            self.stats["min_steps"] = min(self.stats["step_counts"])
        
        if self.stats["topology_lengths"]:
            self.stats["avg_topology_length"] = sum(self.stats["topology_lengths"]) / len(self.stats["topology_lengths"])
        
        if self.stats["requirement_lengths"]:
            self.stats["avg_requirement_length"] = sum(self.stats["requirement_lengths"]) / len(self.stats["requirement_lengths"])
        
        if self.stats["image_counts"]:
            self.stats["avg_images"] = sum(self.stats["image_counts"]) / len(self.stats["image_counts"])
            self.stats["total_images"] = sum(self.stats["image_counts"])
        
        # 计算各类别平均值
        for category, cat_stats in self.stats["categories"].items():
            if cat_stats["file_count"] > 0:
                cat_stats["avg_steps"] = sum(self.stats["step_counts"]) / len(self.stats["step_counts"])
                cat_stats["avg_topology_length"] = sum(self.stats["topology_lengths"]) / len(self.stats["topology_lengths"])
                cat_stats["avg_requirement_length"] = sum(self.stats["requirement_lengths"]) / len(self.stats["requirement_lengths"])
    
    def print_statistics(self):
        """打印统计信息"""
        print("\n" + "="*60)
        print("📊 数据统计报告")
        print("="*60)
        
        print(f"\n📈 总体统计:")
        print(f"  • 总文件数: {self.stats['total_files']}")
        print(f"  • 有效文件数: {self.stats['valid_files']}")
        print(f"  • 无效文件数: {len(self.stats['invalid_files'])}")
        print(f"  • 验证通过率: {self.stats['valid_files']/self.stats['total_files']*100:.1f}%")
        
        if hasattr(self.stats, 'avg_config_length'):
            print(f"\n📝 配置统计:")
            print(f"  • 平均配置长度: {self.stats['avg_config_length']:.0f} 字符")
            print(f"  • 最大配置长度: {self.stats['max_config_length']} 字符")
            print(f"  • 最小配置长度: {self.stats['min_config_length']} 字符")
        
        if hasattr(self.stats, 'avg_steps'):
            print(f"\n📋 步骤统计:")
            print(f"  • 平均配置步骤数: {self.stats['avg_steps']:.1f}")
            print(f"  • 最多配置步骤数: {self.stats['max_steps']}")
            print(f"  • 最少配置步骤数: {self.stats['min_steps']}")
        
        if hasattr(self.stats, 'avg_topology_length'):
            print(f"\n🌐 内容统计:")
            print(f"  • 平均拓扑描述长度: {self.stats['avg_topology_length']:.0f} 字符")
            print(f"  • 平均需求描述长度: {self.stats['avg_requirement_length']:.0f} 字符")
        
        if hasattr(self.stats, 'total_images'):
            print(f"\n🖼️  图片统计:")
            print(f"  • 总图片数: {self.stats['total_images']}")
            print(f"  • 平均每个实验图片数: {self.stats['avg_images']:.1f}")
        
        print(f"\n📂 分类统计:")
        for category, cat_stats in self.stats["categories"].items():
            print(f"  • {category}: {cat_stats['file_count']} 个文件, {cat_stats['device_count']} 个设备配置")
        
        print(f"\n🖥️  设备类型统计 (前10名):")
        for device, count in self.stats["device_types"].most_common(10):
            print(f"  • {device}: {count} 次")
        
        if self.stats["invalid_files"]:
            print(f"\n❌ 无效文件列表:")
            for invalid_file in self.stats["invalid_files"]:
                print(f"  • {invalid_file}")
    
    def save_statistics(self):
        """保存统计信息到文件"""
        stats_file = self.data_dir / "_validation_report.json"
        
        # 转换Counter对象为普通字典
        stats_copy = dict(self.stats)
        stats_copy["device_types"] = dict(self.stats["device_types"])
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats_copy, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 统计报告已保存到: {stats_file}")
    
    def run_validation(self):
        """运行完整验证流程"""
        self.validate_all_files()
        self.calculate_summary_stats()
        self.print_statistics()
        self.save_statistics()
        
        print(f"\n🎉 验证完成!")
        print(f"  • 共处理 {self.stats['total_files']} 个文件")
        print(f"  • 验证通过率: {self.stats['valid_files']/self.stats['total_files']*100:.1f}%")

def main():
    """主函数"""
    validator = DataValidator()
    validator.run_validation()

if __name__ == "__main__":
    main()