from tree_sitter import Language
import os

def build_parser():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(current_dir, 'build')
    
    # 确保 build 目录存在
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    # 编译语法文件
    Language.build_library(
        os.path.join(build_dir, 'config_grammar.so'),
        [current_dir]
    )

if __name__ == '__main__':
    build_parser() 