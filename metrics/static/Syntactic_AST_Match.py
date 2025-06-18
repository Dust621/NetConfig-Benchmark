from tree_sitter import Parser, Language
import os

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 编译语法文件
Language.build_library(
    os.path.join(current_dir, 'build/config_grammar.so'),
    [current_dir]
)

class ConfigASTParser:
    def __init__(self):
        self.parser = Parser()
        
        # 加载编译后的语法规则
        CONFIG_LANGUAGE = Language(os.path.join(current_dir, 'build/config_grammar.so'))
        self.parser.set_language(CONFIG_LANGUAGE)
    
    def parse_config(self, config_str):
        """解析配置文件生成AST"""
        return self.parser.parse(bytes(config_str, 'utf8')).root_node

class ConfigASTSimilarity:
    def __init__(self):
        self.parser = ConfigASTParser()
    
    def get_all_subtrees(self, root_node):
        """获取所有子树"""
        node_stack = []
        subtree_list = []
        depth = 1
        node_stack.append([root_node, depth])
        
        while node_stack:
            cur_node, cur_depth = node_stack.pop()
            subtree_list.append([str(cur_node), cur_depth])
            
            for child_node in cur_node.children:
                if child_node.children:
                    node_stack.append([child_node, cur_depth + 1])
        
        return subtree_list
    
    def calculate_similarity(self, reference_config, candidate_config):
        """计算AST相似度"""
        try:
            # 解析配置文件
            reference_tree = self.parser.parse_config(reference_config)
            candidate_tree = self.parser.parse_config(candidate_config)
            
            # 获取所有子树
            ref_subtrees = [x[0] for x in self.get_all_subtrees(reference_tree)]
            cand_subtrees = [x[0] for x in self.get_all_subtrees(candidate_tree)]
            
            # 计算匹配数
            match_count = 0
            total_count = len(ref_subtrees)
            
            for subtree in ref_subtrees:
                if subtree in cand_subtrees:
                    match_count += 1
            
            # 计算相似度
            similarity = match_count / total_count if total_count > 0 else 0
            return round(similarity * 100, 2)
        except Exception as e:
            print(f"计算相似度时出错: {str(e)}")
            return 0.0
    
    def analyze_matches(self, reference_config, candidate_config):
        """分析匹配情况"""
        try:
            reference_tree = self.parser.parse_config(reference_config)
            candidate_tree = self.parser.parse_config(candidate_config)
            
            ref_subtrees = [x[0] for x in self.get_all_subtrees(reference_tree)]
            cand_subtrees = [x[0] for x in self.get_all_subtrees(candidate_tree)]
            
            matches = set(ref_subtrees) & set(cand_subtrees)
            missing = set(ref_subtrees) - set(cand_subtrees)
            extra = set(cand_subtrees) - set(ref_subtrees)
            
            return {
                'matches': list(matches),
                'missing': list(missing),
                'extra': list(extra),
                'match_count': len(matches),
                'total_reference': len(ref_subtrees),
                'total_candidate': len(cand_subtrees)
            }
        except Exception as e:
            print(f"分析匹配情况时出错: {str(e)}")
            return {
                'matches': [],
                'missing': [],
                'extra': [],
                'match_count': 0,
                'total_reference': 0,
                'total_candidate': 0
            }

def main():
    # 示例配置
    reference_config = """
    sysname R1
    interface GE0/0/0
     ip address 10.0.1.1 255.255.255.0
    interface LoopBack0
     ip address 1.1.0.1 255.255.255.255
    """
    
    candidate_config = """
    sysname R1
    interface GigabitEthernet0/0/0
     ip address 10.0.1.1 255.255.255.0
    interface LoopBack0
     ip address 1.1.0.1 255.255.255.255
    interface LoopBack1
     ip address 1.1.1.1 255.255.255.0
    """
    
    # 创建相似度计算器
    similarity = ConfigASTSimilarity()
    
    # 计算相似度
    score = similarity.calculate_similarity(reference_config, candidate_config)
    print(f"AST相似度得分: {score}%")
    
    # 分析匹配情况
    analysis = similarity.analyze_matches(reference_config, candidate_config)
    print("\n匹配分析:")
    print(f"匹配数量: {analysis['match_count']}")
    print(f"参考配置子树总数: {analysis['total_reference']}")
    print(f"候选配置子树总数: {analysis['total_candidate']}")
    
    print("\n匹配的子树示例:")
    for match in analysis['matches'][:5]:
        print(f"- {match}")
    
    print("\n缺失的子树示例:")
    for missing in analysis['missing'][:5]:
        print(f"- {missing}")
    
    print("\n多余的子树示例:")
    for extra in analysis['extra'][:5]:
        print(f"- {extra}")

if __name__ == "__main__":
    main()