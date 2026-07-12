# [ZipLoot] Cloud Image Translator Setup
# ==============================================

Clear-Host
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   ⚡ ZIPLOOT IMAGE TRANSLATOR & LENS SETUP" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   100% Client-Side | Free OCR | \`$0 Hosting" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectFolder = Join-Path $pwd "unlimited-image-translator-project"

if (Test-Path $ProjectFolder) {
    Write-Host "[WARN] Folder 'unlimited-image-translator-project' already exists." -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Creating folder..." -ForegroundColor Blue
    New-Item -ItemType Directory -Path $ProjectFolder -Force | Out-Null
}

# Copy files
Copy-Item -Path "$scriptDir\index.html" -Destination "$ProjectFolder\index.html" -Force
Copy-Item -Path "$scriptDir\vercel.json" -Destination "$ProjectFolder\vercel.json" -Force
Copy-Item -Path "$scriptDir\package.json" -Destination "$ProjectFolder\package.json" -Force

Write-Host "[SUCCESS] Local files generated in: $ProjectFolder" -ForegroundColor Green
Write-Host

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "⚡ OPTION 1: 1-Click Cloud Deployment (Vercel)" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Deploy to Vercel in 10 seconds for \`$0:"
Write-Host "1. Connect your GitHub/Vercel account and click Deploy."
Write-Host

$choice1 = Read-Host "[INPUT] Do you want to open the 1-Click Vercel Deployment page now? (Y/N)"
if ($choice1 -eq 'y' -or $choice1 -eq 'Y') {
    Write-Host "[INFO] Opening deployment page..." -ForegroundColor Green
    Start-Process "https://vercel.com/new/clone?repository-url=https://github.com/Ziploot/unlimited-image-translator"
}

Write-Host
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "⚡ OPTION 2: Run Locally (Instant Browser Editor)" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Since the Image Translator is 100% client-side, you don't even need a server!"
Write-Host "We can open the app directly in your default browser."
Write-Host

$choice2 = Read-Host "[INPUT] Do you want to open the Translator locally in your browser now? (Y/N)"
if ($choice2 -eq 'y' -or $choice2 -eq 'Y') {
    Write-Host "[INFO] Opening local index.html..." -ForegroundColor Green
    $FullPath = Resolve-Path "$ProjectFolder\index.html"
    Start-Process $FullPath
}

Write-Host
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "🎉 INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
