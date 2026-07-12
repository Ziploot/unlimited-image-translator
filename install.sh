#!/bin/bash
# ZipLoot Linux/macOS 1-Click Image Translator Setup
echo "=============================================="
echo "⚡ ZipLoot - Linux/macOS Auto-Installer ⚡"
echo "=============================================="

# Create project folder locally
PROJECT_DIR="$(pwd)/unlimited-image-translator-project"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Download files from repository
echo "📥 Fetching files..."
curl -sL "https://raw.githubusercontent.com/Ziploot/unlimited-image-translator/main/index.html" -o index.html
curl -sL "https://raw.githubusercontent.com/Ziploot/unlimited-image-translator/main/vercel.json" -o vercel.json
curl -sL "https://raw.githubusercontent.com/Ziploot/unlimited-image-translator/main/package.json" -o package.json

echo "✅ Local files successfully configured!"
echo "Upload these files to your GitHub repository and link it to Vercel to host your private image translator for $0!"
