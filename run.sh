#!/bin/bash

echo "🚀 Starting Task Manager API in development mode..."

if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source venv/bin/activate
fi

if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ .env file created. Please configure your settings."
fi

echo "🔄 Starting server..."
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info
