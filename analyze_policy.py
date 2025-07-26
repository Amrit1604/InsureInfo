"""
Policy Document Analyzer
Extracts and analyzes the insurance policy content
"""

from utils import extract_text_from_file
import re

def analyze_policy_document():
    print("📄 ANALYZING POLICY DOCUMENT...")
    print("="*60)

    # Extract text from PDF
    text = extract_text_from_file('docs/sample_policy_merged.pdf')

    print(f"Total document length: {len(text)} characters")
    print(f"Total lines: {len(text.split(chr(10)))}")

    # Find key sections
    sections = {
        'DEFINITIONS': [],
        'COVERAGE': [],
        'EXCLUSIONS': [],
        'WAITING PERIODS': [],
        'PROCEDURES': [],
        'CLAIMS': []
    }

    lines = text.split('\n')
    current_section = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Look for section headers
        if 'DEFINITIONS' in line.upper() and len(line) < 100:
            current_section = 'DEFINITIONS'
            print(f"\n📋 Found DEFINITIONS section at line {i}")

        elif any(word in line.upper() for word in ['COVERAGE', 'BENEFITS', 'WHAT IS COVERED']):
            if len(line) < 100:
                current_section = 'COVERAGE'
                print(f"\n✅ Found COVERAGE section at line {i}")

        elif 'EXCLUSION' in line.upper() and len(line) < 100:
            current_section = 'EXCLUSIONS'
            print(f"\n❌ Found EXCLUSIONS section at line {i}")

        elif 'WAITING PERIOD' in line.upper() and len(line) < 100:
            current_section = 'WAITING PERIODS'
            print(f"\n⏰ Found WAITING PERIODS section at line {i}")

        elif any(word in line.upper() for word in ['CLAIM', 'PROCEDURE']):
            if len(line) < 100:
                current_section = 'PROCEDURES'
                print(f"\n🔄 Found PROCEDURES section at line {i}")

        # Store content in appropriate section
        if current_section and len(line) > 10:
            sections[current_section].append(line)

    # Print key findings
    print("\n" + "="*60)
    print("📊 POLICY ANALYSIS SUMMARY")
    print("="*60)

    for section_name, content in sections.items():
        if content:
            print(f"\n{section_name}:")
            print(f"  - Found {len(content)} relevant lines")
            print(f"  - Sample: {content[0][:100]}...")

    # Look for specific medical conditions and coverage
    print("\n🏥 MEDICAL CONDITIONS ANALYSIS:")
    print("-"*40)

    medical_keywords = [
        'surgery', 'heart', 'cardiac', 'ortho', 'bone', 'fracture',
        'emergency', 'accident', 'cancer', 'diabetes', 'kidney',
        'liver', 'lung', 'brain', 'spine', 'maternity', 'pregnancy'
    ]

    for keyword in medical_keywords:
        matches = len(re.findall(keyword, text, re.IGNORECASE))
        if matches > 0:
            print(f"  - '{keyword}': mentioned {matches} times")

    # Extract waiting periods
    waiting_period_matches = re.findall(r'(\d+)\s*(day|month|year)s?\s*(waiting|wait)', text, re.IGNORECASE)
    if waiting_period_matches:
        print(f"\n⏰ WAITING PERIODS FOUND:")
        for match in set(waiting_period_matches):
            print(f"  - {match[0]} {match[1]}(s)")

    # Extract coverage amounts
    amount_matches = re.findall(r'₹\s*(\d+(?:,\d+)*)', text)
    if amount_matches:
        print(f"\n💰 COVERAGE AMOUNTS MENTIONED:")
        for amount in set(amount_matches[:5]):  # Show first 5 unique amounts
            print(f"  - ₹{amount}")

    return text

if __name__ == "__main__":
    policy_text = analyze_policy_document()
