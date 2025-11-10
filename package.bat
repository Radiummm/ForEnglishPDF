@echo off
echo ========================================
echo        PDF Assistant - Package Build
echo ========================================

REM Clean cache
echo [1/3] Cleaning...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /q /s *.pyc 2>nul

REM Create config template
echo [2/3] Config...
echo USE_SILICONFLOW=true > .env.example
echo SILICONFLOW_API_KEY=your_api_key_here >> .env.example
echo SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct >> .env.example

REM Package (manual file selection)
echo [3/3] Packaging...
set zipname=pdf-assistant.zip
if exist %zipname% del %zipname%

REM Use 7zip if available, otherwise PowerShell
where 7z >nul 2>&1
if %errorlevel% == 0 (
    7z a %zipname% * -x!.venv -x!.env -x!"data\uploads\*" -x!.git -x!*.zip
) else (
    REM PowerShell method without exclude
    powershell -Command "$files = Get-ChildItem -Recurse | Where {$_.FullName -notlike '*\.venv\*' -and $_.FullName -notlike '*\.env*' -and $_.FullName -notlike '*\data\uploads\*' -and $_.FullName -notlike '*\.git\*' -and $_.Extension -ne '.zip'}; Compress-Archive -Path $files.FullName -DestinationPath '%zipname%' -Force"
)

if exist %zipname% (
    echo SUCCESS: Created %zipname%
    for %%A in (%zipname%) do echo Size: %%~zA bytes
    echo.
    echo Usage:
    echo 1. Extract %zipname%
    echo 2. Run install.bat
    echo 3. Edit .env file  
    echo 4. Run start.bat
) else (
    echo FAILED to create package
)

pause