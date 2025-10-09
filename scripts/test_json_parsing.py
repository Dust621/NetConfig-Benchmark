#!/usr/bin/env python3
"""
测试JSON解析修复功能
"""

import json
from integrate_huawei_data_llm import HuaweiDataLLMIntegrator

def test_json_parsing():
    """测试JSON解析修复功能"""
    
    print("🧪 测试JSON解析修复功能")
    print("=" * 40)
    
    integrator = HuaweiDataLLMIntegrator()
    
    # 测试案例1：markdown包装的JSON（你遇到的情况）
    test_case_1 = '''```json
{
  "topology": "DeviceA 和 DeviceB 作为ABR，连接区域0、区域1和区域2。DeviceC 和 DeviceE 位于区域1。DeviceD 和 DeviceF 位于区域2。",
  "requirement": "所有的路由器都运行OSPF，并将整个自治系统划分为3个区域。其中，DeviceA和DeviceB作为ABR（区域边界路由器）来转发区域之间的路由。配置完成后，每台路由器都应学到自治系统内的所有网段的路由。",
  "steps": [
    "在各路由器上使能OSPF。",
    "指定不同区域内的网段。",
    "配置OSPF区域的密文验证模式。"
  ],
  "configs": {
    "DeviceA": "#\\nsysname DeviceA\\n#\\nrouter id 1.1.1.1\\n#\\ninterface GigabitEthernet1/0/0\\n undo shutdown\\n ip address 192.168.0.1 255.255.255.0\\n#\\ninterface GigabitEthernet2/0/0\\n undo shutdown\\n ip address 192.168.1.1 255.255.255.0\\n#\\nospf\\n area 0.0.0.0\\n  network 192.168.0.0 0.0.0.255\\n  authentication-mode hmac-sha256 1 cipher YsHsjx_\\n area 0.0.0.1\\n  network 192.168.1.0 0.0.0.255\\n#\\nreturn",
    "DeviceB": "#\\nsysname DeviceB\\n#\\nrouter id 2.2.2.2\\n#\\ninterface GigabitEthernet1/0/0\\n undo shutdown\\n ip address 192.168.0.2 255.255.255.0\\n#\\ninterface GigabitEthernet2/0/0\\n undo shutdown\\n ip address 192.168.2.1 255.255.255.0\\n#\\nospf\\n area 0.0.0.0\\n  network 192.168.0.0 0.0.0.255\\n  authentication-mode hmac-sha256 1 cipher YsHsjx_\\n area 0.0.0.2\\n  network 192.168.2.0 0.0.0.255\\n#\\nreturn"
  },
  "related_images": [
    "图1-42 配置 OSPF 基本功能组网图.png"
  ]
}
```'''
    
    print("测试案例1: Markdown包装的JSON")
    result_1 = integrator.parse_llm_response(test_case_1)
    if result_1:
        print("✅ 解析成功!")
        print(f"   拓扑: {result_1['topology'][:50]}...")
        print(f"   设备数: {len(result_1['configs'])}")
        print(f"   步骤数: {len(result_1['steps'])}")
        print(f"   图片数: {len(result_1.get('related_images', []))}")
    else:
        print("❌ 解析失败")
    
    print("\\n" + "=" * 40)
    
    # 测试案例2：纯JSON
    test_case_2 = '''{
  "topology": "简单的网络拓扑",
  "requirement": "配置基本OSPF",
  "steps": ["步骤1", "步骤2"],
  "configs": {"DeviceA": "config1"},
  "related_images": []
}'''
    
    print("测试案例2: 纯JSON")
    result_2 = integrator.parse_llm_response(test_case_2)
    if result_2:
        print("✅ 解析成功!")
    else:
        print("❌ 解析失败")
    
    print("\\n" + "=" * 40)
    
    # 测试案例3：通用代码块格式
    test_case_3 = '''这是一个JSON响应：

```
{
  "topology": "测试拓扑",
  "requirement": "测试需求", 
  "steps": ["测试步骤"],
  "configs": {"DeviceA": "测试配置"},
  "related_images": ["test.png"]
}
```

以上是解析结果。'''
    
    print("测试案例3: 通用代码块")
    result_3 = integrator.parse_llm_response(test_case_3)
    if result_3:
        print("✅ 解析成功!")
    else:
        print("❌ 解析失败")
    
    print("\\n" + "=" * 40)
    
    # 测试案例4：格式错误的JSON
    test_case_4 = '''```json
{
  "topology": "错误的JSON",
  "requirement": "缺少逗号"
  "steps": ["错误格式"],
  "configs": {},
  "related_images": []
}
```'''
    
    print("测试案例4: 格式错误的JSON")
    result_4 = integrator.parse_llm_response(test_case_4)
    if result_4:
        print("✅ 解析成功!")
    else:
        print("❌ 解析失败（预期结果）")
    
    print("\\n🎉 JSON解析测试完成")

if __name__ == "__main__":
    test_json_parsing()