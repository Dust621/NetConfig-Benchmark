class ASTNode:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.children = []
        self.parent = None
    
    def add_child(self, child):
        child.parent = self
        self.children.append(child)

class HuaweiConfigParser:
    def __init__(self):
        self.current_node = None
        self.root = ASTNode("root")
    
    def parse_config(self, config_str):
        lines = config_str.strip().split('\n')
        current_indent = 0
        stack = [self.root]
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 计算缩进级别（每4个空格为一级）
            indent = (len(line) - len(line.lstrip())) // 4
            line = line.strip()
            
            # 根据缩进调整节点层级
            while len(stack) > 1 and indent <= current_indent:
                stack.pop()
                current_indent -= 1
            
            # 创建新节点
            node = ASTNode(line)
            stack[-1].add_child(node)
            stack.append(node)
            current_indent = indent
            
        return self.root

class ConfigSimilarity:
    def __init__(self):
        self.parser = HuaweiConfigParser()
    
    def calculate_similarity(self, config1, config2):
        tree1 = self.parser.parse_config(config1)
        print(tree1)
        tree2 = self.parser.parse_config(config2)
        print(tree2)
        
        # 计算三个维度的相似度
        structure_sim = self._calculate_structure_similarity(tree1, tree2)
        content_sim = self._calculate_content_similarity(tree1, tree2)
        order_sim = self._calculate_order_similarity(tree1, tree2)
        
        # 加权计算最终相似度
        final_similarity = (
            structure_sim * 0.4 +
            content_sim * 0.4 +
            order_sim * 0.2
        )
        
        return round(final_similarity, 2)
    
    def _calculate_structure_similarity(self, node1, node2):
        """计算结构相似度"""
        if not node1 and not node2:
            return 100.0
        if not node1 or not node2:
            return 0.0
            
        # 计算节点层级匹配
        level_match = 1.0 if self._get_node_level(node1) == self._get_node_level(node2) else 0.0
        
        # 计算子节点结构匹配
        children_structure = 0.0
        if node1.children and node2.children:
            # 计算子节点数量比例
            children_ratio = min(len(node1.children), len(node2.children)) / max(len(node1.children), len(node2.children))
            
            # 计算子节点层级匹配
            level_matches = []
            used_children = set()
            
            for child1 in node1.children:
                for j, child2 in enumerate(node2.children):
                    if j not in used_children and self._get_node_level(child1) == self._get_node_level(child2):
                        level_matches.append(1.0)
                        used_children.add(j)
                        break
            
            children_structure = (children_ratio * 0.5 + (sum(level_matches) / max(len(node1.children), len(node2.children))) * 0.5) * 100
        
        return (level_match * 30 + children_structure * 70) / 100.0
    
    def _calculate_content_similarity(self, node1, node2):
        """计算内容相似度"""
        if not node1 and not node2:
            return 100.0
        if not node1 or not node2:
            return 0.0
            
        # 计算节点内容匹配
        content_match = self._compare_node_content(node1, node2)
        
        # 计算子节点内容匹配
        children_content = 0.0
        if node1.children and node2.children:
            content_matches = []
            used_children = set()
            
            for child1 in node1.children:
                max_match = 0.0
                best_match_idx = -1
                
                for j, child2 in enumerate(node2.children):
                    if j not in used_children:
                        match = self._compare_node_content(child1, child2)
                        if match > max_match:
                            max_match = match
                            best_match_idx = j
                
                if best_match_idx != -1:
                    used_children.add(best_match_idx)
                    content_matches.append(max_match)
            
            if content_matches:
                children_content = sum(content_matches) / len(content_matches)
        
        return (content_match * 40 + children_content * 60) / 100.0
    
    def _calculate_order_similarity(self, node1, node2):
        """计算顺序相似度"""
        if not node1 and not node2:
            return 100.0
        if not node1 or not node2:
            return 0.0
            
        # 计算节点顺序匹配
        order_match = 1.0 if node1.name == node2.name else 0.0
        
        # 计算子节点顺序匹配
        children_order = 0.0
        if node1.children and node2.children:
            # 使用最长公共子序列算法计算顺序相似度
            lcs_length = self._longest_common_subsequence(
                [child.name for child in node1.children],
                [child.name for child in node2.children]
            )
            children_order = (lcs_length / max(len(node1.children), len(node2.children))) * 100
        
        return (order_match * 30 + children_order * 70) / 100.0
    
    def _get_node_level(self, node):
        """获取节点的层级深度"""
        level = 0
        current = node
        while current.parent:
            level += 1
            current = current.parent
        return level
    
    def _compare_node_content(self, node1, node2):
        """比较节点内容的相似度"""
        if node1.name == node2.name:
            return 100.0
        
        # 分割命令和参数
        cmd1, *params1 = node1.name.split()
        cmd2, *params2 = node2.name.split()
        
        # 命令匹配（考虑命令别名）
        cmd_match = 1.0 if cmd1 == cmd2 else 0.0
        if not cmd_match:
            # 检查命令别名
            if (cmd1 == "GE" and cmd2 == "GigabitEthernet") or \
               (cmd1 == "GigabitEthernet" and cmd2 == "GE"):
                cmd_match = 1.0
        
        # 参数匹配
        param_match = 0.0
        if params1 and params2:
            common_params = set(params1) & set(params2)
            param_match = len(common_params) / max(len(params1), len(params2))
        
        return (cmd_match * 60 + param_match * 40) / 100.0
    
    def _longest_common_subsequence(self, seq1, seq2):
        """计算最长公共子序列长度"""
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]


# config_str1 = """
# sysname R1
# interface GE0/0/0
#     ip address 10.0.1.1 255.255.255.0
# interface LoopBack0
#     ip address 1.1.0.1 255.255.255.255
# """

# config_str2 = """
# sysname R1
# interface GigabitEthernet0/0/0
#     ip address 10.0.1.1 255.255.255.0
# interface LoopBack0
#     ip address 1.1.0.1 255.255.255.255
# interface LoopBack1
#     ip address 1.1.1.1 255.255.255.0
# """



config_str1 = """
sysname R1
"""


config_str2 = """# 
sysname R1
"""

def main():
    
    config_str1 = """
    #
    sysname R2
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
    config1 = config_str1
    config2 = config_str2
    
    similarity = ConfigSimilarity()
    score = similarity.calculate_similarity(config1, config2)
    
    print(f"配置相似度: {score}%")
    
    # 打印详细的相似度分析
    tree1 = similarity.parser.parse_config(config1)
    tree2 = similarity.parser.parse_config(config2)
    
    structure_sim = similarity._calculate_structure_similarity(tree1, tree2)
    content_sim = similarity._calculate_content_similarity(tree1, tree2)
    order_sim = similarity._calculate_order_similarity(tree1, tree2)
    
    print(f"结构相似度: {structure_sim:.2f}%")
    print(f"内容相似度: {content_sim:.2f}%")
    print(f"顺序相似度: {order_sim:.2f}%")

if __name__ == "__main__":
    main()