"""
Advanced Multi-Policy Analysis System
Let's see what's really in these policies!
"""

import os
import json
from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
import numpy as np

def analyze_policy_collection():
    """Comprehensive analysis of all policy documents"""

    print("🔍 ADVANCED MULTI-POLICY ANALYSIS SYSTEM")
    print("=" * 60)

    # Load all documents
    try:
        all_chunks, document_sources = process_multiple_documents("docs")
        embeddings = get_embeddings(all_chunks)

        print(f"📚 Loaded {len(set(document_sources))} policy documents")
        print(f"📄 Total clauses: {len(all_chunks)}")

        # Analyze document composition
        analyze_document_composition(document_sources)

        # Test comprehensive claim scenarios
        test_claim_scenarios(all_chunks, document_sources, embeddings)

        # Analyze coverage patterns
        analyze_coverage_patterns(all_chunks, document_sources, embeddings)

    except Exception as e:
        print(f"❌ Error: {e}")

def analyze_document_composition(document_sources):
    """Show what's in each document"""
    print("\n📊 DOCUMENT COMPOSITION:")
    print("-" * 40)

    doc_stats = {}
    for doc in document_sources:
        doc_stats[doc] = doc_stats.get(doc, 0) + 1

    for doc, count in sorted(doc_stats.items()):
        print(f"📋 {doc}: {count} clauses")

def test_claim_scenarios(all_chunks, document_sources, embeddings):
    """Test various claim scenarios against real policies"""
    print("\n🧪 COMPREHENSIVE CLAIM TESTING:")
    print("-" * 40)

    test_scenarios = [
        {
            "query": "19-year-old with 5-year policy, fell and broke ligament",
            "category": "Sports/Accident Injury"
        },
        {
            "query": "25-year-old with 2-year policy, needs knee surgery after car accident",
            "category": "Vehicle Accident"
        },
        {
            "query": "30-year-old with 6-month policy, emergency appendicitis surgery",
            "category": "Emergency Surgery"
        },
        {
            "query": "45-year-old with 4-year policy, diabetes treatment and medication",
            "category": "Chronic Condition"
        },
        {
            "query": "22-year-old with 3-year policy, mental health counseling and therapy",
            "category": "Mental Health"
        },
        {
            "query": "35-year-old with 1-year policy, maternity care and delivery",
            "category": "Maternity"
        }
    ]

    results_summary = []

    for scenario in test_scenarios:
        print(f"\n🔍 Testing: {scenario['category']}")
        print(f"Query: {scenario['query']}")

        try:
            # Find relevant clauses
            relevant_chunks = semantic_search(scenario['query'], all_chunks, embeddings)

            # Get document sources
            relevant_indices = []
            for chunk in relevant_chunks:
                try:
                    idx = all_chunks.index(chunk)
                    relevant_indices.append(idx)
                except ValueError:
                    relevant_indices.append(0)

            relevant_sources = [document_sources[idx] for idx in relevant_indices]

            # Get decision
            result = ask_llm(scenario['query'], relevant_chunks, relevant_sources)

            # Store result
            results_summary.append({
                "category": scenario['category'],
                "decision": result['decision'],
                "sources": list(set(relevant_sources))
            })

            print(f"✅ Decision: {result['decision'].upper()}")
            print(f"📄 Sources: {', '.join(set(relevant_sources))}")

        except Exception as e:
            print(f"❌ Error: {e}")
            results_summary.append({
                "category": scenario['category'],
                "decision": "error",
                "sources": []
            })

    # Summary
    print(f"\n📈 TESTING SUMMARY:")
    print("-" * 40)
    approved = sum(1 for r in results_summary if r['decision'] == 'approved')
    rejected = sum(1 for r in results_summary if r['decision'] == 'rejected')
    errors = sum(1 for r in results_summary if r['decision'] == 'error')

    print(f"✅ Approved: {approved}")
    print(f"❌ Rejected: {rejected}")
    print(f"⚠️  Errors: {errors}")

def analyze_coverage_patterns(all_chunks, document_sources, embeddings):
    """Analyze what types of coverage exist across policies"""
    print(f"\n🎯 COVERAGE PATTERN ANALYSIS:")
    print("-" * 40)

    coverage_keywords = {
        "Surgery": ["surgery", "surgical", "operation", "procedure"],
        "Emergency": ["emergency", "urgent", "ambulance", "trauma"],
        "Maternity": ["pregnancy", "maternity", "delivery", "childbirth"],
        "Mental Health": ["mental", "psychological", "therapy", "counseling"],
        "Dental": ["dental", "teeth", "oral", "dentist"],
        "Vision": ["eye", "vision", "optical", "glasses"],
        "Accidents": ["accident", "injury", "fall", "collision"],
        "Chronic Conditions": ["diabetes", "hypertension", "chronic", "ongoing"],
        "Preventive Care": ["preventive", "screening", "checkup", "vaccination"]
    }

    print("Searching for coverage types across all policies...")

    for coverage_type, keywords in coverage_keywords.items():
        print(f"\n🔍 {coverage_type}:")

        # Search for each keyword set
        for keyword in keywords:
            relevant_chunks = semantic_search(keyword, all_chunks, embeddings, top_k=2)

            if relevant_chunks:
                # Get sources
                sources = []
                for chunk in relevant_chunks:
                    try:
                        idx = all_chunks.index(chunk)
                        sources.append(document_sources[idx])
                    except ValueError:
                        pass

                unique_sources = list(set(sources))
                if unique_sources:
                    print(f"  📄 Found in: {', '.join(unique_sources)}")
                    break
        else:
            print(f"  ❌ Not clearly covered")

def create_policy_comparison_report():
    """Create a detailed comparison report"""
    print(f"\n📋 CREATING POLICY COMPARISON REPORT...")

    try:
        all_chunks, document_sources = process_multiple_documents("docs")

        report = {
            "total_policies": len(set(document_sources)),
            "total_clauses": len(all_chunks),
            "policies": {}
        }

        # Analyze each policy
        for doc in set(document_sources):
            doc_chunks = [chunk for i, chunk in enumerate(all_chunks) if document_sources[i] == doc]

            report["policies"][doc] = {
                "clauses": len(doc_chunks),
                "sample_content": doc_chunks[0][:200] + "..." if doc_chunks else "No content"
            }

        # Save report
        with open("policy_analysis_report.json", "w") as f:
            json.dump(report, f, indent=2)

        print("✅ Report saved to 'policy_analysis_report.json'")

    except Exception as e:
        print(f"❌ Error creating report: {e}")

if __name__ == "__main__":
    analyze_policy_collection()
    create_policy_comparison_report()
