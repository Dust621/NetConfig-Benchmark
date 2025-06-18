from collections import Counter
import math
import re



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

class ConfigBLEU:
    def __init__(self, max_n=4):
        self.max_n = max_n  # 最大n-gram长度
    
    def tokenize_config(self, config_str):
        """将配置文本转换为token列表"""
        # 移除注释和空行
        lines = [line.strip() for line in config_str.split('\n') if line.strip() and not line.startswith('#')]
        
        # 将每行配置转换为token
        tokens = []
        for line in lines:
            # 处理缩进
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            
            # 将配置行分割为token
            line_tokens = line.split()
            tokens.extend(line_tokens)
        
        return tokens
    
    def get_ngrams(self, tokens, n):
        """获取n-gram"""
        return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    
    def calculate_bleu(self, reference_config, candidate_config):
        """计算BLEU分数"""
        # 将配置转换为token
        reference_tokens = self.tokenize_config(reference_config)
        candidate_tokens = self.tokenize_config(candidate_config)
        
        # 计算n-gram精确率
        precisions = []
        for n in range(1, self.max_n + 1):
            reference_ngrams = Counter(self.get_ngrams(reference_tokens, n))
            candidate_ngrams = Counter(self.get_ngrams(candidate_tokens, n))
            
            # 计算匹配的n-gram数量
            matches = sum((reference_ngrams & candidate_ngrams).values())
            total = sum(candidate_ngrams.values())
            
            # 计算n-gram精确率
            precision = matches / total if total > 0 else 0
            precisions.append(precision)
        
        # 计算几何平均精确率
        if 0 in precisions:
            return 0.0
        
        log_precision = sum(math.log(p) for p in precisions) / len(precisions)
        bp = self.calculate_brevity_penalty(reference_tokens, candidate_tokens)
        
        # 计算BLEU分数
        bleu_score = bp * math.exp(log_precision)
        
        return round(bleu_score * 100, 2)
    
    def calculate_brevity_penalty(self, reference_tokens, candidate_tokens):
        """计算简短惩罚因子"""
        if len(candidate_tokens) > len(reference_tokens):
            return 1.0
        return math.exp(1 - len(reference_tokens) / len(candidate_tokens))
    
    def analyze_ngram_matches(self, reference_config, candidate_config):
        """分析n-gram匹配情况"""
        reference_tokens = self.tokenize_config(reference_config)
        candidate_tokens = self.tokenize_config(candidate_config)
        
        analysis = {}
        for n in range(1, self.max_n + 1):
            reference_ngrams = Counter(self.get_ngrams(reference_tokens, n))
            candidate_ngrams = Counter(self.get_ngrams(candidate_tokens, n))
            
            matches = reference_ngrams & candidate_ngrams
            analysis[n] = {
                'matches': list(matches.keys()),
                'match_count': len(matches),
                'total_candidate': len(candidate_ngrams),
                'total_reference': len(reference_ngrams)
            }
        
        return analysis

def main():
    # 使用示例配置
    reference_config = config_str1
    candidate_config = config_str2
    
    bleu = ConfigBLEU(max_n=4)
    score = bleu.calculate_bleu(reference_config, candidate_config)
    
    print(f"BLEU相似度得分: {score}%")
    
    # 分析n-gram匹配情况
    analysis = bleu.analyze_ngram_matches(reference_config, candidate_config)
    print("\nN-gram匹配分析:")
    for n, stats in analysis.items():
        print(f"\n{n}-gram分析:")
        print(f"匹配数量: {stats['match_count']}")
        print(f"候选配置中的{n}-gram总数: {stats['total_candidate']}")
        print(f"参考配置中的{n}-gram总数: {stats['total_reference']}")
        print(f"匹配的{n}-gram示例:")
        for match in stats['matches'][:5]:  # 只显示前5个匹配
            print(f"- {' '.join(match)}")

if __name__ == "__main__":
    main()
