#!/bin/bash
# Simple run script for Tempo Contract Analyzer Bot

echo "🚀 Starting Tempo Contract Analyzer Bot..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please copy .env.example to .env and add your Discord token:"
    echo "   cp .env.example .env"
    echo "   nano .env  # or use your favorite editor"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Virtual environment not found. Creating..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run the bot
echo "✅ Dependencies installed"
echo "🤖 Starting bot..."
echo ""
python bot.py
