#!/bin/bash
# [ZipLoot] Cloud Image Translator Setup
# ==============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0;37m' # No Color

clear
echo -e "${CYAN}==============================================${NC}"
echo -e "${CYAN}   ⚡ ZIPLOOT IMAGE TRANSLATOR & LENS SETUP${NC}"
echo -e "${CYAN}==============================================${NC}"
echo -e "${GREEN}   100% Client-Side | Free OCR | \$0 Hosting${NC}"
echo -e "${CYAN}==============================================${NC}"
echo

PROJECT_DIR="$(pwd)/unlimited-image-translator-project"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

echo -e "${BLUE}[INFO] Downloading project files from GitHub...${NC}"
BaseUrl="https://raw.githubusercontent.com/Ziploot/unlimited-image-translator/main"

curl -sL "$BaseUrl/index.html" -o index.html
curl -sL "$BaseUrl/vercel.json" -o vercel.json
curl -sL "$BaseUrl/package.json" -o package.json

echo -e "${GREEN}[SUCCESS] Local files configured successfully in: $PROJECT_DIR${NC}"
echo

echo -e "${CYAN}==============================================${NC}"
echo -e "${GREEN}⚡ OPTION 1: 1-Click Cloud Deployment (Vercel)${NC}"
echo -e "${CYAN}==============================================${NC}"
echo "Deploy to Vercel in 10 seconds for \$0:"
echo "1. Connect your GitHub/Vercel account and click Deploy."
echo

read -p "Do you want to open the 1-Click Vercel Deployment page now? (Y/N): " choice1
if [[ "$choice1" =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}[INFO] Opening deployment page...${NC}"
    URL="https://vercel.com/new/clone?repository-url=https://github.com/Ziploot/unlimited-image-translator"
    if command -v xdg-open &> /dev/null; then
        xdg-open "$URL"
    elif command -v open &> /dev/null; then
        open "$URL"
    else
        echo -e "${YELLOW}Please visit: $URL${NC}"
    fi
fi

echo
echo -e "${CYAN}==============================================${NC}"
echo -e "${GREEN}⚡ OPTION 2: Run Locally (Instant Browser Editor)${NC}"
echo -e "${CYAN}==============================================${NC}"
echo "Since the Image Translator is 100% client-side, you don't even need a server!"
echo "We can open the app directly in your default browser."
echo

read -p "Do you want to open the Translator locally in your browser now? (Y/N): " choice2
if [[ "$choice2" =~ ^[Yy]$ ]]; then
    echo -e "${GREEN}[INFO] Opening local index.html...${NC}"
    FILE_PATH="$(pwd)/index.html"
    if command -v xdg-open &> /dev/null; then
        xdg-open "$FILE_PATH"
    elif command -v open &> /dev/null; then
        open "$FILE_PATH"
    else
        echo -e "${YELLOW}Please open: $FILE_PATH${NC}"
    fi
fi

echo
echo -e "${CYAN}==============================================${NC}"
echo -e "${GREEN}🎉 INSTALLATION COMPLETE!${NC}"
echo -e "${CYAN}==============================================${NC}"
