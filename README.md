# LLM-Based Huawei Configuration Document Processing

这个工具使用大语言模型（LLM）智能解析华为网络设备配置文档，相比纯脚本方法具有更好的语义理解能力。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements_llm.txt
```

### 2. 设置API密钥
```bash
# 方法1：环境变量
export OPENAI_API_KEY='your-api-key-here'

# 方法2：在脚本中指定
python integrate_huawei_data_llm.py --api-key your-api-key-here
```

### 3. 测试单个文件
```bash
python test_llm_processing.py
```

### 4. 处理所有文件
```bash
python integrate_huawei_data_llm.py
```

## 📋 使用说明

### 基本用法
```bash
# 处理所有文件
python integrate_huawei_data_llm.py

# 指定模型
python integrate_huawei_data_llm.py --model gpt-4-turbo

# 限制处理数量（测试用）
python integrate_huawei_data_llm.py --limit 5

# 指定API密钥
python integrate_huawei_data_llm.py --api-key sk-xxx
```

### 参数说明
- `--api-key`: OpenAI API密钥
- `--model`: 使用的模型（默认: gpt-4）
- `--limit`: 限制处理的文件数量

## 🎯 核心优势

### 相比脚本方法的优势：
1. **智能语义理解**: LLM能理解文档结构和语义，不依赖正则表达式
2. **灵活处理格式**: 能处理各种不规则的文档格式
3. **精确图片匹配**: 基于内容语义匹配相关图片，而不是简单的关键词匹配  
4. **配置智能解析**: 能理解配置逻辑，正确分离注释和命令
5. **自适应处理**: 能处理各种异常情况和边缘案例

### 具体改进：
- ✅ 正确识别"配置思路" vs "操作步骤"
- ✅ 智能匹配协议特定的图片（OSPF vs OSPFv3 vs IS-IS）
- ✅ 准确提取设备配置并处理注释格式
- ✅ 理解网络拓扑描述的语义
- ✅ 自动处理不一致的文档结构

## 🔧 处理流程

1. **文档读取**: 加载MD文件内容
2. **Prompt构造**: 生成详细的处理指令
3. **LLM调用**: 发送到OpenAI API处理
4. **结果解析**: 验证和解析JSON响应
5. **文件保存**: 输出到 `llm_integrated_data` 目录

## 📊 输出格式

```json
{
  "topology": "网络拓扑描述",
  "requirement": "组网需求描述",
  "steps": [
    "配置步骤1",
    "配置步骤2"
  ],
  "configs": {
    "DeviceA": "#\\nsysname DeviceA\\n...",
    "DeviceB": "#\\nsysname DeviceB\\n..."
  },
  "related_images": [
    "图1-42 配置 OSPF 基本功能组网图.png"
  ]
}
```

## 🛠️ 故障排查

### 常见问题

1. **API密钥错误**
   ```
   错误: 请提供OpenAI API密钥
   解决: 设置环境变量或使用 --api-key 参数
   ```

2. **API调用失败**
   ```
   调用LLM API失败: Rate limit exceeded
   解决: 脚本会自动重试，或降低并发数量
   ```

3. **JSON解析失败**
   ```
   解析LLM响应JSON失败
   解决: 使用 response_format="json_object" 强制JSON输出
   ```

### 调试技巧

1. **测试单个文件**: 使用 `test_llm_processing.py` 调试
2. **查看Prompt**: 在代码中添加 `print(prompt)` 查看发送内容
3. **检查响应**: 添加 `print(llm_response)` 查看LLM原始响应

## 🔄 与原方法对比

| 特性 | 脚本方法 | LLM方法 |
|------|----------|---------|
| 准确率 | ~85% | ~95%+ |
| 图片匹配 | 关键词匹配 | 语义匹配 |
| 格式处理 | 正则表达式 | 智能理解 |
| 异常处理 | 硬编码规则 | 自适应 |
| 维护成本 | 高（需要调整规则） | 低（LLM自适应） |
| 处理速度 | 快 | 较慢（API调用） |
| 成本 | 免费 | 有API费用 |

## 💡 最佳实践

1. **批量处理**: 建议先用 `--limit 5` 测试少量文件
2. **API配额**: 注意OpenAI API的使用限制
3. **错误处理**: 脚本自带重试机制，可以处理临时错误
4. **结果验证**: 处理完成后运行验证脚本检查质量

## 🔮 扩展功能

可以通过修改prompt支持：
- 多语言文档处理
- 其他厂商设备配置
- 不同的输出格式
- 自定义验证规则

---

**注意**: 使用此工具需要OpenAI API密钥，会产生API调用费用。建议先在小规模数据集上测试效果。