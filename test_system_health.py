"""
🧪 QUICK SYSTEM TEST
===================
This script tests if all components are working correctly.
"""

import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def test_dependencies():
    """Test if all required dependencies are installed"""
    print(f"{Fore.YELLOW}🔍 Testing dependencies...")

    required_packages = [
        'faiss',
        'numpy',
        'sentence_transformers',
        'google.generativeai',
        'dotenv',
        'PyPDF2',
        'fitz',  # PyMuPDF
        'colorama'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'fitz':
                import fitz
            elif package == 'dotenv':
                from dotenv import load_dotenv
            elif package == 'google.generativeai':
                import google.generativeai as genai
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package}")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n{Fore.RED}Missing packages: {', '.join(missing_packages)}")
        return False
    else:
        print(f"\n{Fore.GREEN}✅ All dependencies are installed!")
        return True

def test_environment():
    """Test environment setup"""
    print(f"\n{Fore.YELLOW}🔍 Testing environment setup...")

    # Check for .env file
    if os.path.exists('.env'):
        print(f"   ✅ .env file found")
    else:
        print(f"   ❌ .env file not found")
        return False

    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if api_key:
        print(f"   ✅ GOOGLE_API_KEY found")
    else:
        print(f"   ❌ GOOGLE_API_KEY not found in .env file")
        return False

    print(f"\n{Fore.GREEN}✅ Environment setup is correct!")
    return True

def test_documents():
    """Test if policy documents are available"""
    print(f"\n{Fore.YELLOW}🔍 Testing policy documents...")

    docs_folder = "docs"
    if not os.path.exists(docs_folder):
        print(f"   ❌ docs folder not found")
        return False

    # Look for policy documents
    policy_files = []
    for file in os.listdir(docs_folder):
        if file.lower().endswith(('.pdf', '.docx')):
            if 'policy' in file.lower() or 'sample' in file.lower():
                policy_files.append(file)

    if policy_files:
        print(f"   ✅ Found policy documents:")
        for file in policy_files:
            print(f"      • {file}")
    else:
        print(f"   ❌ No policy documents found in docs folder")
        return False

    print(f"\n{Fore.GREEN}✅ Policy documents are available!")
    return True

def test_basic_functionality():
    """Test basic system functionality"""
    print(f"\n{Fore.YELLOW}🔍 Testing basic functionality...")

    try:
        # Test imports
        from main import IntelligentClaimsProcessor
        print(f"   ✅ Main processor import successful")

        from smart_processor import SmartQueryProcessor
        print(f"   ✅ Smart processor import successful")

        from utils import extract_text_from_file, chunk_text
        print(f"   ✅ Utils import successful")

        # Test smart processor
        smart_proc = SmartQueryProcessor()
        test_query = "25 year old broke arm"
        result = smart_proc.process_query(test_query)
        print(f"   ✅ Smart query processing works")

        print(f"\n{Fore.GREEN}✅ Basic functionality test passed!")
        return True

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def run_quick_test():
    """Run a quick end-to-end test"""
    print(f"\n{Fore.YELLOW}🔍 Running quick end-to-end test...")

    try:
        from main import IntelligentClaimsProcessor

        # Initialize processor
        processor = IntelligentClaimsProcessor()
        print(f"   ✅ Processor initialized")

        # Load documents
        if processor.load_documents("docs"):
            print(f"   ✅ Documents loaded successfully")
        else:
            print(f"   ❌ Failed to load documents")
            return False

        # Test a simple query
        test_query = "broken arm, 25 years old, 1 year policy"
        decision = processor.process_claim_query(test_query)

        if decision and 'decision' in decision:
            print(f"   ✅ Query processing successful")
            print(f"   📋 Result: {decision['decision']}")
        else:
            print(f"   ❌ Query processing failed")
            return False

        print(f"\n{Fore.GREEN}✅ End-to-end test passed!")
        return True

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("🧪 INTELLIGENT CLAIMS PROCESSOR - SYSTEM TEST")
    print("=" * 50)
    print(f"{Style.RESET_ALL}")

    all_tests_passed = True

    # Run tests
    tests = [
        ("Dependencies", test_dependencies),
        ("Environment", test_environment),
        ("Documents", test_documents),
        ("Basic Functionality", test_basic_functionality),
        ("End-to-End Test", run_quick_test)
    ]

    for test_name, test_func in tests:
        print(f"\n{Fore.CYAN}{'=' * 20} {test_name} {'=' * 20}")
        if not test_func():
            all_tests_passed = False
            print(f"{Fore.RED}❌ {test_name} FAILED")
        else:
            print(f"{Fore.GREEN}✅ {test_name} PASSED")

    # Final result
    print(f"\n{Fore.CYAN}{'=' * 50}")
    if all_tests_passed:
        print(f"{Fore.GREEN}{Style.BRIGHT}🎉 ALL TESTS PASSED!")
        print(f"Your system is ready to process insurance claims!")
        print(f"\nNext steps:")
        print(f"• Run 'python demo.py' for a comprehensive demonstration")
        print(f"• Run 'python main.py' for interactive mode")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}❌ SOME TESTS FAILED!")
        print(f"Please fix the issues above before using the system.")

    print(f"{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
