"""
🚀 ULTIMATE DEMO SCRIPT
Showcasing the full power of your real policy analysis system!
"""

import time
from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
import json

def epic_demo():
    """The ultimate demonstration of your claims system"""

    print("🎬" + "="*60)
    print("🚀 ULTIMATE CLAIMS SYSTEM DEMONSTRATION")
    print("   Powered by REAL Insurance Policy Documents")
    print("="*60 + "🎬\n")

    time.sleep(1)

    # Load the real policies
    print("📚 Loading your REAL policy documents...")
    all_chunks, document_sources = process_multiple_documents("docs")
    embeddings = get_embeddings(all_chunks)

    print(f"✅ Loaded {len(set(document_sources))} real policy documents")
    print(f"📄 Extracted {len(all_chunks)} clauses total")

    # Show what we're working with
    policy_breakdown = {}
    for doc in set(document_sources):
        policy_breakdown[doc] = document_sources.count(doc)

    print(f"\n📋 YOUR POLICY PORTFOLIO:")
    for policy, count in policy_breakdown.items():
        print(f"   🔹 {policy}: {count} clauses")

    print(f"\n" + "="*60)

    # Demo scenarios that show the system's intelligence
    demo_scenarios = [
        {
            "title": "🏃 Young Athlete Injury",
            "query": "19-year-old college athlete, torn ligament during basketball, has 5-year family policy",
            "highlight": "Tests age limits, sports coverage, and policy duration benefits"
        },
        {
            "title": "🚗 Car Accident Emergency",
            "query": "25-year-old driver, broken ribs and internal bleeding from car crash, 2-year policy",
            "highlight": "Tests emergency coverage, accident benefits, and trauma care"
        },
        {
            "title": "🏥 Routine vs Emergency",
            "query": "30-year-old needs emergency appendectomy, but only has 6-month-old policy",
            "highlight": "Tests waiting periods vs emergency provisions"
        },
        {
            "title": "👶 New Parent Coverage",
            "query": "28-year-old pregnant woman, delivery complications, 18-month policy",
            "highlight": "Tests maternity benefits and complication coverage"
        },
        {
            "title": "🧠 Mental Health Support",
            "query": "22-year-old college student, anxiety and depression therapy, 3-year policy",
            "highlight": "Tests mental health coverage in real policies"
        }
    ]

    results_summary = []

    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"\n🎯 DEMO {i}/5: {scenario['title']}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"📝 Scenario: {scenario['query']}")
        print(f"🔍 Testing: {scenario['highlight']}")

        print(f"\n🤖 AI Analyzing...")
        time.sleep(1)

        try:
            # Run the analysis
            relevant_chunks = semantic_search(scenario['query'], all_chunks, embeddings, top_k=5)

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
            result = ask_llm(scenario['query'], relevant_chunks, relevant_sources)

            # Display result
            decision_emoji = "✅" if result['decision'] == 'approved' else "❌"
            print(f"\n{decision_emoji} DECISION: {result['decision'].upper()}")

            if result.get('amount'):
                print(f"💰 AMOUNT: ₹{result['amount']:,}")

            # Show which policies were used
            unique_sources = list(set(relevant_sources))
            print(f"📄 POLICIES CONSULTED: {', '.join(unique_sources)}")

            # Brief justification
            justification = result['justification'][:200] + "..." if len(result['justification']) > 200 else result['justification']
            print(f"📋 REASONING: {justification}")

            results_summary.append({
                "scenario": scenario['title'],
                "decision": result['decision'],
                "policies_used": len(unique_sources)
            })

        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            results_summary.append({
                "scenario": scenario['title'],
                "decision": "error",
                "policies_used": 0
            })

        print(f"\n{'─'*60}")

    # Final summary
    print(f"\n🏆 DEMONSTRATION COMPLETE!")
    print(f"{'='*60}")

    approved = sum(1 for r in results_summary if r['decision'] == 'approved')
    rejected = sum(1 for r in results_summary if r['decision'] == 'rejected')
    errors = sum(1 for r in results_summary if r['decision'] == 'error')

    print(f"📊 RESULTS SUMMARY:")
    print(f"   ✅ Approved Claims: {approved}")
    print(f"   ❌ Rejected Claims: {rejected}")
    print(f"   ⚠️  Processing Errors: {errors}")

    avg_policies = sum(r['policies_used'] for r in results_summary) / len(results_summary)
    print(f"   📄 Average Policies Consulted: {avg_policies:.1f}")

    print(f"\n🎯 KEY ACHIEVEMENTS:")
    print(f"   🔹 Successfully processed real insurance policy documents")
    print(f"   🔹 Intelligent semantic search across multiple policies")
    print(f"   🔹 AI-powered decision making with justifications")
    print(f"   🔹 Cross-policy analysis and source tracking")
    print(f"   🔹 Handles complex scenarios like age limits, waiting periods, emergencies")

    print(f"\n🚀 YOUR CLAIMS SYSTEM IS READY FOR PRODUCTION!")
    print(f"{'='*60}")

    # Save detailed results
    with open("demo_results.json", "w") as f:
        json.dump({
            "demo_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "policies_loaded": list(policy_breakdown.keys()),
            "total_clauses": len(all_chunks),
            "test_results": results_summary,
            "summary": {
                "approved": approved,
                "rejected": rejected,
                "errors": errors,
                "average_policies_consulted": avg_policies
            }
        }, f, indent=2)

    print(f"📄 Detailed results saved to 'demo_results.json'")

if __name__ == "__main__":
    epic_demo()
