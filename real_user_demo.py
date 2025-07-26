"""
🎭 REAL USER DEMO
See how the system handles actual everyday language!
"""

from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
from smart_processor import SmartQueryProcessor
import time

def real_user_demo():
    """Demonstrate how the system handles real casual language"""

    print("🎭 REAL USER LANGUAGE DEMO")
    print("=" * 50)
    print("See how our AI handles the way people ACTUALLY talk!\n")

    # Load the insurance system
    print("🔄 Loading insurance system...")
    all_chunks, document_sources = process_multiple_documents("docs")
    embeddings = get_embeddings(all_chunks)
    processor = SmartQueryProcessor()

    print(f"✅ Loaded {len(set(document_sources))} insurance policies\n")

    # Real examples of how people actually describe their situations
    real_user_examples = [
        {
            "user_says": "hey my kid fell off his bike and broke his wrist he's 10 and we've had insurance forever",
            "category": "🚴 Kids Being Kids"
        },
        {
            "user_says": "i twisted my ankle bad playing basketball can barely walk need to go to hospital am 22",
            "category": "🏀 Sports Injury"
        },
        {
            "user_says": "my mom had chest pain rushed her to ER they say she needs heart surgery she's 60 old policy",
            "category": "🚨 Medical Emergency"
        },
        {
            "user_says": "pregnant wife having complications doctor says c-section needed we're scared insurance 6 months old",
            "category": "👶 Pregnancy Emergency"
        },
        {
            "user_says": "hurt my back lifting heavy stuff at work can't move properly need MRI am 35 have insurance 3 years",
            "category": "💼 Work Injury"
        },
        {
            "user_says": "my baby has been throwing up and fever ambulance to hospital insurance is new",
            "category": "👶 Sick Baby"
        }
    ]

    for i, example in enumerate(real_user_examples, 1):
        print(f"📝 EXAMPLE {i}: {example['category']}")
        print("─" * 40)
        print(f"👤 User says: \"{example['user_says']}\"")

        # Process with smart understanding
        processed_info = processor.process_query(example['user_says'])
        print(f"🧠 AI understands: \"{processed_info['processed']}\"")

        if processed_info['is_emergency']:
            print("🚨 EMERGENCY DETECTED - Fast-track processing!")

        if processed_info['analysis']:
            print(f"✨ AI applied: {', '.join(processed_info['analysis'])}")

        print("\n🤖 Analyzing claim...")
        time.sleep(1)

        try:
            # Find relevant clauses
            relevant_chunks = semantic_search(processed_info['processed'], all_chunks, embeddings, top_k=5)

            # Get sources
            relevant_indices = []
            for chunk in relevant_chunks:
                try:
                    idx = all_chunks.index(chunk)
                    relevant_indices.append(idx)
                except ValueError:
                    relevant_indices.append(0)

            relevant_sources = [document_sources[idx] for idx in relevant_indices]

            # Get AI decision
            result = ask_llm(example['user_says'], relevant_chunks, relevant_sources)

            # Display result in user-friendly way
            if result['decision'] == 'approved':
                print("🎉 GOOD NEWS: Your claim looks like it will be covered!")
            elif result['decision'] == 'rejected':
                print("😔 SORRY: This claim might not be covered")
            else:
                print("⚠️ UNCLEAR: Need more information")

            if result.get('amount'):
                print(f"💰 Estimated amount: ₹{result['amount']:,}")

            if result.get('emergency_override'):
                print("🚨 Emergency override applied!")

            # Simple explanation
            if result.get('user_friendly_explanation'):
                print(f"💬 Simple explanation: {result['user_friendly_explanation']}")
            else:
                # Fallback to simplified justification
                simple_explanation = result['justification'][:150] + "..."
                print(f"💬 Why: {simple_explanation}")

            print(f"📄 Checked {len(set(relevant_sources))} insurance policies")

        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n" + "="*60 + "\n")

    print("🏆 DEMO COMPLETE!")
    print("The AI successfully understood and processed casual, everyday language!")
    print("No insurance jargon required - just talk naturally! 💬")

def interactive_chat():
    """Simple interactive chat for testing"""

    print("\n💬 INTERACTIVE CHAT MODE")
    print("=" * 30)
    print("Type your insurance situation in your own words!")
    print("(Type 'quit' to exit)\n")

    # Load system
    print("🔄 Loading...")
    all_chunks, document_sources = process_multiple_documents("docs")
    embeddings = get_embeddings(all_chunks)
    processor = SmartQueryProcessor()
    print("✅ Ready!\n")

    while True:
        user_input = input("👤 You: ").strip()

        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break

        if not user_input:
            continue

        try:
            # Process input
            processed_info = processor.process_query(user_input)
            print(f"🧠 AI understood: {processed_info['processed']}")

            if processed_info['is_emergency']:
                print("🚨 EMERGENCY DETECTED!")

            # Quick analysis
            relevant_chunks = semantic_search(processed_info['processed'], all_chunks, embeddings, top_k=3)
            relevant_indices = [all_chunks.index(chunk) for chunk in relevant_chunks if chunk in all_chunks]
            relevant_sources = [document_sources[idx] for idx in relevant_indices]

            result = ask_llm(user_input, relevant_chunks, relevant_sources)

            # Simple response
            decision_emoji = "✅" if result['decision'] == 'approved' else "❌"
            print(f"🤖 AI: {decision_emoji} {result['decision'].upper()}")

            if result.get('user_friendly_explanation'):
                print(f"💬 {result['user_friendly_explanation']}")

            print()

        except Exception as e:
            print(f"🤖 AI: Sorry, I had trouble understanding that. Can you try rephrasing? ({e})\n")

if __name__ == "__main__":
    real_user_demo()

    # Ask if they want to try interactive mode
    try_interactive = input("\n🎮 Want to try interactive chat mode? (y/n): ").strip().lower()
    if try_interactive in ['y', 'yes']:
        interactive_chat()
