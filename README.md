# 📚 PDF Study Assistant

一个基于 Streamlit 的智能 PDF 学习助手，帮助你快速理解英文课程资料和学术文档。

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特点

🔍 **智能解析** - 支持 PDF 文档上传与页面预览  
🤖 **AI 对话** - 逐页智能问答，深度理解文档内容  
🌐 **多模型支持** - SiliconFlow、Gemini、Claude、OpenAI 等多种 AI 模型  
💬 **中文输出** - 强制中文回答，适合中文用户  
⚡ **快速响应** - 优化的 API 调用和缓存机制  
🎨 **美观界面** - 专业的双栏布局，独立滚动设计

## 🎯 核心功能

### 📄 PDF 处理
- 拖拽上传 PDF 文件，自动解析与预览
- 高质量页面渲染，支持缩放查看
- OCR 文字识别，处理扫描版文档

### 🤖 AI 对话
- 逐页内容智能问答
- 支持自定义问题与深度讨论
- 多种 AI 模型可选，响应快速稳定

### 💡 智能功能
- 智能缓存，避免重复请求
- 中文强制输出，本地化体验
- 专业 UI 设计，操作简单直观

## 🚀 快速开始

### 系统要求
- Python 3.9+
- Windows 用户需安装 [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

### 一键安装（推荐）
```bash
# Windows 用户
./install.bat

# Linux/Mac 用户  
./install.sh
```

### 手动安装
```bash
# 1. 克隆项目
git clone https://github.com/your-username/pdf-study-assistant.git
cd pdf-study-assistant

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或者
.venv\Scripts\activate     # Windows

# 3. 安装依赖
pip install -r requirements.txt
```

### 配置与启动
```bash
# 1. 复制配置文件
cp .env.example .env

# 2. 编辑 .env 文件，填入你的 API 密钥

# 3. 启动应用
streamlit run app.py
# 或者使用启动脚本
./start.bat  # Windows
./start.sh   # Linux/Mac
```

## ⚙️ 配置说明

### 环境变量配置
编辑 `.env` 文件，选择你的 AI 服务商：

```env
# SiliconFlow（推荐，国内访问稳定）
SILICONFLOW_API_KEY=your_siliconflow_api_key
SILICONFLOW_MODEL=Qwen/Qwen2.5-72B-Instruct

# 或者使用其他服务商
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
CLAUDE_API_KEY=your_claude_api_key

# 选择服务商域名（可选）
SELECTED_DOMAIN=SiliconFlow  # 或 OpenAI, Gemini, Claude
```

### 支持的 AI 服务商

| 服务商 | 优势 | 获取方式 |
|--------|------|----------|
| **SiliconFlow** | 国内访问稳定，速度快 | [siliconflow.cn](https://siliconflow.cn) |
| **OpenAI** | 模型质量高 | [platform.openai.com](https://platform.openai.com) |
| **Google Gemini** | 免费额度大 | [ai.google.dev](https://ai.google.dev) |
| **Anthropic Claude** | 安全性好 | [console.anthropic.com](https://console.anthropic.com) |

## 📁 项目结构

```
📦 pdf-study-assistant
├── 📄 app.py                    # 应用主入口
├── 📁 pages/                    # Streamlit 页面
│   ├── 01_上传与配置.py         # PDF 上传页面
│   └── 02_阅读与对话.py         # 阅读与对话页面
├── 📁 src/                      # 核心源码
│   ├── config.py                # 配置管理
│   ├── prompts.py               # AI 提示词模板
│   ├── services/
│   │   └── llm_client.py        # AI 服务客户端
│   └── utils/
│       ├── cache_utils.py       # 缓存工具
│       └── pdf_utils.py         # PDF 处理工具
├── 📁 data/                     # 数据目录
├── 🐳 Dockerfile               # Docker 配置
├── 🐳 docker-compose.yml       # Docker Compose
└── 📋 requirements.txt          # Python 依赖
```

## 🐳 Docker 部署

```bash
# 1. 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 2. 启动服务
docker-compose up -d

# 3. 访问应用
# http://localhost:8501
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的 Web 应用框架
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF 处理库
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - 文字识别引擎

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
