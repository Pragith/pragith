# Standalone Tailwind CSS build script for Windows (no Node/npm required)

$ErrorActionPreference = "Stop"

$TAILWIND_VERSION = "v3.4.1"
$PLATFORM = "windows-x64"
$BINARY_NAME = "tailwindcss-$PLATFORM.exe"
$BINARY_PATH = ".\.tailwind\$BINARY_NAME"

# Create .tailwind directory if it doesn't exist
if (-not (Test-Path ".\.tailwind")) {
    New-Item -ItemType Directory -Path ".\.tailwind" | Out-Null
}

# Download standalone Tailwind CLI if not present
if (-not (Test-Path $BINARY_PATH)) {
    Write-Host "Downloading Tailwind CSS standalone binary..." -ForegroundColor Yellow
    $url = "https://github.com/tailwindlabs/tailwindcss/releases/download/$TAILWIND_VERSION/$BINARY_NAME"
    Invoke-WebRequest -Uri $url -OutFile $BINARY_PATH
    Write-Host "✓ Tailwind CLI downloaded" -ForegroundColor Green
}

# Build CSS
Write-Host "Building CSS..." -ForegroundColor Yellow
& $BINARY_PATH -i .\app\static\css\input.css -o .\app\static\css\style.min.css --minify

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ CSS built successfully: app\static\css\style.min.css" -ForegroundColor Green
} else {
    Write-Host "✗ CSS build failed" -ForegroundColor Red
    exit 1
}
