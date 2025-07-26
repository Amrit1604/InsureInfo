"""
Script to help you add your Document 1-5 files to the system
"""

import os

def setup_documents():
    """Helper to set up multiple documents"""
    docs_folder = "docs"

    # Create docs folder if it doesn't exist
    if not os.path.exists(docs_folder):
        os.makedirs(docs_folder)
        print(f"Created '{docs_folder}' folder")

    print("Current files in docs folder:")
    files = os.listdir(docs_folder)
    if files:
        for file in files:
            print(f"  - {file}")
    else:
        print("  (empty)")

    print("\n" + "="*50)
    print("INSTRUCTIONS TO ADD YOUR DOCUMENTS:")
    print("="*50)
    print("1. Copy your Document 1-5 files to the 'docs' folder")
    print("2. Rename them as needed (e.g., 'Document_1.pdf', 'Document_2.docx')")
    print("3. Supported formats: PDF, DOCX, EML")
    print("4. The system will automatically process all files in the docs folder")

    print(f"\nDocs folder location: {os.path.abspath(docs_folder)}")

    # Create some example placeholder files for testing
    example_files = [
        "Document_1.txt",
        "Document_2.txt",
        "Document_3.txt",
        "Document_4.txt",
        "Document_5.txt"
    ]

    print("\nWould you like me to create example placeholder files? (for testing)")
    print("These are just text files with sample content.")

if __name__ == "__main__":
    setup_documents()
