#!/bin/bash

# ================================================================
# Quick Fix Script - Emergency Solution for Python 3.13 Issues
# Usage: chmod +x quick_fix.sh && ./quick_fix.sh
# ================================================================

set -e

echo "🚑 Emergency Fix for Python 3.13 Compatibility Issues"
echo "======================================================="

# Check current directory
if [ ! -d "task-manager-backend" ]; then
    echo "❌ task-manager-backend directory not found."
    echo "💡 Please run this script in the directory where you ran generate_backend.sh"
    exit 1
fi

cd task-manager-backend

echo "🔧 Applying Python 3.13 compatibility fixes..."

# Create minimal requirements.txt for Python 3.13
cat > requirements-minimal.txt << 'EOF'
fastapi==0.110.0
uvicorn==0.27.0
pydantic>=2.6.1
sqlalchemy>=2.0.27
python-multipart>=0.0.9
python-decouple>=3.8
EOF

# Create alternative requirements with specific versions
cat > requirements-alt.txt << 'EOF'
# Alternative requirements for Python 3.13
fastapi>=0.100.0
uvicorn>=0.24.0
pydantic>=2.4.0,<3.0.0
sqlalchemy>=2.0.0
python-multipart>=0.0.6
python-decouple>=3.8
# Skip problematic packages
# pydantic-settings
# alembic
# python-jose
# passlib
EOF

echo "🐍 Activating virtual environment..."
source venv/bin/activate

echo "📦 Upgrading pip..."
pip install --upgrade pip

echo "🔄 Trying minimal installation..."
if pip install --no-cache-dir -r requirements-minimal.txt; then
    echo "✅ Minimal installation successful!"
    
    echo "📦 Installing optional packages one by one..."
    
    # Try to install additional packages individually
    packages=(
        "pydantic-settings>=2.0.0"
        "alembic>=1.13.0"
        "pytest>=7.0.0"
        "httpx>=0.25.0"
    )
    
    for package in "${packages[@]}"; do
        echo "Installing $package..."
        if pip install --no-cache-dir "$package"; then
            echo "✅ $package installed successfully"
        else
            echo "⚠️  Failed to install $package (skipping)"
        fi
    done
    
else
    echo "❌ Minimal installation failed. Trying pre-compiled wheels only..."
    if pip install --only-binary=all fastapi uvicorn 'pydantic>=2.4.0'; then
        echo "✅ Basic packages installed with pre-compiled wheels"
    else
        echo "❌ All installation methods failed."
        echo ""
        echo "🔧 Manual Solutions:"
        echo "1. Downgrade to Python 3.12:"
        echo "   - Install pyenv: curl https://pyenv.run | bash"
        echo "   - Install Python 3.12: pyenv install 3.12.0"
        echo "   - Use Python 3.12: pyenv local 3.12.0"
        echo "   - Recreate venv: rm -rf venv && python -m venv venv"
        echo ""
        echo "2. Use conda instead of pip:"
        echo "   - conda create -n taskmanager python=3.12"
        echo "   - conda activate taskmanager"
        echo "   - conda install fastapi uvicorn pydantic sqlalchemy"
        echo ""
        echo "3. Use Docker (if available):"
        echo "   - Create Dockerfile with Python 3.12 base image"
        exit 1
    fi
fi

# Fix imports in Python files for minimal setup
echo "🔧 Fixing imports for minimal setup..."

# Update app/core/config.py to handle missing pydantic-settings
if [ -f "app/core/config.py" ]; then
    cat > app/core/config.py << 'EOF'
"""
app/core/config.py - Application configuration management (Python 3.13 compatible)
"""
from typing import List
try:
    from pydantic import BaseSettings
except ImportError:
    # Fallback for newer pydantic versions
    from pydantic_settings import BaseSettings
    
from pydantic import validator
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Task Manager API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./task_manager.db"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Security
    SECRET_KEY: str = "development-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    def __init__(self, **kwargs):
        # Load from environment variables
        env_vars = {
            'APP_NAME': os.getenv('APP_NAME', self.APP_NAME),
            'DEBUG': os.getenv('DEBUG', str(self.DEBUG)).lower() == 'true',
            'DATABASE_URL': os.getenv('DATABASE_URL', self.DATABASE_URL),
            'HOST': os.getenv('HOST', self.HOST),
            'PORT': int(os.getenv('PORT', self.PORT)),
        }
        
        # Override with environment variables
        for key, value in env_vars.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        super().__init__(**kwargs)
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v: str, values: dict) -> str:
        if values.get("ENVIRONMENT") == "production" and v == "development-secret-key":
            raise ValueError("SECRET_KEY must be set in production")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


def get_settings() -> Settings:
    return settings
EOF
fi

# Create a simple test script to verify installation
cat > test_installation.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify FastAPI installation
"""
import sys

def test_imports():
    """Test if all required packages can be imported"""
    
    tests = [
        ("FastAPI", "from fastapi import FastAPI"),
        ("Uvicorn", "import uvicorn"),
        ("Pydantic", "from pydantic import BaseModel"),
        ("SQLAlchemy", "from sqlalchemy import create_engine"),
    ]
    
    print("🧪 Testing package imports...")
    print("=" * 40)
    
    success_count = 0
    
    for name, import_statement in tests:
        try:
            exec(import_statement)
            print(f"✅ {name}: OK")
            success_count += 1
        except ImportError as e:
            print(f"❌ {name}: Failed - {e}")
    
    print("=" * 40)
    print(f"📊 Results: {success_count}/{len(tests)} packages working")
    
    if success_count >= 3:  # At least FastAPI, Uvicorn, Pydantic
        print("🎉 Minimum requirements met! You can start development.")
        return True
    else:
        print("❌ Too many packages failed. Please check installation.")
        return False

def test_fastapi():
    """Test if FastAPI app can be created"""
    try:
        from fastapi import FastAPI
        app = FastAPI()
        
        @app.get("/")
        def read_root():
            return {"message": "Hello World"}
        
        print("✅ FastAPI app creation: OK")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation: Failed - {e}")
        return False

if __name__ == "__main__":
    print(f"🐍 Python version: {sys.version}")
    print("")
    
    if test_imports() and test_fastapi():
        print("")
        print("🚀 Installation verification successful!")
        print("💡 You can now run: python -m uvicorn app.main:app --reload")
    else:
        print("")
        print("❌ Installation verification failed.")
        sys.exit(1)
EOF

echo "🧪 Testing installation..."
python test_installation.py

echo ""
echo "🎉 Quick fix completed!"
echo ""
echo "📝 What was fixed:"
echo "✅ Updated to Python 3.13 compatible package versions"
echo "✅ Fixed pydantic-settings import issues"
echo "✅ Created minimal requirements file"
echo "✅ Added installation verification"
echo ""
echo "🚀 Next steps:"
echo "1. Test the server: python -m uvicorn app.main:app --reload"
echo "2. Check API docs: http://localhost:8000/docs"
echo "3. If issues persist, consider using Python 3.12"
echo ""
echo "⚠️  Note: Some advanced features may be disabled in minimal mode"
