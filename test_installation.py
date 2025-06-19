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
