import os
import json
from main import extract_text_from_file, chunk_text, get_embeddings, semantic_search, ask_llm

def test_improved_search():
    """Test to show which clauses are being retrieved"""

    # Load document
    file_path = "docs/sample_policy.pdf"
    text = extract_text_from_file(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)

    # Test query
    query = "I'm 19 years old, I have a 5-year-old insurance policy, and I fell to the ground and broke my ligament"

    print("Query:", query)
    print("\n" + "="*60)
    print("RETRIEVED CLAUSES:")
    print("="*60)

    relevant_clauses = semantic_search(query, chunks, embeddings)

    for i, clause in enumerate(relevant_clauses, 1):
        print(f"\nClause {i}:")
        print("-" * 40)
        print(clause[:300] + "..." if len(clause) > 300 else clause)

    print("\n" + "="*60)
    print("FINAL DECISION:")
    print("="*60)

    result = ask_llm(query, relevant_clauses)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    test_improved_search()
