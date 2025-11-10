@echo off
echo ========================================
echo     PDF Assistant - Manual Package
echo ========================================

REM Clean cache first
echo [1/4] Cleaning cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

REM Create empty uploads folder
echo [2/4] Preparing folders...
if exist "data\uploads\*.pdf" (
    echo WARNING: Please close Streamlit app first!
    echo Files in uploads folder are in use.
    pause
    exit /b 1
)

REM Create config
echo [3/4] Creating config...
echo USE_SILICONFLOW=true > .env.example
echo SILICONFLOW_API_KEY=your_api_key_here >> .env.example  
echo SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct >> .env.example

REM Manual packaging - copy essential files only
echo [4/4] Manual packaging...
set zipname=pdf-assistant-manual.zip
if exist %zipname% del %zipname%

REM Create temporary folder
set tempdir=temp_package
if exist %tempdir% rd /s /q %tempdir%
mkdir %tempdir%

REM Copy essential files
copy *.py %tempdir%\ >nul 2>&1
copy *.txt %tempdir%\ >nul 2>&1  
copy *.md %tempdir%\ >nul 2>&1
copy *.bat %tempdir%\ >nul 2>&1
copy *.sh %tempdir%\ >nul 2>&1
copy *.yml %tempdir%\ >nul 2>&1
copy Dockerfile %tempdir%\ >nul 2>&1
copy .env.example %tempdir%\ >nul 2>&1

REM Copy folders
xcopy /E /I src %tempdir%\src\ >nul 2>&1
xcopy /E /I pages %tempdir%\pages\ >nul 2>&1
xcopy /E /I tests %tempdir%\tests\ >nul 2>&1

REM Create empty data structure
mkdir %tempdir%\data\uploads >nul 2>&1
mkdir %tempdir%\data\sample >nul 2>&1  
echo. > %tempdir%\data\uploads\.gitkeep
echo Sample PDF files go here > %tempdir%\data\sample\README.txt

REM Create zip
powershell -Command "Compress-Archive -Path '%tempdir%\*' -DestinationPath '%zipname%' -Force"

REM Cleanup
rd /s /q %tempdir%

if exist %zipname% (
    echo.
    echo ========================================
    echo SUCCESS!
    echo ========================================  
    echo Package: %zipname%
    for %%A in (%zipname%) do echo Size: %%~zA bytes
    echo.
    echo This package contains:
    echo - All source code
    echo - Installation scripts
    echo - Configuration templates
    echo - Empty upload folders
    echo.
    echo User instructions:
    echo 1. Extract %zipname%
    echo 2. Run install.bat
    echo 3. Edit .env with API key
    echo 4. Run start.bat
) else (
    echo FAILED to create package
)

echo.
pause