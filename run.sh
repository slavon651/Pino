#!/bin/bash

echo "🚀 Starting Pinterest Video Downloader..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo ""
echo "✨ Starting Flask server..."
echo "🌐 Open http://localhost:5000 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
