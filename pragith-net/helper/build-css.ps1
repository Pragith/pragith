$ErrorActionPreference = "Stop"

$TAILWIND_DIR = ".tailwind"
$TAILWIND_EXE = "$TAILWIND_DIR\tailwindcss.exe"
$URL = "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-windows-x64.exe"

if (-not (Test-Path $TAILWIND_DIR)) {
    New-Item -ItemType Directory -Path $TAILWIND_DIR | Out-Null
}

if (-not (Test-Path $TAILWIND_EXE)) {
    Write-Host "Downloading Tailwind CSS v3.4.1..."
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $URL -OutFile $TAILWIND_EXE -UseBasicParsing
    Write-Host "Download complete."
} else {
    Write-Host "Tailwind binary already exists."
}

Write-Host "Building CSS..."
& $TAILWIND_EXE -i .\app\static\css\input.css -o .\app\static\css\style.min.css --minify -c .\tailwind.config.js
Write-Host "CSS built successfully!"
$size = (Get-Item .\app\static\css\style.min.css).Length
Write-Host "Output: app/static/css/style.min.css ($size bytes)"
