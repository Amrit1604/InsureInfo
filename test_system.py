import os
import json
from main import extract_text_from_file, chunk_text, get_embeddings, semantic_search, ask_llm

def test_different_queries():
    """Test the system with various claim scenarios"""

    # Load document once
    file_path = "docs/sample_policy.pdf"
    text = extract_text_from_file(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)

    # Test queries
    test_queries = [
        "25-year-old female, dental treatment, Mumbai, 6-month policy",
        "60-year-old male, heart surgery, emergency, Delhi, 2-year policy",
        "35-year-old male, eye surgery, elective, Bangalore, 1-year policy",
        "45-year-old female, maternity, delivery, Chennai, 10-month policy",
        "50-year-old male, cosmetic surgery, face lift, Pune, 5-year policy"
    ]

    print("Testing LLM Claims System with Multiple Scenarios")
    print("=" * 60)

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)

        try:
            relevant = semantic_search(query, chunks, embeddings)
            result = ask_llm(query, relevant)

            print(f"Decision: {result['decision'].upper()}")
            if result['amount']:
                print(f"Amount: {result['amount']}")
            print(f"Justification: {result['justification'][:200]}...")

        except Exception as e:
            print(f"Error processing query: {e}")

if __name__ == "__main__":
    test_different_queries()
