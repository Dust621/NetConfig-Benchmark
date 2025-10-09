#!/usr/bin/env python3
"""
增强TEST和HCIEP目录下JSON文件的topology描述
基于enhance_topology_with_images.py，专门处理TEST和HCIEP目录
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, List, Optional, Union
import time
import httpx
from openai import OpenAI
import requests

def extract_think_content(text):
    """提取<think>标签内容"""
    import re
    match = re.search(r"<think>(.*?)</think>", text, re.DOTALL)
    if match:
        reasoning_content = match.group(1).strip()
        response_content = (text[:match.start()] + text[match.end():]).strip()
        return response_content, reasoning_content
    return text, None

class MultimodalLLMClient:
    def __init__(self, provider: str = "claude", api_key: str = None, base_url: str = None, model: str = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

        # 配置代理支持
        http_proxy = os.getenv("PES_HTTP_PROXY") or os.getenv("HTTP_PROXY")
        https_proxy = os.getenv("PES_HTTPS_PROXY") or os.getenv("HTTPS_PROXY")

        client_kwargs = {
            "api_key": self.api_key,
            "base_url": self.base_url
        }

        # 如果有代理设置，添加代理配置
        if http_proxy or https_proxy:
            proxy_url = https_proxy if https_proxy else http_proxy
            client_kwargs["http_client"] = httpx.Client(proxy=proxy_url)
            print(f"使用代理: {proxy_url}")
        
        if provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            self.base_url = base_url or "https://api.openai.com/v1"
            self.model = model or "gpt-4o"
            self.client = OpenAI(**client_kwargs)
            
        elif provider == "claude":
            self.api_key = api_key or "sk-GdmMOsWLYBdMwUBwJsaZGKOhM0k7cfuonqzTPvzLVVo1N4SL"
            self.model = model or "claude-sonnet-4-20250514"
            self.base_url = base_url or "https://chat.cloudapi.vip/v1/"
            self.client = OpenAI(**client_kwargs)
                
        elif provider == "gemini":
            self.api_key = api_key or os.getenv("GOOGLE_API_KEY") 
            self.model = model or "gemini-1.5-pro"
            self.base_url = "https://generativelanguage.googleapis.com/v1beta"
            
        else:
            raise ValueError(f"不支持的提供商: {provider}")
    
    def encode_image(self, image_path: str) -> str:
        """将图片编码为base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"图片编码失败 {image_path}: {e}")
            return None
    
    def analyze_topology_with_image(self, json_data: Dict, image_paths: List[str]) -> Optional[str]:
        """使用多模态模型分析网络拓扑图并增强描述"""
        
        if not image_paths:
            return None
        
        # 构建prompt - 针对TEST和HCIEP数据优化
        current_topology = json_data.get("topology", "")
        requirement = json_data.get("requirement", "")
        configs = json_data.get("configs", {})
        
        prompt = f"""你是一个网络工程专家，请根据提供的网络拓扑图，增强和完善以下网络拓扑描述。

当前拓扑描述：
{current_topology}

组网需求：
{requirement}

配置文件：
{configs}

请仔细分析图片中的网络拓扑结构，包括：
1. 设备类型和数量（路由器、交换机等）
2. 设备之间的连接关系和接口
3. 网络分段和VLAN信息
4. IP地址分配和子网划分
5. 协议配置区域（如OSPF区域、BGP AS等）
6. 特殊配置（如虚连接、汇聚链路等）

注意：如果图片中的信息杂糅，无法判断接口地址或连接情况，请参考配置文件中对应设备的具体配置，确保拓扑信息的正确性。

基于图片内容，提供一个更详细、准确的网络拓扑描述。保持专业性和准确性，重点描述网络的逻辑结构和物理连接。

请直接返回增强后的拓扑描述，不要添加任何解释文字(请保证返回的拓扑描述的正确性和简洁性)："""

        try:
            if self.provider == "openai":
                return self._call_openai_vision(prompt, image_paths)
            elif self.provider == "claude":
                return self._call_openai_vision(prompt, image_paths)
            elif self.provider == "gemini":
                return self._call_gemini_vision(prompt, image_paths)
        except Exception as e:
            print(f"多模态调用失败: {e}")
            return None
    
    def _call_openai_vision(self, prompt: str, image_paths: List[str]) -> Optional[str]:
        """调用OpenAI Vision API"""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # 添加图片
        for image_path in image_paths[:3]:  # 限制最多3张图片
            base64_image = self.encode_image(image_path)
            if base64_image:
                messages[0]["content"].append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        "detail": "high"
                    }
                })
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    
    def _call_gemini_vision(self, prompt: str, image_paths: List[str]) -> Optional[str]:
        """调用Gemini Vision API"""
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        parts = [{"text": prompt}]
        
        # 添加图片
        for image_path in image_paths[:3]:  # 限制最多3张图片
            base64_image = self.encode_image(image_path)
            if base64_image:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": base64_image
                    }
                })
        
        data = {
            "contents": [{"parts": parts}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1500
            }
        }
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            if "candidates" in result and result["candidates"]:
                return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        else:
            print(f"Gemini API调用失败: {response.status_code} - {response.text}")
        
        return None

class TestHciepTopologyEnhancer:
    def __init__(self, provider: str = "claude", api_key: str = None, base_url: str = None, model: str = None):
        self.llm_client = MultimodalLLMClient(
            provider=provider,
            api_key=api_key,
            base_url=base_url,
            model=model
        )
        self.base_dir = Path("datasets/Huawei")
        
    def find_corresponding_image(self, json_path: Path) -> List[str]:
        """查找对应的图片文件"""
        image_paths = []
        
        # 获取JSON文件的基本名称（不含扩展名）
        json_name = json_path.stem
        
        # 根据不同目录查找图片
        if "TEST" in str(json_path):
            # TEST目录的图片在img/子目录下
            img_dir = json_path.parent / "img"
            possible_image = img_dir / f"{json_name}.png"
        elif "HCIEP" in str(json_path):
            # HCIEP目录的图片在imgs/子目录下
            img_dir = json_path.parent / "imgs"
            possible_image = img_dir / f"{json_name}.png"
        else:
            return image_paths
        
        # 检查图片是否存在
        if possible_image.exists():
            image_paths.append(str(possible_image))
        else:
            print(f"⚠️  未找到对应图片: {possible_image}")
        
        return image_paths
        
    def enhance_single_json(self, json_path: Path) -> bool:
        """增强单个JSON文件的拓扑描述"""
        try:
            # 读取JSON文件
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 查找对应的图片文件
            image_paths = self.find_corresponding_image(json_path)
            
            if not image_paths:
                print(f"⏭️  {json_path.name}: 没有找到对应图片，跳过增强")
                return True
            
            print(f"🖼️  {json_path.name}: 分析 {len(image_paths)} 张图片...")
            
            # 调用多模态模型增强拓扑描述
            enhanced_topology = self.llm_client.analyze_topology_with_image(data, image_paths)
            
            if enhanced_topology and enhanced_topology != data.get("topology", ""):
                # 保存原始描述
                if "topology" in data and data["topology"]:
                    data["topology_original"] = data["topology"]
                
                # 更新增强后的描述
                data["topology"] = enhanced_topology
                
                # 保存更新后的JSON
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"✅ {json_path.name}: 拓扑描述已增强")
                print(f"   原始长度: {len(data.get('topology_original', ''))} 字符")
                print(f"   增强长度: {len(enhanced_topology)} 字符")
                return True
            else:
                print(f"⚠️  {json_path.name}: 无法生成增强描述或内容相同")
                return False
                
        except Exception as e:
            print(f"❌ {json_path.name}: 处理失败 - {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def enhance_directory(self, json_dir: Path, limit: int = None):
        """增强整个目录中的JSON文件"""
        json_files = list(json_dir.glob("**/*.json"))
        
        # 过滤掉不相关的JSON文件
        json_files = [f for f in json_files if not f.name.startswith("_")]
        
        if limit:
            json_files = json_files[:limit]
        
        enhanced_count = 0
        failed_count = 0
        
        print(f"🚀 开始增强 {len(json_files)} 个JSON文件的拓扑描述")
        print("=" * 60)
        
        for json_file in json_files:
            success = self.enhance_single_json(json_file)
            if success:
                enhanced_count += 1
            else:
                failed_count += 1
            
            # 添加延迟避免API限制
            time.sleep(2)
        
        print("=" * 60)
        print(f"🎉 增强完成!")
        print(f"   成功: {enhanced_count} 个文件")
        print(f"   失败: {failed_count} 个文件")
    
    def enhance_both_directories(self, limit: int = None):
        """增强TEST和HCIEP两个目录"""
        test_dir = self.base_dir / "TEST"
        hciep_dir = self.base_dir / "HCIEP"
        
        directories = []
        if test_dir.exists():
            directories.append(("TEST", test_dir))
        if hciep_dir.exists():
            directories.append(("HCIEP", hciep_dir))
        
        if not directories:
            print("❌ 未找到TEST或HCIEP目录")
            return
        
        for dir_name, dir_path in directories:
            print(f"\n🔄 处理 {dir_name} 目录...")
            print("=" * 50)
            self.enhance_directory(dir_path, limit)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="增强TEST和HCIEP目录下JSON文件的拓扑描述")
    parser.add_argument("--provider", choices=["openai", "claude", "gemini"], 
                       default="claude", help="多模态LLM提供商")
    parser.add_argument("--api-key", help="API密钥", default="sk-GdmMOsWLYBdMwUBwJsaZGKOhM0k7cfuonqzTPvzLVVo1N4SL")
    parser.add_argument("--base-url", help="API基础URL（可选）", default="https://chat.cloudapi.vip/v1/")
    parser.add_argument("--model", help="使用的模型", default="claude-sonnet-4-20250514")
    parser.add_argument("--limit", type=int, help="限制处理的文件数量（用于测试）")
    parser.add_argument("--single-file", help="处理单个文件（测试用）")
    parser.add_argument("--directory", choices=["TEST", "HCIEP", "both"], default="both",
                       help="选择要处理的目录")
    
    args = parser.parse_args()
    
    # 根据提供商设置默认值
    if args.provider == "openai":
        default_api_key_env = "OPENAI_API_KEY"
        default_model = "gpt-4o"
        api_description = "OpenAI API密钥"
    elif args.provider == "claude":
        default_api_key_env = "ANTHROPIC_API_KEY"
        default_model = "claude-sonnet-4-20250514"
        api_description = "Anthropic API密钥"
    elif args.provider == "gemini":
        default_api_key_env = "GOOGLE_API_KEY"
        default_model = "gemini-1.5-pro"
        api_description = "Google API密钥"
    
    # 获取API密钥
    api_key = args.api_key or os.getenv(default_api_key_env)
    if not api_key:
        print(f"❌ 请提供{api_description}")
        print(f"方法1: 设置环境变量 {default_api_key_env}")
        print(f"方法2: 使用 --api-key 参数")
        return
    
    # 获取模型
    model = args.model or default_model
    
    print(f"🤖 使用{args.provider}提供商")
    print(f"📱 模型: {model}")
    if args.base_url:
        print(f"🌐 API地址: {args.base_url}")
    
    # 创建增强器
    enhancer = TestHciepTopologyEnhancer(
        provider=args.provider,
        api_key=api_key,
        base_url=args.base_url,
        model=model
    )
    
    # 处理文件
    if args.single_file:
        # 单文件测试
        json_path = Path(args.single_file)
        if json_path.exists():
            enhancer.enhance_single_json(json_path)
        else:
            print(f"❌ 文件不存在: {json_path}")
    else:
        # 批量处理
        if args.directory == "both":
            enhancer.enhance_both_directories(limit=args.limit)
        elif args.directory == "TEST":
            test_dir = Path("datasets/Huawei/TEST")
            if test_dir.exists():
                enhancer.enhance_directory(test_dir, limit=args.limit)
            else:
                print(f"❌ 目录不存在: {test_dir}")
        elif args.directory == "HCIEP":
            hciep_dir = Path("datasets/Huawei/HCIEP")
            if hciep_dir.exists():
                enhancer.enhance_directory(hciep_dir, limit=args.limit)
            else:
                print(f"❌ 目录不存在: {hciep_dir}")

if __name__ == "__main__":
    main()