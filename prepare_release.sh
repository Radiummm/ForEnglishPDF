#!/bin/bash
# PDF学习助手发布准备脚本

echo "========================================="
echo "   PDF学习助手 - 发布准备"
echo "========================================="

# 1. 清理临时文件
echo "[1/5] 清理临时文件..."
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache .coverage htmlcov 2>/dev/null || true

# 2. 创建示例配置
echo "[2/5] 创建配置模板..."
if [ ! -f .env.example ]; then
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

# 3. 生成gitignore
echo "[3/5] 创建.gitignore..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
.venv/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# 项目特定
.env
data/uploads/*
!data/uploads/.gitkeep
data/sample/*
!data/sample/README.txt

# 日志
*.log

# 系统文件
.DS_Store
Thumbs.db
EOF

# 4. 创建空目录保持文件
echo "[4/5] 创建目录结构..."
mkdir -p data/uploads data/sample
touch data/uploads/.gitkeep

# 5. 验证项目结构
echo "[5/5] 验证项目结构..."
python -c "
import os
required_files = [
    'app.py', 'requirements.txt', '.env.example',
    'install.bat', 'start.bat', 'Dockerfile',
    'src/config.py', 'src/services/llm_client.py'
]
missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print(f'缺少文件: {missing}')
    exit(1)
print('✓ 项目结构完整')
"

echo ""
echo "========================================="
echo "发布准备完成！"
echo "========================================="
echo ""
echo "打包发布步骤:"
echo "1. zip -r pdf-assistant.zip . -x '*.git*' '.env' 'data/uploads/*'"
echo "2. 或使用: tar -czf pdf-assistant.tar.gz --exclude='.git' --exclude='.env' --exclude='data/uploads/*' ."
echo ""
echo "用户使用步骤:"
echo "1. 解压文件"
echo "2. 复制 .env.example 为 .env"
echo "3. 编辑 .env 添加API密钥" 
echo "4. Windows: 双击 install.bat 然后 start.bat"
echo "5. Linux/Mac: bash install.sh 然后 bash start.sh"