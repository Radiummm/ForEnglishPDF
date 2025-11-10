@echo off
echo Creating PDF Assistant package...

REM Clean cache  
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul

REM Create config
echo USE_SILICONFLOW=true > .env.example
echo SILICONFLOW_API_KEY=your_api_key_here >> .env.example
echo SILICONFLOW_MODEL_NAME=Qwen/Qwen3-Omni-30B-A3B-Instruct >> .env.example

REM Quick package (skip problem files)
set tempdir=pkg_temp
if exist %tempdir% rd /s /q %tempdir%
mkdir %tempdir%

REM Copy core files
copy *.py %tempdir%\ >nul
copy *.txt %tempdir%\ >nul
copy *.md %tempdir%\ >nul  
copy *.bat %tempdir%\ >nul
copy *.yml %tempdir%\ >nul
copy Dockerfile %tempdir%\ >nul
copy .env.example %tempdir%\ >nul

REM Copy source
xcopy /E /I src %tempdir%\src\ >nul
xcopy /E /I pages %tempdir%\pages\ >nul

REM Create empty data structure  
mkdir %tempdir%\data\uploads
mkdir %tempdir%\data\sample
echo. > %tempdir%\data\uploads\.gitkeep

REM Package
powershell -Command "Compress-Archive -Path '%tempdir%\*' -DestinationPath 'pdf-assistant-ready.zip' -Force"

REM Cleanup
rd /s /q %tempdir%

echo DONE! Created: pdf-assistant-ready.zip
dir pdf-assistant-ready.zip
pause