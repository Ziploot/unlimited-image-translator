# =================================================================
#  ZipLoot AI Watermark Remover — Windows A-to-Z Single File Installer
# =================================================================

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Write-Host "🚀 Starting A to Z ZipLoot Watermark AI VPS Setup..." -ForegroundColor Cyan

# Find Python executable on Windows VPS
$pythonPath = "python"
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    $possiblePaths = @(
        "$env:LocalAppData\Programs\Python\Python312\python.exe",
        "$env:LocalAppData\Programs\Python\Python311\python.exe",
        "$env:LocalAppData\Programs\Python\Python310\python.exe",
        "C:\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python310\python.exe",
        "C:\Program Files\Python312\python.exe",
        "C:\Program Files\Python311\python.exe"
    )
    foreach ($p in $possiblePaths) {
        if (Test-Path $p) {
            $pythonPath = $p
            Write-Host "✅ Python found at: $pythonPath" -ForegroundColor Green
            break
        }
    }
}

# 1. Install Dependencies using python -m pip
Write-Host "📦 Installing required Python packages..." -ForegroundColor Yellow
& $pythonPath -m pip install --upgrade pip
& $pythonPath -m pip install opencv-python numpy onnxruntime pillow imageio imageio-ffmpeg

# 2. Download cloudflared if missing
if (-not (Test-Path ".\cloudflared.exe")) {
    Write-Host "🌐 Downloading Cloudflare Tunnel (cloudflared.exe)..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile ".\cloudflared.exe"
        Write-Host "✅ Cloudflared Downloaded!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Skipping cloudflared download fallback." -ForegroundColor Yellow
    }
}

# 3. Start Python Server in Background
Write-Host "🧠 Starting AI Server on http://localhost:8080 ..." -ForegroundColor Green
$env:PYTHONIOENCODING="utf-8"
& $pythonPath video_web_app.py
