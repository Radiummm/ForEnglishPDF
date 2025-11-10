#!/bin/bash
echo "========================================="
echo "     PDF学习助手 - 自动安装脚本"
echo "========================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3，请先安装Python 3.9+"
    exit 1
fi

echo "[1/4] 检查Python版本..."
python3 -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)"
if [ $? -ne 0 ]; then
    echo "[错误] Python版本过低，需要3.9+"
    exit 1
fi

echo "[2/4] 创建虚拟环境..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "[3/4] 激活虚拟环境并安装依赖..."
source .venv/bin/activate
pip install -r requirements.txt

echo "[4/4] 检查配置文件..."
if [ ! -f ".env" ]; then
    echo "[提示] 未找到.env文件，创建示例配置..."
    cp .env.example .env
    echo "请编辑 .env 文件添加你的API密钥"
fi

echo ""
echo "========================================="
echo "安装完成！"
echo "========================================="
echo ""
echo "使用方法:"
echo "  1. 编辑 .env 文件，添加API密钥"
echo "  2. 运行: bash start.sh"