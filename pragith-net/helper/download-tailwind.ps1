$ErrorActionPreference = "Stop"

$dir = ".tailwind"
$exe = "$dir\tailwindcss.exe"
$url = "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-windows-x64.exe"

if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
}

if (-not (Test-Path $exe)) {
    Write-Host "Downloading Tailwind CSS v3.4.1 standalone binary..."
    Invoke-WebRequest -Uri $url -OutFile $exe
    Write-Host "Downloaded successfully."
} else {
    Write-Host "Tailwind binary already exists."
}

Write-Host "Building CSS..."
& $exe -i .\app\static\css\input.css -o .\app\static\css\style.min.css --minify

if ($LASTEXITCODE -eq 0) {
    Write-Host "CSS built successfully."
} else {
    Write-Host "CSS build FAILED"
    exit 1
}
