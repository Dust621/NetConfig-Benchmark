#!/usr/bin/env python3
"""
华为NE40E设备手册数据整合脚本
将datasets/Huawei/example和datasets/Huawei/extracted_images中的内容
整合成类似datasets/Huawei/HCIP_datacom目录下的json格式评测集
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional

class HuaweiDataIntegrator:
    def __init__(self, base_dir: str = "datasets/Huawei"):
        self.base_dir = Path(base_dir)
        self.example_dir = self.base_dir / "example"
        self.images_dir = self.base_dir / "extracted_images"
        self.output_dir = self.base_dir / "integrated_data"
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)
    
    def extract_topology_from_md(self, content: str) -> str:
        """从markdown内容中提取网络拓扑信息"""
        # 查找网络拓扑相关的章节，支持多种标题级别
        patterns = [
            r"#{1,4}\s*网络拓扑(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*拓扑结构(.*?)(?=#{1,4}|$)",
            r"网络拓扑：(.*?)(?=\n\n|\n#{1,4}|$)",
            r"拓扑结构：(.*?)(?=\n\n|\n#{1,4}|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                topology = match.group(1).strip()
                # 清理markdown格式
                topology = re.sub(r'\n+', ' ', topology)
                topology = re.sub(r'[*_-]+', '', topology)
                return topology
        
        # 如果没有找到专门的拓扑章节，从组网需求中提取
        patterns = [
            r"#{1,4}\s*组网需求(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*配置需求(.*?)(?=#{1,4}|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                requirement_text = match.group(1).strip()
                # 提取第一段作为拓扑描述
                lines = requirement_text.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('*'):
                        # 清理markdown格式
                        line = re.sub(r'[*_-]+', '', line)
                        return line
        
        return "网络拓扑信息未找到"
    
    def extract_requirement_from_md(self, content: str) -> str:
        """从markdown内容中提取组网需求"""
        patterns = [
            r"#{1,4}\s*组网需求(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*配置需求(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*网络需求(.*?)(?=#{1,4}|$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                requirement = match.group(1).strip()
                # 清理markdown格式但保留基本结构
                requirement = re.sub(r'\n\s*\n', '\n', requirement)
                requirement = re.sub(r'^\s*[-*+]\s*', '', requirement, flags=re.MULTILINE)
                return requirement
        
        return "组网需求信息未找到"
    
    def extract_steps_from_md(self, content: str) -> List[str]:
        """从markdown内容中提取配置思路"""
        steps = []
        
        # 首先尝试提取配置思路章节
        thought_patterns = [
            r"#{1,4}\s*配置思路(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*实现思路(.*?)(?=#{1,4}|$)",
            r"#{1,4}\s*设计思路(.*?)(?=#{1,4}|$)"
        ]
        
        for pattern in thought_patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                thought_content = match.group(1)
                # 提取编号列表（配置思路中的步骤）
                numbered_items = re.findall(r'\d+\.\s*(.*?)(?=\n\d+\.|\n#{1,4}|$)', thought_content, re.DOTALL)
                for item in numbered_items:
                    if isinstance(item, tuple):
                        item = next((s for s in item if s and s.strip()), "")
                    if isinstance(item, str):
                        item = re.sub(r'\n+', ' ', item.strip())
                        item = re.sub(r'\s+', ' ', item)  # 合并多余空格
                        if item and len(item) > 5:  # 过滤太短的内容
                            steps.append(item)
                break
        
        # 如果配置思路中没有编号列表，从操作步骤中提取简化版本
        if not steps:
            operation_patterns = [
                r"#{1,4}\s*操作步骤(.*?)(?=#{1,4}\s*配置文件|#{1,4}\s*验证配置|$)",
                r"#{1,4}\s*配置步骤(.*?)(?=#{1,4}\s*配置文件|#{1,4}\s*验证配置|$)"
            ]
            
            for pattern in operation_patterns:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    steps_content = match.group(1)
                    # 提取主要步骤标题
                    step_titles = re.findall(r"#{2,4}\s*步骤\s*\d+\s*([^\n]+)", steps_content, re.IGNORECASE)
                    for title in step_titles:
                        title = title.strip()
                        if title and len(title) > 5:
                            steps.append(title)
                    break
        
        return steps if steps else ["配置步骤信息未找到"]
    
    def extract_configs_from_md(self, content: str) -> Dict[str, str]:
        """从markdown内容中提取设备配置"""
        configs = {}
        
        # 查找配置文件章节，支持多种标题级别
        config_section_match = re.search(r"#{1,4}\s*配置文件(.*?)$", content, re.DOTALL | re.IGNORECASE)
        if not config_section_match:
            config_section_match = re.search(r"#{1,4}\s*设备配置(.*?)$", content, re.DOTALL | re.IGNORECASE)
        
        if config_section_match:
            config_content = config_section_match.group(1)
            
            # 提取每个设备的配置，支持多种设备命名模式
            device_patterns = [
                r"#{2,4}\s*(Device[A-Z])(?:的)?配置文件?[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,4}\s*配置\s*(Device[A-Z])[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,4}\s*(R\d+)(?:的)?配置文件?[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,4}\s*配置\s*(R\d+)[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,4}\s*(SW\d+)(?:的)?配置文件?[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,4}\s*(路由器[A-Z])(?:的)?配置文件?[^`]*```(?:bash)?\s*(.*?)```"
            ]
            
            for pattern in device_patterns:
                matches = re.findall(pattern, config_content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        device_name, config = match
                    else:
                        device_name, config = match, ""
                    config = config.strip()
                    if config:
                        # 修复配置中的注释格式问题
                        config = self.fix_config_comments(config)
                        configs[device_name] = config
        
        # 如果配置文件章节没有找到配置，从操作步骤中提取
        if not configs:
            # 在操作步骤中查找设备配置，支持多种模式
            device_config_patterns = [
                r"#{2,5}\s*配置\s*(Device[A-Z])[^`]*```(?:bash)?\s*(.*?)```",
                r"配置\s*(Device[A-Z])[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,5}\s*配置\s*(R\d+)[^`]*```(?:bash)?\s*(.*?)```",
                r"配置\s*(R\d+)[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,5}\s*配置\s*(SW\d+)[^`]*```(?:bash)?\s*(.*?)```",
                r"#{2,5}\s*(Device[A-Z])\s*上[^`]*```(?:bash)?\s*(.*?)```",
                r"在\s*(Device[A-Z])\s*上[^`]*```(?:bash)?\s*(.*?)```"
            ]
            
            for pattern in device_config_patterns:
                matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        device_name, config = match
                    else:
                        device_name, config = match, ""
                    config = config.strip()
                    if config:
                        # 修复配置中的注释格式问题
                        config = self.fix_config_comments(config)
                        configs[device_name] = config
        
        return configs
    
    def fix_config_comments(self, config: str) -> str:
        """修复配置中的注释格式问题"""
        # 修复 #command 格式为 #\ncommand
        # 匹配以#开头但后面紧跟命令的行（不是纯注释）
        lines = config.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 如果行以#开头，但后面紧跟的是命令关键字，则分离
            if re.match(r'^#(sysname|interface|router|bgp|ospf|rip|isis|mpls|ip|ipv6|vlan|return)\b', line):
                # 分离为 # 和命令
                command = line[1:]  # 去掉#
                fixed_lines.append('#')
                fixed_lines.append(command)
            else:
                fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def find_related_images(self, md_content: str, md_filename: str) -> List[str]:
        """根据MD文件内容中提到的图序号查找相关图片，如没有则查找相邻图片"""
        related_images = []
        
        # 从MD内容中提取图序号引用，如"图1-49"、"如图1-77所示"
        figure_patterns = [
            r"图(\d+-\d+)",
            r"图片(\d+-\d+)",
            r"Figure\s*(\d+-\d+)"
        ]
        
        figure_numbers = set()
        for pattern in figure_patterns:
            matches = re.findall(pattern, md_content, re.IGNORECASE)
            for match in matches:
                figure_numbers.add(match)
        
        # 在图片目录中查找对应的图片文件
        if self.images_dir.exists() and figure_numbers:
            for img_file in self.images_dir.glob("*.png"):
                img_name = img_file.name
                # 检查图片文件名是否包含提到的图序号
                for fig_num in figure_numbers:
                    if f"图{fig_num}" in img_name or f"图{fig_num.replace('-', '')}" in img_name:
                        related_images.append(str(img_file))
                        break
        
        # 如果没有找到明确的图序号引用，尝试通过内容关键词查找
        if not related_images:
            related_images = self.find_images_by_content_keywords(md_content, md_filename)
        
        # 如果关键词匹配失败，尝试查找相邻图片
        if not related_images:
            related_images = self.find_adjacent_images(md_filename)
        
        return related_images
    
    def find_images_by_content_keywords(self, md_content: str, md_filename: str) -> List[str]:
        """根据MD内容和文件名中的关键词查找相关图片"""
        related_images = []
        
        if not self.images_dir.exists():
            return related_images
        
        # 从文件名中确定协议类型
        protocol = None
        filename_lower = md_filename.lower()
        if 'ospf' in filename_lower and 'ospfv3' not in filename_lower:
            protocol = 'ospf'
        elif 'ospfv3' in filename_lower:
            protocol = 'ospfv3'
        elif 'bgp' in filename_lower:
            protocol = 'bgp'
        elif 'rip' in filename_lower and 'ripng' not in filename_lower:
            protocol = 'rip'
        elif 'ripng' in filename_lower:
            protocol = 'ripng'
        elif 'isis' in filename_lower or 'is-is' in filename_lower:
            protocol = 'isis'
        
        # 从文件名和内容中提取功能关键词
        keywords = set()
        filename_keywords = [
            '基本功能', '虚连接', '负载分担', '快速收敛', 'DR选择', 'NSSA区域', 'Stub区域',
            '路由聚合', 'FRR', 'BFD', '联盟', '团体', '路由反射器', '震荡抑制',
            'Auto FRR', '多实例', '动态对等体', '环路检测', '本地MT', '伪连接',
            '静态路由', '浮动静态', 'NQA', '联动', '引入', 'Keychain', 'RPD', 'BGP-LS',
            '水平分割', '引入外部路由', '防止路由环路'
        ]
        
        for keyword in filename_keywords:
            if keyword in md_filename:
                keywords.add(keyword)
        
        # 从MD内容中提取关键词
        content_keywords = [
            '基本功能', '虚连接', '负载分担', 'FRR', 'BFD', '联盟', '团体',
            '路由反射器', '震荡抑制', '多实例', '动态对等体', '环路检测',
            'NSSA', 'Stub', 'DR选择', '路由聚合', '本地MT', '伪连接'
        ]
        
        for keyword in content_keywords:
            if keyword in md_content:
                keywords.add(keyword)
        
        # 在图片目录中查找包含关键词的图片，优先匹配协议和功能
        if keywords:
            matched_images = []
            
            for img_file in self.images_dir.glob("*.png"):
                img_name = img_file.name
                img_name_lower = img_name.lower()
                
                # 如果确定了协议，先检查协议匹配
                protocol_match = False
                if protocol:
                    if protocol == 'ospf' and 'ospf' in img_name_lower and 'ospfv3' not in img_name_lower:
                        protocol_match = True
                    elif protocol == 'ospfv3' and 'ospfv3' in img_name_lower:
                        protocol_match = True
                    elif protocol == 'bgp' and 'bgp' in img_name_lower:
                        protocol_match = True
                    elif protocol == 'rip' and 'rip' in img_name_lower and 'ripng' not in img_name_lower:
                        protocol_match = True
                    elif protocol == 'ripng' and 'ripng' in img_name_lower:
                        protocol_match = True
                    elif protocol == 'isis' and ('isis' in img_name_lower or 'is-is' in img_name_lower):
                        protocol_match = True
                
                # 检查功能关键词匹配
                keyword_match = False
                matched_keyword = None
                for keyword in keywords:
                    if keyword in img_name:
                        keyword_match = True
                        matched_keyword = keyword
                        break
                
                # 优先级：协议匹配+关键词匹配 > 仅关键词匹配 > 仅协议匹配
                if protocol_match and keyword_match:
                    matched_images.append((str(img_file), 'exact', matched_keyword))
                elif keyword_match:
                    matched_images.append((str(img_file), 'keyword', matched_keyword))
                elif protocol_match:
                    matched_images.append((str(img_file), 'protocol', None))
            
            # 按优先级排序，优先返回exact匹配
            matched_images.sort(key=lambda x: ('exact', 'keyword', 'protocol').index(x[1]))
            
            # 如果有exact匹配，只返回exact匹配的结果
            exact_matches = [img for img in matched_images if img[1] == 'exact']
            if exact_matches:
                # 只返回最好的exact匹配
                for img_path, match_type, _ in exact_matches[:1]:
                    related_images.append(img_path)
            else:
                # 没有exact匹配时，返回其他匹配，限制返回数量
                for img_path, match_type, _ in matched_images[:2]:
                    related_images.append(img_path)
        
        return related_images
    
    def find_adjacent_images(self, md_filename: str) -> List[str]:
        """为没有明确图序号的MD文件查找相邻图片"""
        related_images = []
        
        # 从文件名中提取协议版本号，如"1.5.30.8"
        version_match = re.search(r'(\d+\.\d+\.\d+)\.(\d+)', md_filename)
        if not version_match:
            return related_images
        
        base_version = version_match.group(1)  # 如"1.5.30"
        current_num = int(version_match.group(2))  # 如8
        
        if not self.images_dir.exists():
            return related_images
        
        # 查找相邻序号的图片（前后各2个序号范围）
        search_range = range(max(1, current_num - 2), current_num + 3)
        
        for search_num in search_range:
            # 构建可能的图序号模式
            possible_fig_nums = [
                f"{base_version}.{search_num}",  # 如"1.5.30.8"
                f"{base_version}-{search_num}",  # 如"1.5.30-8"
                f"{base_version.replace('.', '-')}-{search_num}"  # 如"1-5-30-8"
            ]
            
            for img_file in self.images_dir.glob("*.png"):
                img_name = img_file.name
                
                # 检查图片名是否包含相邻的序号
                for fig_pattern in possible_fig_nums:
                    if fig_pattern in img_name:
                        related_images.append(str(img_file))
                        break
                
                # 如果找到图片就跳出内层循环
                if str(img_file) in related_images:
                    break
            
            # 限制最多找到2张相邻图片
            if len(related_images) >= 2:
                break
        
        # 如果还是没找到，尝试通过协议关键词匹配
        if not related_images:
            related_images = self.find_images_by_protocol(md_filename)
        
        return related_images
    
    def find_images_by_protocol(self, md_filename: str) -> List[str]:
        """基于协议关键词查找相关图片"""
        related_images = []
        
        if not self.images_dir.exists():
            return related_images
        
        # 从文件名中提取协议关键词
        protocol_keywords = []
        filename_lower = md_filename.lower()
        
        protocol_map = {
            'ospf': ['ospf', 'OSPF'],
            'ospfv3': ['ospfv3', 'OSPFv3'],
            'bgp': ['bgp', 'BGP'],
            'rip': ['rip', 'RIP'],
            'ripng': ['ripng', 'RIPng'],
            'isis': ['isis', 'IS-IS'],
            '静态路由': ['静态路由', '静态']
        }
        
        for proto, keywords in protocol_map.items():
            if proto in filename_lower:
                protocol_keywords.extend(keywords)
                break
        
        if protocol_keywords:
            # 在图片目录中查找包含协议关键词的图片
            for img_file in self.images_dir.glob("*.png"):
                img_name = img_file.name
                for keyword in protocol_keywords:
                    if keyword in img_name:
                        related_images.append(str(img_file))
                        break
                
                # 限制最多返回1张协议相关图片
                if len(related_images) >= 1:
                    break
        
        return related_images
    
    def process_md_file(self, md_file: Path) -> Optional[Dict]:
        """处理单个md文件"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取各个组件
            topology = self.extract_topology_from_md(content)
            requirement = self.extract_requirement_from_md(content)
            steps = self.extract_steps_from_md(content)
            configs = self.extract_configs_from_md(content)
            
            # 查找相关图片
            related_images = self.find_related_images(content, md_file.name)
            
            # 构建json结构
            result = {
                "topology": topology,
                "requirement": requirement,
                "steps": steps,
                "configs": configs
            }
            
            # 如果找到相关图片，添加到结果中
            if related_images:
                result["related_images"] = related_images
            
            return result
            
        except Exception as e:
            print(f"处理文件 {md_file} 时出错: {e}")
            return None
    
    def process_all_md_files(self):
        """处理所有md文件"""
        if not self.example_dir.exists():
            print(f"源目录不存在: {self.example_dir}")
            return
        
        processed_count = 0
        for md_file in self.example_dir.glob("*.md"):
            print(f"正在处理: {md_file.name}")
            
            result = self.process_md_file(md_file)
            if result:
                # 生成输出文件名
                output_filename = md_file.stem + ".json"
                output_path = self.output_dir / output_filename
                
                # 保存json文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                
                processed_count += 1
                print(f"  -> 已生成: {output_path}")
            else:
                print(f"  -> 处理失败: {md_file.name}")
        
        print(f"\n处理完成! 共处理了 {processed_count} 个文件")
        print(f"输出目录: {self.output_dir}")

def main():
    """主函数"""
    integrator = HuaweiDataIntegrator()
    integrator.process_all_md_files()

if __name__ == "__main__":
    main()