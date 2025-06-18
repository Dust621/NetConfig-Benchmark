from typing import List, Dict, Any, Tuple
import re
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class ConfigNode:
    name: str
    value: str = ""
    children: List['ConfigNode'] = None
    level: int = 0  # 添加层级信息
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    def get_structure_signature(self) -> str:
        """获取节点的结构特征"""
        if not self.children:
            return f"{self.name}"
        children_sig = "(" + ",".join(child.get_structure_signature() for child in self.children) + ")"
        return f"{self.name}{children_sig}"

def parse_config(config_str: str) -> ConfigNode:
    """将配置字符串解析为树形结构"""
    root = ConfigNode("root", level=0)
    current_path = [root]
    
    # 按行解析配置
    lines = config_str.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # 计算缩进级别
        indent = len(line) - len(line.lstrip())
        level = indent // 2  # 假设每级缩进是2个空格
        
        # 调整当前路径
        while len(current_path) > level + 1:
            current_path.pop()
            
        # 解析命令
        parts = line.strip().split()
        if not parts:
            continue
            
        # 创建新节点
        node = ConfigNode(parts[0], ' '.join(parts[1:]) if len(parts) > 1 else "", level=level)
        current_path[-1].children.append(node)
        current_path.append(node)
    
    return root

def calculate_tree_similarity(tree1: ConfigNode, tree2: ConfigNode) -> Tuple[float, float]:
    """计算两棵配置树的相似度，返回(结构相似度, 内容相似度)"""
    def get_node_content_signature(node: ConfigNode) -> str:
        """获取节点的内容特征"""
        return f"{node.name}:{node.value}"
    
    def count_nodes(node: ConfigNode) -> int:
        """计算树中的节点总数"""
        return 1 + sum(count_nodes(child) for child in node.children)
    
    def calculate_structure_similarity(node1: ConfigNode, node2: ConfigNode) -> float:
        """计算结构相似度"""
        if node1.get_structure_signature() == node2.get_structure_signature():
            return 1.0
        
        # 计算子节点的结构相似度
        if not node1.children or not node2.children:
            return 0.0
            
        # 使用最长公共子序列算法计算子节点匹配
        matches = []
        for child1 in node1.children:
            best_match = 0.0
            for child2 in node2.children:
                if child1.name == child2.name:
                    match = calculate_structure_similarity(child1, child2)
                    best_match = max(best_match, match)
            matches.append(best_match)
        
        return sum(matches) / max(len(node1.children), len(node2.children))
    
    def calculate_content_similarity(node1: ConfigNode, node2: ConfigNode) -> float:
        """计算内容相似度"""
        if get_node_content_signature(node1) == get_node_content_signature(node2):
            content_match = 1.0
        else:
            # 如果节点名称相同但值不同，给予部分分数
            # content_match = 0.5 if node1.name == node2.name else 0.0
            content_match = 0.0
        
        if not node1.children or not node2.children:
            return content_match
            
        # 计算子节点的内容相似度
        child_matches = []
        for child1 in node1.children:
            best_match = 0.0
            for child2 in node2.children:
                if child1.name == child2.name:
                    match = calculate_content_similarity(child1, child2)
                    best_match = max(best_match, match)
            child_matches.append(best_match)
        
        child_similarity = sum(child_matches) / max(len(node1.children), len(node2.children))
        return 0.7 * content_match + 0.3 * child_similarity
    
    # 计算总体相似度
    structure_sim = calculate_structure_similarity(tree1, tree2)
    content_sim = calculate_content_similarity(tree1, tree2)
    
    return structure_sim, content_sim

def compare_configs(config1: str, config2: str) -> Dict[str, float]:
    """比较两个配置文件的相似度"""
    tree1 = parse_config(config1)
    tree2 = parse_config(config2)
    structure_sim, content_sim = calculate_tree_similarity(tree1, tree2)
    
    # 计算综合相似度
    total_sim = 0.4 * structure_sim + 0.6 * content_sim
    
    return {
        "结构相似度": structure_sim,
        "内容相似度": content_sim,
        "综合相似度": total_sim
    }

# config_str1 = """#
# sysname DeviceC
# #
# interface GigabitEthernet2/0/0
#  undo shutdown
#  ip address 172.16.1.2 255.255.255.0
# #
# rip 2
#  version 2
#  network 172.16.0.0
# #
# return
# """

# config_str2 = """#
# sysname DeviceC
# #
# interface GigabitEthernet2/0/0
#  undo shutdown
#  ip address 10.1.1.2 255.255.255.0
# #
# rip 1
#  version 2
#  network 172.16.0.0
# #
# return
# """

config_str1 = """
#
sysname R1
#
interface GE0/0/0
 undo shutdown
 ip address 10.0.1.1 255.255.255.0
#
interface LoopBack0
 ip address 1.1.0.1 255.255.255.255
#
bgp 64513
 router-id 1.1.0.1
 peer 10.0.1.2 as-number 64512
 #
 ipv4-family unicast
  undo synchronization
  peer 10.0.1.2 enable
  network 1.1.0.1 255.255.255.255
#
ip route-static 2.2.0.2 255.255.255.255 10.0.1.2
#
"""


config_str2 = """# 
sysname R1
#
interface GigabitEthernet0/0/0
 ip address 10.0.1.1 255.255.255.0
#
interface LoopBack0
 ip address 1.1.0.1 255.255.255.255
#
interface LoopBack1
 ip address 1.1.1.1 255.255.255.0
#
bgp 64513
 router-id 1.1.0.1
 peer 2.2.0.2 as-number 64512
 peer 2.2.0.2 ebgp-max-hop 2
 peer 2.2.0.2 connect-interface LoopBack0
#
 ipv4-family unicast
  undo synchronization
  network 1.1.1.0 255.255.255.0
  peer 2.2.0.2 enable
#
ip route-static 2.2.0.2 255.255.255.255 10.0.1.2
#
return
"""

# 示例使用
if __name__ == "__main__":
    similarity = compare_configs(config_str1, config_str2)
    print("配置相似度分析结果：")
    for metric, value in similarity.items():
        print(f"{metric}: {value:.2f}")