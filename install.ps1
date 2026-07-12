# ZipLoot Windows 1-Click Image Translator Setup
try {
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host "[ZipLoot] Image Translator Installer" -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Green

    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

    # Create project folder locally in the user's CURRENT directory
    $projectFolder = Join-Path $pwd "unlimited-image-translator-project"
    if (Test-Path $projectFolder) {
        Write-Host "[WARN] Folder 'unlimited-image-translator-project' already exists." -ForegroundColor Yellow
    } else {
        New-Item -ItemType Directory -Path $projectFolder -ErrorAction SilentlyContinue | Out-Null
    }

    # Copy template files
    Copy-Item -Path "$scriptDir\\index.html" -Destination "$projectFolder\\index.html" -Force
    Copy-Item -Path "$scriptDir\\vercel.json" -Destination "$projectFolder\\vercel.json" -Force
    Copy-Item -Path "$scriptDir\\package.json" -Destination "$projectFolder\\package.json" -Force

    Write-Host "[SUCCESS] Local files generated!" -ForegroundColor Green
    Write-Host "--------------------------------------------------------" -ForegroundColor Green
    Write-Host "To host this on Vercel for free ($0):" -ForegroundColor Yellow
    Write-Host "1. Create a free account on Vercel." -ForegroundColor Yellow
    Write-Host "2. Link your GitHub account." -ForegroundColor Yellow
    Write-Host "3. Push the files in $projectFolder to your GitHub repo." -ForegroundColor Yellow
    Write-Host "4. Import the repo to Vercel. It deploys instantly as a static website!" -ForegroundColor Green
    Write-Host "--------------------------------------------------------" -ForegroundColor Green
    
    Read-Host "`nSetup completed. Press Enter to exit..."
} catch {
    Write-Host "[ERROR] An unexpected error occurred: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
}
