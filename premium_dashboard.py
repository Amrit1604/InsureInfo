"""
🚀 PREMIUM CLAIMS ANALYSIS DASHBOARD
Real policy documents with advanced AI analysis!
"""

import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from main import process_multiple_documents, get_embeddings, semantic_search, ask_llm
import numpy as np

# Configure Streamlit
st.set_page_config(
    page_title="AI Claims Analyzer Pro",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_policy_data():
    """Load and cache all policy data"""
    try:
        all_chunks, document_sources = process_multiple_documents("docs")
        embeddings = get_embeddings(all_chunks)

        # Create policy stats
        policy_stats = {}
        for doc in set(document_sources):
            policy_stats[doc] = {
                'clauses': document_sources.count(doc),
                'chunks': [chunk for i, chunk in enumerate(all_chunks) if document_sources[i] == doc]
            }

        return all_chunks, document_sources, embeddings, policy_stats
    except Exception as e:
        st.error(f"Error loading policies: {e}")
        return None, None, None, None

def main():
    # Header
    st.title("🏥 AI-Powered Claims Analysis Dashboard")
    st.markdown("### Powered by Real Insurance Policy Documents + Gemini AI")
    st.markdown("---")

    # Load data
    with st.spinner("🔄 Loading and analyzing policy documents..."):
        all_chunks, document_sources, embeddings, policy_stats = load_policy_data()

    if all_chunks is None:
        st.error("Failed to load policy documents!")
        return

    # Sidebar
    st.sidebar.header("📊 Dashboard Controls")

    # Policy overview in sidebar
    st.sidebar.subheader("📚 Loaded Policies")
    total_policies = len(policy_stats)
    total_clauses = len(all_chunks)

    st.sidebar.metric("Total Policies", total_policies)
    st.sidebar.metric("Total Clauses", total_clauses)

    for policy, stats in policy_stats.items():
        with st.sidebar.expander(f"📋 {policy}"):
            st.write(f"Clauses: {stats['clauses']}")
            if stats['chunks']:
                st.write("Sample content:")
                st.write(stats['chunks'][0][:150] + "...")

    # Main dashboard tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Claims Analysis", "📊 Policy Insights", "🧪 Batch Testing", "📈 Analytics"])

    with tab1:
        claims_analysis_tab(all_chunks, document_sources, embeddings)

    with tab2:
        policy_insights_tab(policy_stats, all_chunks, document_sources, embeddings)

    with tab3:
        batch_testing_tab(all_chunks, document_sources, embeddings)

    with tab4:
        analytics_tab(policy_stats, all_chunks, document_sources)

def claims_analysis_tab(all_chunks, document_sources, embeddings):
    """Main claims analysis interface"""
    st.header("🔍 AI Claims Analyzer")

    # Quick test buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏃 Sports Injury Test"):
            st.session_state.test_query = "19-year-old athlete, torn ACL during basketball, 3-year policy"

    with col2:
        if st.button("🚗 Car Accident Test"):
            st.session_state.test_query = "25-year-old, broken ribs from car crash, 2-year policy"

    with col3:
        if st.button("🏥 Emergency Surgery Test"):
            st.session_state.test_query = "30-year-old, emergency appendectomy, 6-month policy"

    # Main query input
    query = st.text_area(
        "📝 Enter Claim Details:",
        value=getattr(st.session_state, 'test_query', ''),
        placeholder="e.g., 19-year-old with 5-year policy, fell and broke ligament",
        height=100
    )

    # Analysis parameters
    col1, col2 = st.columns(2)
    with col1:
        search_depth = st.slider("🔍 Search Depth (clauses to analyze)", 3, 10, 5)
    with col2:
        confidence_threshold = st.slider("🎯 Confidence Threshold", 0.5, 1.0, 0.7)

    if st.button("🚀 Analyze Claim", type="primary"):
        if query.strip():
            analyze_claim(query, all_chunks, document_sources, embeddings, search_depth)
        else:
            st.warning("Please enter a claim description!")

def analyze_claim(query, all_chunks, document_sources, embeddings, search_depth):
    """Analyze a single claim with detailed breakdown"""

    with st.spinner("🤖 AI is analyzing your claim..."):
        try:
            # Find relevant clauses
            relevant_chunks = semantic_search(query, all_chunks, embeddings, top_k=search_depth)

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
            result = ask_llm(query, relevant_chunks, relevant_sources)

            # Display results
            st.markdown("---")
            st.subheader("🎯 Analysis Results")

            # Decision with styling
            if result['decision'] == 'approved':
                st.success("✅ CLAIM APPROVED")
                decision_color = "green"
            elif result['decision'] == 'rejected':
                st.error("❌ CLAIM REJECTED")
                decision_color = "red"
            else:
                st.warning("⚠️ ANALYSIS ERROR")
                decision_color = "orange"

            # Metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Decision", result['decision'].upper())

            with col2:
                if result.get('amount'):
                    st.metric("Eligible Amount", f"₹{result['amount']:,}")
                else:
                    st.metric("Eligible Amount", "TBD")

            with col3:
                unique_sources = list(set(relevant_sources))
                st.metric("Policies Referenced", len(unique_sources))

            # Justification
            st.subheader("📋 AI Justification")
            st.write(result['justification'])

            # Source breakdown
            st.subheader("📄 Policy Sources Used")
            source_counts = {}
            for source in relevant_sources:
                source_counts[source] = source_counts.get(source, 0) + 1

            for source, count in source_counts.items():
                st.write(f"• **{source}**: {count} clause(s)")

            # Relevant clauses
            with st.expander("🔍 View Retrieved Clauses"):
                for i, (chunk, source) in enumerate(zip(relevant_chunks, relevant_sources), 1):
                    st.write(f"**Clause {i} (from {source}):**")
                    st.write(chunk)
                    st.markdown("---")

        except Exception as e:
            st.error(f"Analysis failed: {e}")

def policy_insights_tab(policy_stats, all_chunks, document_sources, embeddings):
    """Policy comparison and insights"""
    st.header("📊 Policy Intelligence Dashboard")

    # Policy comparison chart
    st.subheader("📈 Policy Size Comparison")

    policy_names = list(policy_stats.keys())
    clause_counts = [stats['clauses'] for stats in policy_stats.values()]

    fig = px.bar(
        x=policy_names,
        y=clause_counts,
        title="Number of Clauses per Policy",
        labels={'x': 'Policy Document', 'y': 'Number of Clauses'}
    )
    fig.update_traces(marker_color='lightblue')
    st.plotly_chart(fig, use_container_width=True)

    # Coverage heatmap
    st.subheader("🎯 Coverage Analysis by Type")

    coverage_types = [
        "surgery", "emergency", "accident", "maternity",
        "dental", "vision", "mental health", "chronic conditions"
    ]

    coverage_matrix = []
    for policy in policy_names:
        policy_coverage = []
        policy_chunks = policy_stats[policy]['chunks']

        for coverage_type in coverage_types:
            # Simple keyword matching for demo
            coverage_found = any(coverage_type.lower() in chunk.lower() for chunk in policy_chunks[:10])  # Sample first 10 chunks
            policy_coverage.append(1 if coverage_found else 0)

        coverage_matrix.append(policy_coverage)

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=coverage_matrix,
        x=coverage_types,
        y=policy_names,
        colorscale='RdYlGn',
        showscale=True
    ))
    fig.update_layout(
        title="Policy Coverage Heatmap",
        xaxis_title="Coverage Type",
        yaxis_title="Policy Document"
    )
    st.plotly_chart(fig, use_container_width=True)

def batch_testing_tab(all_chunks, document_sources, embeddings):
    """Batch testing interface"""
    st.header("🧪 Batch Claims Testing")

    st.write("Test multiple claims at once to understand policy patterns!")

    # Predefined test scenarios
    test_scenarios = [
        "19-year-old, ligament injury, 5-year policy",
        "25-year-old, car accident surgery, 2-year policy",
        "30-year-old, emergency appendectomy, 6-month policy",
        "45-year-old, diabetes medication, 4-year policy",
        "22-year-old, mental health therapy, 3-year policy",
        "35-year-old, maternity care, 1-year policy",
        "28-year-old, dental implant, 3-year policy",
        "40-year-old, eye surgery, 2-year policy"
    ]

    if st.button("🚀 Run Batch Test"):
        results = []
        progress_bar = st.progress(0)

        for i, scenario in enumerate(test_scenarios):
            with st.spinner(f"Testing scenario {i+1}/{len(test_scenarios)}..."):
                try:
                    relevant_chunks = semantic_search(scenario, all_chunks, embeddings)
                    relevant_indices = []
                    for chunk in relevant_chunks:
                        try:
                            idx = all_chunks.index(chunk)
                            relevant_indices.append(idx)
                        except ValueError:
                            relevant_indices.append(0)

                    relevant_sources = [document_sources[idx] for idx in relevant_indices]
                    result = ask_llm(scenario, relevant_chunks, relevant_sources)

                    results.append({
                        "Scenario": scenario,
                        "Decision": result['decision'],
                        "Amount": result.get('amount', 'N/A'),
                        "Sources": len(set(relevant_sources))
                    })

                except Exception as e:
                    results.append({
                        "Scenario": scenario,
                        "Decision": "error",
                        "Amount": "N/A",
                        "Sources": 0
                    })

                progress_bar.progress((i + 1) / len(test_scenarios))

        # Display results
        st.subheader("📊 Batch Test Results")
        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        # Summary stats
        col1, col2, col3 = st.columns(3)

        with col1:
            approved = len(df[df['Decision'] == 'approved'])
            st.metric("Approved Claims", approved)

        with col2:
            rejected = len(df[df['Decision'] == 'rejected'])
            st.metric("Rejected Claims", rejected)

        with col3:
            error_rate = len(df[df['Decision'] == 'error']) / len(df) * 100
            st.metric("Error Rate", f"{error_rate:.1f}%")

def analytics_tab(policy_stats, all_chunks, document_sources):
    """Advanced analytics and insights"""
    st.header("📈 Advanced Analytics")

    # Document length distribution
    st.subheader("📊 Document Analysis")

    lengths = []
    names = []
    for policy, stats in policy_stats.items():
        total_length = sum(len(chunk) for chunk in stats['chunks'])
        lengths.append(total_length)
        names.append(policy)

    fig = px.pie(
        values=lengths,
        names=names,
        title="Content Distribution Across Policies"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Word frequency analysis
    st.subheader("🔤 Key Terms Analysis")

    # Simple word frequency for all documents
    all_text = " ".join(all_chunks).lower()
    key_terms = ["coverage", "exclusion", "benefit", "claim", "treatment", "surgery", "emergency", "accident"]

    term_counts = []
    for term in key_terms:
        count = all_text.count(term)
        term_counts.append(count)

    fig = px.bar(
        x=key_terms,
        y=term_counts,
        title="Frequency of Key Insurance Terms",
        labels={'x': 'Terms', 'y': 'Frequency'}
    )
    fig.update_traces(marker_color='lightcoral')
    st.plotly_chart(fig, use_container_width=True)

    # Download reports
    st.subheader("📥 Export Data")
    if st.button("Generate Comprehensive Report"):
        report_data = {
            "total_policies": len(policy_stats),
            "total_clauses": len(all_chunks),
            "policy_breakdown": {k: v['clauses'] for k, v in policy_stats.items()},
            "term_frequencies": dict(zip(key_terms, term_counts))
        }

        st.download_button(
            label="📄 Download JSON Report",
            data=json.dumps(report_data, indent=2),
            file_name="policy_analysis_report.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
