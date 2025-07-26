import streamlit as st
import json
from main import extract_text_from_file, chunk_text, get_embeddings, semantic_search, ask_llm
import os

@st.cache_data
def load_document_data():
    """Load and process the policy document once"""
    file_path = "docs/sample_policy.pdf"
    if not os.path.exists(file_path):
        return None, None, None

    text = extract_text_from_file(file_path)
    chunks = chunk_text(text)
    embeddings = get_embeddings(chunks)
    return text, chunks, embeddings

def main():
    st.title("🏥 LLM Claims Processing System")
    st.markdown("---")

    # Load document data
    with st.spinner("Loading policy document..."):
        text, chunks, embeddings = load_document_data()

    if text is None:
        st.error("Could not load policy document!")
        return

    st.success(f"✅ Policy loaded: {len(chunks)} clauses indexed")

    # Input section
    st.header("Submit a Claim Query")

    # Example queries
    example_queries = [
        "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
        "25-year-old female, dental treatment, Mumbai, 6-month policy",
        "60-year-old male, heart surgery, emergency, Delhi, 2-year policy",
        "35-year-old male, eye surgery, elective, Bangalore, 1-year policy"
    ]

    selected_example = st.selectbox("Or choose an example:", [""] + example_queries)

    user_query = st.text_area(
        "Enter your claim details:",
        value=selected_example,
        placeholder="e.g., 46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
        height=100
    )

    if st.button("🔍 Process Claim", type="primary"):
        if user_query.strip():
            with st.spinner("Analyzing claim..."):
                try:
                    # Find relevant clauses
                    relevant_clauses = semantic_search(user_query, chunks, embeddings)

                    # Get LLM decision
                    result = ask_llm(user_query, relevant_clauses)

                    # Display results
                    st.markdown("---")
                    st.header("📋 Claim Analysis Result")

                    # Decision badge
                    if result['decision'] == 'approved':
                        st.success("✅ CLAIM APPROVED")
                    elif result['decision'] == 'rejected':
                        st.error("❌ CLAIM REJECTED")
                    else:
                        st.warning("⚠️ ERROR IN PROCESSING")

                    # Amount
                    if result.get('amount'):
                        st.metric("Eligible Amount", f"₹{result['amount']:,}")

                    # Justification
                    st.subheader("Justification")
                    st.write(result['justification'])

                    # Show relevant clauses
                    with st.expander("📄 Relevant Policy Clauses Used"):
                        for i, clause in enumerate(relevant_clauses, 1):
                            st.write(f"**Clause {i}:**")
                            st.write(clause[:500] + "..." if len(clause) > 500 else clause)
                            st.markdown("---")

                    # JSON output
                    with st.expander("🔧 Technical Details (JSON)"):
                        st.json(result)

                except Exception as e:
                    st.error(f"Error processing claim: {str(e)}")
        else:
            st.warning("Please enter a claim query!")

if __name__ == "__main__":
    main()
