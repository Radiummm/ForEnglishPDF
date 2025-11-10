# PDF学习助手

一个基于AI的PDF文档解释工具，帮助快速理解英文技术文档。

## 功能特点

- 📄 **PDF上传与预览** - 支持PDF文件上传和页面预览
- 🤖 **AI智能解释** - 点击页面按钮，AI自动解释该页内容
- 💬 **对话交互** - 支持与AI进行自然语言对话
- 🚀 **多模型支持** - 支持Gemini、Claude、Qwen等多种AI模型
- 🔄 **独立滚动** - 左侧聊天和右侧PDF独立滚动
- 🌐 **国内优化** - 支持硅基流动等国内API，访问稳定

## 快速开始

### 方法1: 一键安装（Windows推荐）

1. 下载项目文件
2. 双击运行 `install.bat`
3. 编辑 `.env` 文件，添加API密钥
4. 双击运行 `start.bat`

### 方法2: Docker部署

```bash
# 克隆项目
git clone <repository-url>
cd pdf-assistant

# 编辑配置
cp .env.example .env
# 编辑 .env 文件添加API密钥

# 启动服务
docker-compose up -d
```

### 方法3: 手动安装

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate.bat  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置API
cp .env.example .env
# 编辑 .env 文件

# 启动应用
streamlit run app.py
```

## API配置说明

推荐使用**硅基流动**，国内访问稳定，价格便宜：

1. 访问 [硅基流动](https://cloud.siliconflow.cn/)
2. 注册账号并获取API密钥
3. 在 `.env` 文件中配置：
   ```
   USE_SILICONFLOW=true
   SILICONFLOW_API_KEY=your_api_key_here
   SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct
   ```

## 支持的模型

- **硅基流动**: Qwen3系列、GLM-4、Llama等
- **Google Gemini**: Gemini 2.0 Flash
- **OpenAI**: GPT-4o系列
- **Anthropic Claude**: Claude 3.5 Sonnet
- **阿里通义**: Qwen系列
- **智谱AI**: GLM-4系列

## 使用说明

1. **上传PDF** - 选择领域并上传PDF文件
2. **页面解释** - 点击页面旁的"发送"按钮，AI解释该页内容
3. **自由对话** - 在聊天框中提问，与AI交流
4. **独立浏览** - 左右两栏可独立滚动，互不影响

## 项目结构

```
├── app.py                 # 主应用入口
├── requirements.txt       # Python依赖
├── .env.example          # 配置文件模板
├── install.bat           # Windows一键安装
├── start.bat             # Windows启动脚本
├── Dockerfile            # Docker容器配置
├── docker-compose.yml    # Docker编排配置
├── pages/                # Streamlit页面
│   ├── 01_上传与配置.py
│   └── 02_阅读与对话.py
├── src/                  # 源代码
│   ├── config.py         # 配置管理
│   ├── prompts.py        # 提示词模板
│   ├── services/         # 服务层
│   └── utils/            # 工具函数
├── data/                 # 数据目录
│   ├── uploads/          # 上传文件
│   └── sample/           # 示例文件
└── tests/                # 测试文件
```

## 常见问题

**Q: 网络连接失败怎么办？**
A: 推荐使用硅基流动API，国内访问稳定。

**Q: API调用失败？**  
A: 检查API密钥是否正确，余额是否充足。

**Q: 响应太慢？**
A: 可以切换到更小的模型或调整max_tokens参数。

**Q: OCR识别不准？**
A: 确保安装了tesseract-ocr，或上传文字清晰的PDF。

## 技术支持

如有问题，请提交Issue或联系开发者。

## 许可证

MIT License