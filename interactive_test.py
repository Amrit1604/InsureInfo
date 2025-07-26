"""
Interactive Multi-Document Claims Testing System
"""

import os
import json
from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm

def interactive_claims_system():
    """Interactive system to test claims against multiple documents"""

    print("🏥 Multi-Document Claims Processing System")
    print("=" * 50)

    # Load all documents once
    print("Loading all policy documents...")
    try:
        all_chunks, document_sources = process_multiple_documents("docs")
        embeddings = get_embeddings(all_chunks)
        print(f"✅ Loaded {len(all_chunks)} clauses from {len(set(document_sources))} documents")
    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        return

    # Sample queries for quick testing
    sample_queries = [
        "I'm 19 years old, I have a 5-year-old insurance policy, and I fell to the ground and broke my ligament",
        "25-year-old with 2-year policy, broken arm from bicycle accident",
        "30-year-old with 6-month policy, knee surgery needed",
        "22-year-old with 4-year policy, torn ACL from basketball",
        "45-year-old with 1-year policy, hip replacement surgery"
    ]

    while True:
        print("\n" + "="*50)
        print("OPTIONS:")
        print("1. Enter custom claim query")
        print("2. Use sample queries")
        print("3. Show loaded documents")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            query = input("\nEnter your claim details: ").strip()
            if query:
                process_query(query, all_chunks, document_sources, embeddings)

        elif choice == "2":
            print("\nSample Queries:")
            for i, query in enumerate(sample_queries, 1):
                print(f"{i}. {query}")

            try:
                sample_choice = int(input("\nChoose sample (1-5): ")) - 1
                if 0 <= sample_choice < len(sample_queries):
                    process_query(sample_queries[sample_choice], all_chunks, document_sources, embeddings)
            except ValueError:
                print("Invalid choice!")

        elif choice == "3":
            show_documents(document_sources)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

def process_query(query, all_chunks, document_sources, embeddings):
    """Process a single query"""
    print(f"\n🔍 Processing: {query}")
    print("-" * 40)

    try:
        # Find relevant clauses
        relevant_chunks = semantic_search(query, all_chunks, embeddings)

        # Get corresponding document sources
        relevant_indices = []
        for chunk in relevant_chunks:
            try:
                idx = all_chunks.index(chunk)
                relevant_indices.append(idx)
            except ValueError:
                relevant_indices.append(0)

        relevant_sources = [document_sources[idx] for idx in relevant_indices]

        # Get LLM decision
        result = ask_llm(query, relevant_chunks, relevant_sources)

        # Display results
        print(f"\n📋 DECISION: {result['decision'].upper()}")

        if result.get('amount'):
            print(f"💰 AMOUNT: ₹{result['amount']:,}")

        print(f"\n📝 JUSTIFICATION:")
        print(result['justification'])

        print(f"\n📄 DOCUMENTS REFERENCED:")
        unique_sources = list(set(relevant_sources))
        for source in unique_sources:
            count = relevant_sources.count(source)
            print(f"  • {source}: {count} clause(s)")

        # Show relevant clauses
        print(f"\n🔍 RELEVANT CLAUSES FOUND:")
        for i, (chunk, source) in enumerate(zip(relevant_chunks, relevant_sources), 1):
            print(f"\nClause {i} (from {source}):")
            print(f"{chunk[:200]}..." if len(chunk) > 200 else chunk)

    except Exception as e:
        print(f"❌ Error processing query: {e}")

def show_documents(document_sources):
    """Show information about loaded documents"""
    unique_docs = list(set(document_sources))
    print(f"\n📚 LOADED DOCUMENTS ({len(unique_docs)} total):")

    for doc in sorted(unique_docs):
        count = document_sources.count(doc)
        print(f"  • {doc}: {count} clauses")

if __name__ == "__main__":
    interactive_claims_system()
