#!/bin/bash
echo "========================================"
echo "       PDF学习助手 - 打包发布脚本"
echo "========================================"
echo

# 1. 清理临时文件和缓存
echo "[1/5] 清理缓存文件..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

# 2. 创建示例配置文件
echo "[2/5] 创建配置模板..."
if [ ! -f ".env.example" ]; then
cat > .env.example << 'EOF'
# PDF学习助手配置文件
# 推荐使用硅基流动API，国内访问稳定

USE_SILICONFLOW=true
SILICONFLOW_API_KEY=your_api_key_here
SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct

# 其他可选配置
GOOGLE_API_KEY=
OPENAI_API_KEY=
CLAUDE_API_KEY=
EOF
fi

# 3. 创建目录保持文件
echo "[3/5] 准备目录结构..."
mkdir -p data/uploads data/sample
touch data/uploads/.gitkeep
if [ ! -f "data/sample/README.txt" ]; then
    echo "请将示例PDF文件放在此目录" > data/sample/README.txt
fi

# 4. 创建发布说明文件
echo "[4/5] 生成使用说明..."
cat > 快速开始.md << 'EOF'
# PDF学习助手 - 快速开始指南

## 安装步骤
1. 运行 `bash install.sh` 进行自动安装
2. 复制 `.env.example` 为 `.env`
3. 编辑 `.env` 文件，添加你的API密钥
4. 运行 `bash start.sh` 启动应用

## API密钥获取
- 硅基流动(推荐): https://cloud.siliconflow.cn/
- Google Gemini: https://aistudio.google.com/
- OpenAI: https://platform.openai.com/

## Docker 部署 (可选)
```bash
cp .env.example .env
# 编辑 .env 文件
docker-compose up -d
```

## 技术支持
如有问题，请查看 README_DEPLOY.md 详细文档
EOF

# 5. 打包文件
echo "[5/5] 正在打包..."
timestamp=$(date +"%Y%m%d_%H%M")
zipname="pdf-assistant_v${timestamp}.tar.gz"

tar -czf "$zipname" \
    --exclude='.venv' \
    --exclude='.env' \
    --exclude='data/uploads/*' \
    --exclude='.git' \
    --exclude='*.tar.gz' \
    --exclude='*.zip' \
    --exclude='__pycache__' \
    --exclude='node_modules' \
    .

filesize=$(du -h "$zipname" | cut -f1)

echo
echo "========================================"
echo "打包完成！"
echo "========================================"
echo
echo "打包文件: $zipname"
echo "文件大小: $filesize"
echo
echo "打包内容包括:"
echo "  ✓ 应用程序源代码"
echo "  ✓ 依赖配置文件"
echo "  ✓ 安装和启动脚本"
echo "  ✓ Docker配置文件"
echo "  ✓ 使用说明文档"
echo
echo "排除内容:"
echo "  ✗ 虚拟环境(.venv)"
echo "  ✗ 个人配置(.env)"
echo "  ✗ 上传文件(data/uploads/*)"
echo "  ✗ Git历史(.git)"
echo "  ✗ Python缓存(__pycache__)"
echo
echo "用户使用步骤:"
echo "  1. 解压文件: tar -xzf $zipname"
echo "  2. 运行: bash install.sh"
echo "  3. 编辑 .env 添加API密钥"
echo "  4. 运行: bash start.sh"
echo