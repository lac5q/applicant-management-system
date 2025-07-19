#!/bin/bash

# Recruiting System Startup Script
# Created: July 19, 2025
# Updated: July 19, 2025

echo "🚀 Starting Recruiting System..."
echo "=================================="

# Check if we're in the right directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run this script from the Recruiting project root directory"
    exit 1
fi

# Activate virtual environment
echo "🐍 Activating Python virtual environment..."
source .venv/bin/activate

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"

# Test Python environment
echo "🧪 Testing Python environment..."
python3 --version
pip3 list | grep -E "(requests|pandas|numpy|openai)" | head -5

# Test database connection
echo "🗄️ Testing database connection..."
python3 -c "
from scripts.applicant_database_manager import ApplicantDatabaseManager
db = ApplicantDatabaseManager()
print('✅ Database connection successful')
"

# Test MCP connection
echo "🔧 Testing MCP connection..."
python3 scripts/test_mcp_connection.py

# Start Next.js development server
echo "🚀 Starting Next.js development server..."
echo "📱 Next.js will be available at: http://localhost:3000"
echo "💡 Press Ctrl+C to stop the server"
echo ""

cd nextjs-app
npm run dev 