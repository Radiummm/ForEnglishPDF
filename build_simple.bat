@echo off
chcp 65001 > nul
echo ========================================
echo        PDF Learning Assistant - Build
echo ========================================
echo.

REM 1. Clean cache
echo [1/4] Cleaning cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /q /s *.pyc 2>nul

REM 2. Create directories
echo [2/4] Preparing directories...
if not exist "data\uploads" mkdir "data\uploads"
echo. > "data\uploads\.gitkeep"

REM 3. Create example config
echo [3/4] Creating config...
(
echo USE_SILICONFLOW=true
echo SILICONFLOW_API_KEY=your_api_key_here  
echo SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct
) > .env.example

REM 4. Create temp directory for packaging
echo [4/4] Creating package...
set timestamp=%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%
set timestamp=%timestamp: =0%
set zipname=pdf-assistant_v%timestamp%.zip
set tempdir=temp_package_%timestamp%

REM Create temp directory and copy files
mkdir "%tempdir%" 2>nul
xcopy /E /I /Q . "%tempdir%" /EXCLUDE:exclude.txt 2>nul

REM Create exclude list
(
echo .venv\
echo .env
echo *.zip
echo .git\
echo __pycache__\
echo data\uploads\
echo %tempdir%\
) > exclude.txt

REM Copy files excluding sensitive ones
for %%f in (*.py *.txt *.md *.bat *.sh *.yml *.dockerfile) do copy "%%f" "%tempdir%\" >nul 2>&1
xcopy /E /I /Q src "%tempdir%\src\" >nul 2>&1  
xcopy /E /I /Q pages "%tempdir%\pages\" >nul 2>&1
xcopy /E /I /Q tests "%tempdir%\tests\" >nul 2>&1
mkdir "%tempdir%\data\uploads" >nul 2>&1
echo. > "%tempdir%\data\uploads\.gitkeep"

REM Create zip
powershell -Command "Compress-Archive -Path '%tempdir%\*' -DestinationPath '%zipname%' -Force"

REM Cleanup
rd /s /q "%tempdir%" 2>nul
del exclude.txt 2>nul

if exist "%zipname%" (
    echo.
    echo ========================================
    echo Build Complete!
    echo ========================================
    echo Package: %zipname%
    for %%A in ("%zipname%") do echo Size: %%~zA bytes
    echo.
    echo User Instructions:
    echo 1. Extract: %zipname%
    echo 2. Run: install.bat  
    echo 3. Edit: .env file
    echo 4. Run: start.bat
    echo.
) else (
    echo ERROR: Failed to create package
)

pause