#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Bot Telegram Sipenduduk Deployment ===${NC}\n"

# Check Python
if ! command -v python3 &> /dev/null
then
    echo "Python 3 tidak ditemukan. Silakan install Python 3 terlebih dahulu."
    exit 1
fi

echo -e "${GREEN}✓ Python 3 ditemukan${NC}"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Membuat virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Install dependencies...${NC}"
pip install -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}File .env tidak ditemukan${NC}"
    echo "Buat file .env dari template:"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Edit file .env dan masukkan TELEGRAM_BOT_TOKEN${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Setup selesai${NC}"
echo -e "${GREEN}Jalankan bot dengan: python bot.py${NC}"
