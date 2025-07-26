"""
🧪 TEST IMPROVED CLAIMS LOGIC
Testing the scenarios you mentioned to ensure proper approvals
"""

from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
from smart_processor import SmartQueryProcessor

def test_claim(description, expected_result=None):
    """Test a claim and show results"""
    print(f"\n{'='*60}")
    print(f"🧪 TESTING: {description}")
    print('='*60)

    try:
        # Process with smart understanding
        processor = SmartQueryProcessor()
        processed_info = processor.process_query(description)

        print(f"👤 User said: {description}")
        print(f"🧠 AI understood: {processed_info['processed']}")
        if processed_info['is_emergency']:
            print("🚨 EMERGENCY DETECTED!")
        if processed_info['analysis']:
            print(f"✨ Intelligence: {', '.join(processed_info['analysis'])}")
        print()

        # Find relevant policy clauses
        relevant_chunks = semantic_search(processed_info['processed'], all_chunks, embeddings, top_k=5)

        # Get corresponding sources
        relevant_indices = []
        for chunk in relevant_chunks:
            try:
                idx = all_chunks.index(chunk)
                relevant_indices.append(idx)
            except ValueError:
                relevant_indices.append(0)

        relevant_sources = [document_sources[idx] for idx in relevant_indices]

        # Get AI decision
        result = ask_llm(description, relevant_chunks, relevant_sources)

        # Show results
        decision_emoji = {
            'approved': '✅ APPROVED',
            'rejected': '❌ REJECTED',
            'error': '⚠️ ERROR'
        }.get(result['decision'], '❓ UNKNOWN')

        print(f"🤖 AI Decision: {decision_emoji}")

        if result.get('amount'):
            print(f"💰 Amount: ₹{result['amount']:,}")

        if result.get('user_friendly_explanation'):
            print(f"💬 Explanation: {result['user_friendly_explanation']}")

        if result.get('emergency_override'):
            print("🚨 Emergency override applied!")

        # Expected vs actual
        if expected_result:
            status = "✅ CORRECT" if result['decision'] == expected_result else "❌ WRONG"
            print(f"\n📊 Expected: {expected_result.upper()}, Got: {result['decision'].upper()} - {status}")

        return result

    except Exception as e:
        print(f"💥 ERROR: {str(e)}")
        return None

def main():
    print("🚀 TESTING IMPROVED CLAIMS SYSTEM")
    print("Loading insurance policies...")

    # Load data
    global all_chunks, document_sources, embeddings
    all_chunks, document_sources = process_multiple_documents("docs")
    embeddings = get_embeddings(all_chunks)

    print(f"📚 Loaded {len(set(document_sources))} policies with {len(all_chunks)} clauses")

    # Test scenarios that should be APPROVED
    print("\n\n🟢 SCENARIOS THAT SHOULD BE APPROVED:")

    test_claim(
        "my friend got his ligament busted while playing basketball he is 19 and have 3 year old insurance",
        expected_result="approved"
    )

    test_claim(
        "32 year old man with heart issue have 3 year old insurance",
        expected_result="approved"
    )

    test_claim(
        "my friend got his ligament busted while playing basketball he is 19 and have 1 year old insurance",
        expected_result="approved"
    )

    # Test edge cases
    print("\n\n🟡 EDGE CASES:")

    test_claim(
        "my friend got his ligament busted while playing basketball he is 19 and have 5 months old insurance",
        expected_result="approved"  # Should be approved for sports injury
    )

    test_claim(
        "emergency heart attack 25 year old new insurance 1 month old",
        expected_result="approved"  # Emergency should override waiting period
    )

if __name__ == "__main__":
    main()
