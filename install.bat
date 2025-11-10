@echo off
echo ========================================
echo     PDF学习助手 - 自动安装脚本
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.9+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检查Python版本...
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if errorlevel 1 (
    echo [错误] Python版本过低，需要3.9+
    pause
    exit /b 1
)

echo [2/4] 创建虚拟环境...
if not exist .venv (
    python -m venv .venv
)

echo [3/4] 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo [4/4] 检查配置文件...
if not exist .env (
    echo [提示] 未找到.env文件，创建示例配置...
    copy .env.example .env
    echo 请编辑 .env 文件添加你的API密钥
)

echo.
echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 使用方法:
echo   1. 编辑 .env 文件，添加API密钥
echo   2. 运行: start.bat
echo.
pause