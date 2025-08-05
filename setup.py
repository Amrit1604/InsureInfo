"""
🔧 HACKATHON SETUP WIZARD
========================
Complete setup script for the LLM Claims Processing API
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up environment variables"""
    print("🔐 Setting up environment variables...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        print("✅ .env file already exists")
        return True

    if env_example.exists():
        print("📋 Found .env.example file")
        api_key = input("🔑 Enter your Google Gemini API key: ").strip()

        if api_key and not api_key.startswith("your_"):
            # Create .env file from example
            with open(env_example, 'r') as f:
                content = f.read()

            # Replace placeholder with actual key
            content = content.replace("your_gemini_api_key_here", api_key)

            with open(env_file, 'w') as f:
                f.write(content)

            print("✅ .env file created successfully")
            return True
        else:
            print("❌ Invalid API key provided")
            return False
    else:
        print("❌ .env.example file not found")
        return False

def check_documents():
    """Check document setup"""
    print("\n📄 Checking documents...")

    docs_path = Path("docs")
    if not docs_path.exists():
        print("❌ docs folder not found!")
        return False

    pdf_files = list(docs_path.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in docs folder!")
        return False

    print(f"✅ Found {len(pdf_files)} PDF document(s):")
    for pdf in pdf_files:
        size_mb = pdf.stat().st_size / (1024 * 1024)
        print(f"   📄 {pdf.name} ({size_mb:.2f} MB)")

    return True

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python packages...")

    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("✅ All packages installed successfully")
            return True
        else:
            print(f"❌ Package installation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing packages: {str(e)}")
        return False

def test_imports():
    """Test if all imports work"""
    print("\n🧪 Testing imports...")

    try:
        import fastapi
        print("✅ FastAPI imported")

        import sentence_transformers
        print("✅ SentenceTransformers imported")

        import google.generativeai
        print("✅ Google Gemini imported")

        import faiss
        print("✅ FAISS imported")

        return True
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("🏆 HACKATHON API SETUP WIZARD")
    print("=" * 40)
    print("This will set up your LLM Claims Processing API for the hackathon.")
    print()

    # Step 1: Environment setup
    if not setup_environment():
        print("❌ Environment setup failed. Please try again.")
        return False

    # Step 2: Document check
    if not check_documents():
        print("❌ Document setup incomplete. Please add PDF files to docs/ folder.")
        return False

    # Step 3: Install requirements
    if not install_requirements():
        print("❌ Package installation failed. Please check your Python environment.")
        return False

    # Step 4: Test imports
    if not test_imports():
        print("❌ Import test failed. Please check package installation.")
        return False

    # Success!
    print("\n" + "=" * 40)
    print("🎉 SETUP COMPLETE!")
    print()
    print("✅ Environment variables configured")
    print("✅ Documents ready")
    print("✅ Packages installed")
    print("✅ Imports working")
    print()
    print("🚀 Next steps:")
    print("1. Start the API: python api_server.py")
    print("2. Test the API: python test_api.py")
    print("3. View docs: http://localhost:8000/docs")
    print()
    print("🌐 Webhook URL for submission:")
    print("POST http://localhost:8000/hackrx/run")
    print()
    print("🏆 Good luck with the hackathon!")

    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup error: {str(e)}")
        print("Please check your environment and try again.")
