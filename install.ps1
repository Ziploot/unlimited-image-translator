# =================================================================
#  ZipLoot AI Watermark Remover — Windows Single File Installer
# =================================================================

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Write-Host "🚀 Starting ZipLoot Watermark AI Setup..." -ForegroundColor Cyan

# Find Python executable on Windows
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

# 2. Start Python Server
Write-Host "🧠 Starting AI Server on http://localhost:8080 ..." -ForegroundColor Green
[Environment]::SetEnvironmentVariable('PYTHONIOENCODING', 'utf-8', 'Process')
& $pythonPath video_web_app.py
