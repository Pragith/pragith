@echo off
cd /d "%~dp0"
echo Building Tailwind...
.\.tailwind\tailwindcss.exe -i .\app\static\css\input.css -o .\app\static\css\style.min.css --minify
if %errorlevel% neq 0 (
    echo Build failed with error code %errorlevel%
    exit /b %errorlevel%
)
echo Build complete.
