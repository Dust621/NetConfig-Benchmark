#!/usr/bin/env python3
"""
基于LLM的华为NE40E设备手册数据整合脚本
使用大语言模型智能解析MD文档，生成结构化的JSON数据
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Union
import time
import httpx
from openai import OpenAI

def extract_think_content(text):
    """
    提取<think>和</think>标签之间的内容，并返回标签外的内容
    :param text: 包含<think>标签的字符串
    :return: (标签外内容, 标签内内容) 元组，若未找到则标签内内容为None
    """
    match = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
    if match:
        reasoning_content = match.group(1).strip()
        # 去除<think>...</think>部分，保留外部内容
        response_content = (text[:match.start()] + text[match.end():]).strip()
        return response_content, reasoning_content
    return text, None

class LLMClient:
    def __init__(self, api_key="sk-7b818fc469ff47fa8d95d7b24a530869", base_url="https://api.deepseek.com", model="deepseek-chat"):
    # def __init__(self, api_key="sk-GdmMOsWLYBdMwUBwJsaZGKOhM0k7cfuonqzTPvzLVVo1N4SL", base_url="https://chat.cloudapi.vip/v1/", model="claude-sonnet-4-20250514"):
        """
        初始化LLM客户端。

        :param api_key: 访问LLM所需的密钥
        :param base_url: LLM的基础URL
        :param model: 使用的LLM模型名称
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")  # 从环境变量获取API密钥
        self.base_url = base_url
        self.model = model
        
        # 配置代理支持
        http_proxy = os.getenv("PES_HTTP_PROXY") or os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("PES_HTTPS_PROXY") or os.getenv("HTTPS_PROXY")
        
        client_kwargs = {
            "api_key": self.api_key, 
            "base_url": self.base_url,
            "timeout": 60.0  # 增加超时时间
        }
        
        # 如果有代理设置，添加代理配置
        if http_proxy or https_proxy:
            # 使用 HTTPS 代理（优先）或 HTTP 代理
            proxy_url = https_proxy if https_proxy else http_proxy
            
            client_kwargs["http_client"] = httpx.Client(
                proxy=proxy_url,
                timeout=60.0
            )
            print(f"使用代理: {proxy_url}")
        
        self.client = OpenAI(**client_kwargs)

    def send_prompt(self, prompt):
        """
        发送Prompt到模型并获取响应。

        :param prompt: 发送给模型的Prompt字符串
        :return: 解析后的文本响应和推理过程（如果存在）
        """
        try:
            response_content, reasoning_content = self.call_llm(prompt)
            return response_content, reasoning_content
        except Exception as e:
            raise RuntimeError(f"Error calling LLM API: {e}")

    def call_llm(self, prompt):
        """
        调用模型API。

        :param prompt: 发送给模型的Prompt字符串
        :return: 响应内容和推理过程（如果存在）
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.6,
            max_tokens=8096
        )
        # 提取响应内容和推理过程
        response_content = response.choices[0].message.content
        if self.model == "deepseek-reasoner":
            reasoning_content = getattr(response.choices[0].message, 'reasoning_content', None)
        elif "claude" in self.model:
            response_content, reasoning_content = extract_think_content(response.choices[0].message.content)
        else:
            reasoning_content = "非深度思考模型，无推理上下文"
        return response_content, reasoning_content

class HuaweiDataLLMIntegrator:
    def __init__(self, base_dir: str = "datasets/Huawei", api_key: str = None, base_url: str = None, model: str = None):
        self.base_dir = Path(base_dir)
        self.example_dir = self.base_dir / "example"
        self.images_dir = self.base_dir / "extracted_images"
        self.output_dir = self.base_dir / "llm_integrated_data"
        
        # 确保输出目录存在
        self.output_dir.mkdir(exist_ok=True)
        
        # 初始化LLM客户端
        client_kwargs = {}
        if api_key:
            client_kwargs["api_key"] = api_key
        if base_url:
            client_kwargs["base_url"] = base_url
        if model:
            client_kwargs["model"] = model
        
        self.client = LLMClient(**client_kwargs)
        
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
        
        # 从现有的成功示例中选择一些作为few-shot examples
        examples = """
示例1 - OSPF基本功能：
```json
{
  "topology": "DeviceA 和 DeviceB 作为ABR，连接区域0、区域1和区域2。DeviceC 和 DeviceE 位于区域1。DeviceD 和 DeviceF 位于区域2。",
  "requirement": "所有的路由器都运行OSPF，并将整个自治系统划分为3个区域。其中，DeviceA和DeviceB作为ABR（区域边界路由器）来转发区域之间的路由。配置完成后，每台路由器都应学到自治系统内的所有网段的路由。",
  "steps": [
    "在各路由器上使能OSPF。",
    "指定不同区域内的网段。",
    "配置OSPF区域的密文验证模式。"
  ],
  "configs": {
    "DeviceA": "#\\nsysname DeviceA\\n#\\nrouter id 1.1.1.1\\n#\\ninterface GigabitEthernet1/0/0\\n undo shutdown\\n ip address 192.168.0.1 255.255.255.0\\n#\\nospf\\n area 0.0.0.0\\n  network 192.168.0.0 0.0.0.255\\n#\\nreturn",
    "DeviceB": "#\\nsysname DeviceB\\n#\\nrouter id 2.2.2.2\\n#\\ninterface GigabitEthernet1/0/0\\n undo shutdown\\n ip address 192.168.0.2 255.255.255.0\\n#\\nospf\\n area 0.0.0.0\\n  network 192.168.0.0 0.0.0.255\\n#\\nreturn"
  },
  "related_images": [
    "图1-42 配置 OSPF 基本功能组网图.png"
  ]
}
```

示例2 - BGP负载分担：
```json
{
  "topology": "组网需求如图1154所示，所有路由器都配置BGP，DeviceA和DeviceB在AS100中，DeviceC、DeviceD和DeviceE在AS200中。",
  "requirement": "通过配置BGP非等值负载分担可以根据每条路由的带宽值动态分配流量，减少网络拥塞，充分利用网络资源。",
  "steps": [
    "在DeviceA和DeviceC、DeviceD之间配置EBGP连接。",
    "配置扩展团体属性发布给对等体。",
    "配置非等值负载分担功能。"
  ],
  "configs": {
    "DeviceA": "#\\nsysname DeviceA\\n#\\nbgp router-id 1.0.0.1\\n#\\nreturn"
  },
  "related_images": [
    "图1-154 配置BGP 非等值负载分担组网图.png"
  ]
}
```
"""
        
        # 构造可用图片列表字符串
        images_list = "\n".join([f"- {img}" for img in available_images[:50]])  # 限制数量避免prompt过长
        
        prompt = f"""你是一个专业的网络配置文档解析专家，需要将华为网络设备的Markdown配置文档转换为结构化的JSON数据。

## 任务要求

将以下Markdown文档解析为JSON格式，包含以下字段：

1. **topology**: 网络拓扑描述（从"网络拓扑"、"拓扑结构"或"组网需求"章节提取）
2. **requirement**: 组网需求描述（从"组网需求"、"配置需求"章节提取）  
3. **steps**: 配置思路步骤数组（优先从"配置思路"章节提取，如没有则从操作步骤中提取主要步骤）
4. **configs**: 设备配置字典，key为设备名，value为配置内容
5. **related_images**: 相关图片数组（从文档中提到的图序号匹配，如"图1-42"等）

## 重要处理规则

### 配置处理规则：
- 配置命令中如遇到 `#command` 格式，需要拆分为两行：`#` 和 `command`
- 例如：`#sysname DeviceA` 应该处理为 `#\\nsysname DeviceA`
- 配置内容使用 `\\n` 表示换行

### 图片匹配规则：
- 仔细查找文档中提到的图序号，如"图1-42"、"如图1-77所示"等
- 根据文档内容和功能匹配最相关的图片
- 优先匹配协议类型（OSPF、BGP、RIP等）和功能描述
- 对于文件名：`{md_filename}`，重点关注其中的协议和功能关键词

### 内容提取规则：
- topology: 简洁描述网络拓扑结构和设备角色
- requirement: 完整描述配置需求和目标
- steps: 提取配置思路或主要操作步骤，每个步骤为一个独立的字符串
- configs: 提取每个设备的完整配置，保持原有格式

## 参考示例

{examples}

## 可用图片列表
{images_list}

## 待处理文档

文件名: {md_filename}

文档内容:
```markdown
{md_content}
```

## 输出要求

请直接输出JSON格式的结果，确保：
1. JSON格式正确且完整
2. 字符串中的换行使用 `\\n` 表示  
3. 配置中的 `#command` 格式已正确处理
4. 图片匹配准确，基于文档内容和功能相关性
5. 不要添加任何解释文字，直接输出JSON

输出JSON:"""
        
        return prompt
    
    def call_llm(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """调用LLM API"""
        for attempt in range(max_retries):
            try:
                # 在prompt前添加系统指令
                enhanced_prompt = f"""你是一个专业的网络配置文档解析专家，专门处理华为网络设备配置文档。请严格按照要求输出JSON格式数据，不要添加任何其他内容。

{prompt}"""
                
                response_content, reasoning_content = self.client.send_prompt(enhanced_prompt)
                
                # 如果有推理过程，打印出来（可选）
                if reasoning_content and reasoning_content != "非深度思考模型，无推理上下文":
                    print(f"🤔 推理过程: {reasoning_content[:200]}...")
                
                return response_content.strip()
                
            except Exception as e:
                print(f"调用LLM API失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 指数退避
                else:
                    print(f"所有重试都失败了")
                    return None
        
        return None
    
    def parse_llm_response(self, response: str) -> Optional[Dict]:
        """解析LLM响应并验证JSON格式"""
        if not response:
            return None
        
        try:
            # 尝试提取JSON内容（处理可能的markdown格式）
            json_content = response.strip()
            
            # 如果响应包含markdown代码块，提取其中的JSON
            if "```json" in json_content:
                # 提取```json和```之间的内容
                start_marker = "```json"
                end_marker = "```"
                start_idx = json_content.find(start_marker)
                if start_idx != -1:
                    start_idx += len(start_marker)
                    end_idx = json_content.find(end_marker, start_idx)
                    if end_idx != -1:
                        json_content = json_content[start_idx:end_idx].strip()
            elif "```" in json_content and json_content.count("```") >= 2:
                # 处理通用代码块格式
                parts = json_content.split("```")
                if len(parts) >= 3:
                    json_content = parts[1].strip()
            
            # 尝试解析JSON
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
            print(f"原始响应: {response[:300]}...")
            
            # 尝试修复常见的JSON格式问题
            try:
                # 移除可能的额外字符
                cleaned_response = response.strip()
                if cleaned_response.startswith("```json"):
                    cleaned_response = cleaned_response[7:]
                if cleaned_response.endswith("```"):
                    cleaned_response = cleaned_response[:-3]
                
                # 再次尝试解析
                data = json.loads(cleaned_response.strip())
                print("✅ JSON修复成功")
                return data
                
            except:
                print(f"JSON修复也失败了")
                return None
        
        except Exception as e:
            print(f"解析响应时发生未知错误: {e}")
            return None
    
    def process_md_file(self, md_file: Path) -> Optional[Dict]:
        """使用LLM处理单个md文件"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"正在使用LLM处理: {md_file.name}")
            
            # 构造prompt
            prompt = self.construct_prompt(content, md_file.name, self.available_images)
            
            # 调用LLM
            llm_response = self.call_llm(prompt)
            if not llm_response:
                print(f"  -> LLM调用失败: {md_file.name}")
                return None
            
            # 解析响应
            result = self.parse_llm_response(llm_response)
            if not result:
                print(f"  -> 解析LLM响应失败: {md_file.name}")
                return None
            
            print(f"  -> LLM处理成功: {md_file.name}")
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
    
    parser = argparse.ArgumentParser(description="使用LLM处理华为网络配置文档")
    parser.add_argument("--api-key", help="API密钥")
    parser.add_argument("--base-url", help="API基础URL")
    parser.add_argument("--model", help="使用的LLM模型")
    parser.add_argument("--provider", choices=["deepseek", "claude", "openai"], 
                       default="deepseek", help="LLM提供商")
    parser.add_argument("--limit", type=int, help="限制处理的文件数量（用于测试）")
    
    args = parser.parse_args()
    
    # 根据提供商设置默认值
    if args.provider == "deepseek":
        default_api_key_env = "DEEPSEEK_API_KEY"
        default_base_url = "https://api.deepseek.com"
        default_model = "deepseek-chat"
        api_description = "DeepSeek API密钥"
    elif args.provider == "claude":
        default_api_key_env = "ANTHROPIC_API_KEY" 
        default_base_url = "https://chat.cloudapi.vip/v1/"
        default_model = "claude-sonnet-4-20250514"
        api_description = "Claude API密钥"
    elif args.provider == "openai":
        default_api_key_env = "OPENAI_API_KEY"
        default_base_url = "https://api.openai.com/v1"
        default_model = "gpt-4"
        api_description = "OpenAI API密钥"
    else:
        # 默认使用deepseek
        default_api_key_env = "DEEPSEEK_API_KEY"
        default_base_url = "https://api.deepseek.com"
        default_model = "deepseek-chat"
        api_description = "DeepSeek API密钥"
    
    # 获取配置参数
    api_key = args.api_key or os.getenv(default_api_key_env)
    base_url = args.base_url or default_base_url
    model = args.model or default_model
    
    if not api_key:
        print(f"错误: 请提供{api_description}")
        print(f"方法1: 设置环境变量 {default_api_key_env}")
        print(f"方法2: 使用 --api-key 参数")
        return
    
    print(f"使用{args.provider}提供商")
    print(f"模型: {model}")
    print(f"API地址: {base_url}")
    
    integrator = HuaweiDataLLMIntegrator(
        api_key=api_key, 
        base_url=base_url,
        model=model
    )
    integrator.process_all_md_files(limit=args.limit)

if __name__ == "__main__":
    main()