"""
Simple test script to verify backend setup
"""
import sys
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("✓ FastAPI")
    except ImportError as e:
        print(f"✗ FastAPI: {e}")
        return False
    
    try:
        import uvicorn
        print("✓ Uvicorn")
    except ImportError as e:
        print(f"✗ Uvicorn: {e}")
        return False
    
    try:
        import pydantic
        print("✓ Pydantic")
    except ImportError as e:
        print(f"✗ Pydantic: {e}")
        return False
    
    try:
        import jose
        print("✓ Python-JOSE")
    except ImportError as e:
        print(f"✗ Python-JOSE: {e}")
        return False
    
    try:
        import passlib
        print("✓ Passlib")
    except ImportError as e:
        print(f"✗ Passlib: {e}")
        return False
    
    try:
        import supabase
        print("✓ Supabase")
    except ImportError as e:
        print(f"✗ Supabase: {e}")
        return False
    
    return True


def test_env_file():
    """Test that .env file exists"""
    print("\nTesting environment configuration...")
    
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found")
        print("  Please copy .env.example to .env and fill in your credentials")
        return False


def test_app_structure():
    """Test that app structure is correct"""
    print("\nTesting app structure...")
    
    required_files = [
        "app/__init__.py",
        "app/main.py",
        "app/config.py",
        "app/database.py",
        "app/models.py",
        "app/auth.py",
        "app/routers/__init__.py",
        "app/routers/auth.py",
        "app/routers/projects.py",
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} not found")
            all_exist = False
    
    return all_exist


def main():
    print("=" * 50)
    print("Backend Setup Verification")
    print("=" * 50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_env_file()))
    results.append(("App Structure", test_app_structure()))
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("✓ All checks passed! You're ready to run the backend.")
        print("\nTo start the server, run:")
        print("  python run.py")
        print("\nOr:")
        print("  uvicorn app.main:app --reload")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
