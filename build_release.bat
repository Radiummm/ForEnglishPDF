@echo off
chcp 65001 > nul
echo ========================================
echo        PDF Learning Assistant - Build
echo ========================================
echo.

REM 1. Clean cache files
echo [1/4] Cleaning cache files...
if exist "src\__pycache__" rmdir /s /q "src\__pycache__" 2>nul
if exist "src\services\__pycache__" rmdir /s /q "src\services\__pycache__" 2>nul
if exist "src\utils\__pycache__" rmdir /s /q "src\utils\__pycache__" 2>nul
if exist "pages\__pycache__" rmdir /s /q "pages\__pycache__" 2>nul
if exist ".pytest_cache" rmdir /s /q ".pytest_cache" 2>nul
del /q *.pyc 2>nul
del /q *.log 2>nul

REM 2. Create directories
echo [2/4] Preparing directory structure...
if not exist "data\uploads" mkdir "data\uploads"
if not exist "data\sample" mkdir "data\sample"
echo. > "data\uploads\.gitkeep"

REM 3. Create example config
echo [3/4] Creating config template...
if not exist ".env.example" (
    echo # PDF Learning Assistant Config > .env.example
    echo USE_SILICONFLOW=true >> .env.example
    echo SILICONFLOW_API_KEY=your_api_key_here >> .env.example
    echo SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct >> .env.example
)

REM 4. Simple zip creation using PowerShell
echo [4/4] Creating package...
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set mydate=%%c%%a%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set mytime=%%a%%b
set timestamp=%mydate%_%mytime%
set zipname=pdf-assistant_v%timestamp%.zip

powershell -Command "Compress-Archive -Path . -DestinationPath '%zipname%' -Exclude '.venv','*.env','data/uploads/*','.git*','*.zip','__pycache__*' -Force"

if exist "%zipname%" (
    echo.
    echo ========================================
    echo Build Complete!
    echo ========================================
    echo Package: %zipname%
    echo.
    echo User Instructions:
    echo   1. Extract zip file
    echo   2. Run install.bat
    echo   3. Edit .env file with API key
    echo   4. Run start.bat
) else (
    echo ERROR: Failed to create package
)

echo.
pause