# 📚 ForEnglishPDF - PDF Study Assistant

为了更方便的理解英文PDF。一个基于 Streamlit 的智能 PDF 学习助手，帮助你快速理解英文课程资料和学术文档。

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
git clone https://github.com/Radiummm/ForEnglishPDF.git
cd ForEnglishPDF

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
