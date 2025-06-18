# config_str1 = """
# #
# sysname R1
# #
# interface GE0/0/0
#  undo shutdown
#  ip address 10.0.1.1 255.255.255.0
# #
# interface LoopBack0
#  ip address 1.1.0.1 255.255.255.255
# #
# bgp 64513
#  router-id 1.1.0.1
#  peer 10.0.1.2 as-number 64512
#  #
#  ipv4-family unicast
#   undo synchronization
#   peer 10.0.1.2 enable
#   network 1.1.0.1 255.255.255.255
# #
# ip route-static 2.2.0.2 255.255.255.255 10.0.1.2
# #
# """


# config_str2 = """# 
# sysname R1
# #
# interface GigabitEthernet0/0/0
#  ip address 10.0.1.1 255.255.255.0
# #
# interface LoopBack0
#  ip address 1.1.0.1 255.255.255.255
# #
# interface LoopBack1
#  ip address 1.1.1.1 255.255.255.0
# #
# bgp 64513
#  router-id 1.1.0.1
#  peer 2.2.0.2 as-number 64512
#  peer 2.2.0.2 ebgp-max-hop 2
#  peer 2.2.0.2 connect-interface LoopBack0
# #
#  ipv4-family unicast
#   undo synchronization
#   network 1.1.1.0 255.255.255.0
#   peer 2.2.0.2 enable
# #
# ip route-static 2.2.0.2 255.255.255.255 10.0.1.2
# #
# return
# """

config_str1 = """#
sysname DeviceC
#
interface GigabitEthernet2/0/0
 undo shutdown
 ip address 172.16.1.2 255.255.255.0
#
rip 1
 version 2
 network 172.16.0.0
#
return
"""

config_str2 = """#
sysname DeviceC
#
interface GigabitEthernet2/0/0
 undo shutdown
 ip address 10.1.1.2 255.255.255.0
#
rip 1
 version 2
 network 172.16.0.0
#
return
"""

class ConfigPrecisionRecall:
    def __init__(self):
        self.target_config = None
        self.test_config = None
    
    def parse_config(self, config_str):
        """解析配置文件，返回命令列表"""
        commands = []
        current_command = []
        
        for line in config_str.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                if current_command:
                    commands.append(' '.join(current_command))
                    current_command = []
                continue
            
            # 计算缩进级别
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            
            if indent == 0:
                if current_command:
                    commands.append(' '.join(current_command))
                current_command = [line]
            else:
                current_command.append(line)
        
        # 添加最后一个命令
        if current_command:
            commands.append(' '.join(current_command))
            
        return commands
    
    def calculate_metrics(self, target_config, test_config):
        """计算精确率和召回率"""
        self.target_config = self.parse_config(target_config)
        self.test_config = self.parse_config(test_config)
        
        # 计算匹配的命令数
        matched_commands = set(self.target_config) & set(self.test_config)
        
        # 计算精确率 (Precision)
        precision = len(matched_commands) / len(self.test_config) if self.test_config else 0
        
        # 计算召回率 (Recall)
        recall = len(matched_commands) / len(self.target_config) if self.target_config else 0
        
        # 计算F1分数
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'precision': round(precision * 100, 2),
            'recall': round(recall * 100, 2),
            'f1_score': round(f1_score * 100, 2),
            'matched_commands': list(matched_commands),
            'missing_commands': list(set(self.target_config) - set(self.test_config)),
            'extra_commands': list(set(self.test_config) - set(self.target_config))
        }

def main():
    # 使用示例配置
    target_config = config_str2
    test_config = config_str1
    
    analyzer = ConfigPrecisionRecall()
    results = analyzer.calculate_metrics(target_config, test_config)
    
    print("配置匹配分析结果:")
    print(f"精确率 (Precision): {results['precision']}%")
    print(f"召回率 (Recall): {results['recall']}%")
    print(f"F1分数: {results['f1_score']}%")
    print("\n匹配的命令:")
    for cmd in results['matched_commands']:
        print(f"- {cmd}")
    print("\n缺失的命令:")
    for cmd in results['missing_commands']:
        print(f"- {cmd}")
    print("\n多余的命令:")
    for cmd in results['extra_commands']:
        print(f"- {cmd}")

if __name__ == "__main__":
    main()