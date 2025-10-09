#!/usr/bin/env python3
"""
支持多种LLM的华为NE40E设备手册数据整合脚本
支持OpenAI、Claude、Ollama等多种LLM提供商
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
import time
import requests
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """LLM提供商的抽象基类"""
    
    @abstractmethod
    def call_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        pass

class OpenAIProvider(LLMProvider):
    """OpenAI API提供商"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("请安装OpenAI库: pip install openai")
    
    def call_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system", 
                            "content": "你是一个专业的网络配置文档解析专家，专门处理华为网络设备配置文档。请严格按照要求输出JSON格式数据。"
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=4000,
                    response_format={"type": "json_object"}
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"OpenAI API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None

class ClaudeProvider(LLMProvider):
    """Claude API提供商"""
    
    def __init__(self, api_key: str, model: str = "claude-3-sonnet-20240229"):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model
        except ImportError:
            raise ImportError("请安装Anthropic库: pip install anthropic")
    
    def call_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(max_retries):
            try:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=4000,
                    temperature=0.1,
                    system="你是一个专业的网络配置文档解析专家，专门处理华为网络设备配置文档。请严格按照要求输出JSON格式数据。",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                return message.content[0].text.strip()
                
            except Exception as e:
                print(f"Claude API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None

class OllamaProvider(LLMProvider):
    """Ollama本地模型提供商"""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def call_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 4000
                        }
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result.get("response", "").strip()
                
            except Exception as e:
                print(f"Ollama API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        
        return None

class HuaweiDataMultiLLMIntegrator:
    def __init__(self, base_dir: str = "datasets/Huawei", provider: LLMProvider = None):
        self.base_dir = Path(base_dir)
        self.example_dir = self.base_dir / "example"
        self.images_dir = self.base_dir / "extracted_images"
        self.output_dir = self.base_dir / "multi_llm_integrated_data"
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # LLM提供商
        self.provider = provider
        
        # 获取可用图片列表
        self.available_images = self.get_available_images()
    
    def get_available_images(self) -> List[str]:
        """获取所有可用的图片文件列表"""
        if not self.images_dir.exists():
            return []
        
        images = []
        for img_file in self.images_dir.glob("*.png"):
            images.append(img_file.name)
        return sorted(images)
    
    def construct_prompt(self, md_content: str, md_filename: str, available_images: List[str]) -> str:
        """构造LLM处理的prompt"""
        
        # 简化的示例，避免prompt过长
        example = """
示例输出格式:
```json
{
  "topology": "网络拓扑描述，简洁描述设备角色和连接关系",
  "requirement": "组网需求描述，说明配置目标和要求", 
  "steps": [
    "配置步骤1：具体操作描述",
    "配置步骤2：具体操作描述"
  ],
  "configs": {
    "DeviceA": "#\\nsysname DeviceA\\n#\\ninterface GE1/0/0\\n ip address 192.168.1.1 255.255.255.0\\n#\\nreturn",
    "DeviceB": "#\\nsysname DeviceB\\n#\\ninterface GE1/0/0\\n ip address 192.168.1.2 255.255.255.0\\n#\\nreturn"
  },
  "related_images": [
    "图1-42 配置 OSPF 基本功能组网图.png"
  ]
}
```
"""
        
        # 构造可用图片列表字符串（限制数量避免prompt过长）
        images_list = "\\n".join([f"- {img}" for img in available_images[:30]])
        
        prompt = f"""任务：将华为网络设备Markdown配置文档转换为JSON格式数据

## 输出要求
1. 严格输出JSON格式，不要任何解释文字
2. 包含字段：topology, requirement, steps, configs, related_images
3. configs中的配置命令如遇到 `#command` 格式需拆分为 `#\\ncommand`
4. 根据文档内容和功能匹配最相关的图片

{example}

## 可用图片列表（选择最相关的）
{images_list}

## 文档信息
文件名: {md_filename}

文档内容:
```markdown
{md_content}
```

请输出JSON格式结果："""
        
        return prompt
    
    def parse_llm_response(self, response: str) -> Optional[Dict]:
        """解析LLM响应并验证JSON格式"""
        if not response:
            return None
        
        try:
            # 尝试提取JSON内容（处理可能的markdown格式）
            json_content = response
            if "```json" in response:
                json_content = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_content = response.split("```")[1].split("```")[0].strip()
            
            # 解析JSON
            data = json.loads(json_content)
            
            # 验证必需字段
            required_fields = ["topology", "requirement", "steps", "configs"]
            for field in required_fields:
                if field not in data:
                    print(f"LLM响应缺少必需字段: {field}")
                    return None
            
            # 验证数据类型
            if not isinstance(data["steps"], list):
                print("steps字段应该是数组")
                return None
            
            if not isinstance(data["configs"], dict):
                print("configs字段应该是对象")
                return None
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"解析LLM响应JSON失败: {e}")
            print(f"响应内容: {response[:500]}...")
            return None
    
    def process_md_file(self, md_file: Path) -> Optional[Dict]:
        """使用LLM处理单个md文件"""
        if not self.provider:
            print("错误：未设置LLM提供商")
            return None
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"正在处理: {md_file.name}")
            
            # 构造prompt
            prompt = self.construct_prompt(content, md_file.name, self.available_images)
            
            # 调用LLM
            llm_response = self.provider.call_llm(prompt)
            if not llm_response:
                print(f"  -> LLM调用失败: {md_file.name}")
                return None
            
            # 解析响应
            result = self.parse_llm_response(llm_response)
            if not result:
                print(f"  -> 解析LLM响应失败: {md_file.name}")
                return None
            
            print(f"  -> 处理成功: {md_file.name}")
            return result
            
        except Exception as e:
            print(f"处理文件 {md_file} 时出错: {e}")
            return None
    
    def process_all_md_files(self, limit: int = None):
        """处理所有md文件"""
        if not self.example_dir.exists():
            print(f"源目录不存在: {self.example_dir}")
            return
        
        md_files = list(self.example_dir.glob("*.md"))
        if limit:
            md_files = md_files[:limit]
        
        processed_count = 0
        failed_count = 0
        
        for md_file in md_files:
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
                failed_count += 1
                print(f"  -> 处理失败: {md_file.name}")
            
            # 添加延迟避免API限制
            time.sleep(1)
        
        print(f"\\n处理完成!")
        print(f"成功处理: {processed_count} 个文件")
        print(f"失败: {failed_count} 个文件")
        print(f"输出目录: {self.output_dir}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="使用多种LLM处理华为网络配置文档")
    parser.add_argument("--provider", choices=["openai", "claude", "ollama"], 
                       default="openai", help="LLM提供商")
    parser.add_argument("--api-key", help="API密钥 (OpenAI/Claude)")
    parser.add_argument("--model", help="使用的模型")
    parser.add_argument("--base-url", help="Ollama服务器地址", default="http://localhost:11434")
    parser.add_argument("--limit", type=int, help="限制处理的文件数量（用于测试）")
    
    args = parser.parse_args()
    
    # 根据选择创建对应的提供商
    provider = None
    
    if args.provider == "openai":
        api_key = args.api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("错误: 请提供OpenAI API密钥")
            return
        model = args.model or "gpt-4"
        provider = OpenAIProvider(api_key=api_key, model=model)
        print(f"使用OpenAI提供商，模型: {model}")
    
    elif args.provider == "claude":
        api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            print("错误: 请提供Anthropic API密钥")
            return
        model = args.model or "claude-3-sonnet-20240229"
        provider = ClaudeProvider(api_key=api_key, model=model)
        print(f"使用Claude提供商，模型: {model}")
    
    elif args.provider == "ollama":
        model = args.model or "llama2"
        provider = OllamaProvider(model=model, base_url=args.base_url)
        print(f"使用Ollama提供商，模型: {model}，服务器: {args.base_url}")
    
    if not provider:
        print("错误: 无法初始化LLM提供商")
        return
    
    integrator = HuaweiDataMultiLLMIntegrator(provider=provider)
    integrator.process_all_md_files(limit=args.limit)

if __name__ == "__main__":
    main()