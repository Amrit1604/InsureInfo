"""
💬 FRIENDLY CLAIMS CHAT
Talk to your insurance like you're talking to a friend!
"""

import streamlit as st
import json
from enhanced_system import EnhancedClaimsSystem
from smart_processor import SmartQueryProcessor

# Configure Streamlit for friendly interface
st.set_page_config(
    page_title="💬 Talk to Your Insurance",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for friendly design
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }

    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
        background-color: #f9f9f9;
    }

    .emergency-alert {
        background: linear-gradient(90deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }

    .approved {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }

    .rejected {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_insurance_data():
    """Load insurance policies once"""
    try:
        # Initialize the enhanced processor
        processor = EnhancedClaimsSystem()

        # Load documents using the processor
        success = processor.load_documents("docs")
        if success:
            return processor, True
        else:
            return None, False
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, False

def main():
    # Friendly header
    st.markdown("""
    <div class="main-header">
        <h1>💬 Talk to Your Insurance</h1>
        <p>Just tell us what happened - we speak human, not insurance jargon!</p>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    with st.spinner("🔄 Getting your insurance policies ready..."):
        processor, success = load_insurance_data()

    if not success:
        st.error("❌ Couldn't load your insurance policies. Please check your documents!")
        return

    st.success(f"✅ Your insurance policies are ready! We've got {len(processor.document_chunks)} text chunks loaded.")

    # Example prompts to help users
    st.markdown("### 💡 Not sure how to start? Try these examples:")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🏃 My kid hurt himself", help="Sports injury example"):
            st.session_state.user_input = "my 8 year old son fell off his bike and broke his arm we have had insurance for 3 years"

    with col2:
        if st.button("🚗 Car accident", help="Emergency situation"):
            st.session_state.user_input = "i was in a car accident broke my ribs ambulance took me to hospital i am 28 have insurance 2 years"

    with col3:
        if st.button("🏥 Need surgery", help="Medical procedure"):
            st.session_state.user_input = "my mom needs hip replacement surgery she is 65 we have old insurance policy"

    st.markdown("---")

    # Main chat interface
    st.markdown("### 💬 Tell us what happened:")

    user_input = st.text_area(
        "Describe your situation in your own words:",
        value=getattr(st.session_state, 'user_input', ''),
        placeholder="Example: 'my daughter broke her leg playing soccer, she's 12 and we've had insurance for 4 years'",
        height=100,
        key="main_input"
    )

    # Smart hints
    if user_input:
        query_processor = SmartQueryProcessor()
        preview = query_processor.process_query(user_input)

        if preview['analysis']:
            st.info(f"🧠 I understand: {', '.join(preview['analysis'])}")

        if preview['is_emergency']:
            st.markdown("""
            <div class="emergency-alert">
                🚨 EMERGENCY SITUATION DETECTED!
                We'll prioritize your claim and consider emergency coverage provisions.
            </div>
            """, unsafe_allow_html=True)

    # Process button
    if st.button("🔍 Check My Coverage", type="primary", disabled=not user_input.strip()):
        analyze_claim(user_input, processor)

def analyze_claim(user_input, processor):
    """Analyze the user's claim with friendly output"""

    with st.spinner("🤖 Checking your coverage... This might take a moment!"):
        try:
            # Process the claim using the intelligent processor
            result = processor.process_claim_query(user_input)

            # Display results in friendly way
            st.markdown("---")
            st.markdown("## 📋 Your Coverage Analysis")

            # Decision
            if result['decision'] == 'approved':
                st.markdown("""
                <div class="approved">
                    <h2>🎉 GREAT NEWS! Your claim looks like it will be covered!</h2>
                </div>
                """, unsafe_allow_html=True)
            elif result['decision'] == 'rejected':
                st.markdown("""
                <div class="rejected">
                    <h2>😔 Sorry, this claim might not be covered</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ We had trouble analyzing your claim. Please contact customer service.")

            # Healthcare Assistance Section
            st.markdown("---")
            st.markdown("## 🏥 Healthcare Assistance")

            # Location detected
            if result.get('location_detected') and result['location_detected'] != 'Not specified':
                st.info(f"📍 **Location detected:** {result['location_detected']}")

            # Nearby hospitals
            if result.get('nearby_hospitals'):
                st.markdown("### 🏥 Recommended Hospitals/Medical Centers:")
                for i, hospital in enumerate(result['nearby_hospitals'], 1):
                    st.write(f"{i}. {hospital}")

            # Emergency contacts
            if result.get('emergency_contacts'):
                st.markdown("### � Emergency Contacts:")
                emergency_col1, emergency_col2 = st.columns(2)
                with emergency_col1:
                    for i, contact in enumerate(result['emergency_contacts'][:len(result['emergency_contacts'])//2]):
                        st.write(f"• {contact}")
                with emergency_col2:
                    for contact in result['emergency_contacts'][len(result['emergency_contacts'])//2:]:
                        st.write(f"• {contact}")

            # Immediate care tips
            if result.get('immediate_care_tips'):
                st.markdown("### 💡 Immediate Care Tips:")
                for i, tip in enumerate(result['immediate_care_tips'], 1):
                    st.write(f"{i}. {tip}")

            # Specialist recommendation
            if result.get('specialist_recommendation'):
                st.success(f"👨‍⚕️ **Specialist Recommended:** {result['specialist_recommendation']}")

            # Policy-specific information
            if result.get('policy_specific_info'):
                st.info(f"🏛️ **Bajaj Allianz Info:** {result['policy_specific_info']}")

            # Policy details
            if result.get('policy_name'):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Policy:** {result['policy_name']}")
                with col2:
                    if result.get('policy_uin'):
                        st.write(f"**UIN:** {result['policy_uin']}")

            # User-friendly explanation
            if result.get('user_friendly_explanation'):
                st.markdown("### 💬 Coverage Details:")
                st.markdown(f"""
                <div class="chat-message">
                    {result['user_friendly_explanation']}
                </div>
                """, unsafe_allow_html=True)

            # Emergency override
            if result.get('emergency_override'):
                st.success("🚨 Emergency provisions applied - some waiting periods may be waived!")

            # Show what the AI understood
            with st.expander("🧠 How the AI understood your situation"):
                st.write(f"**You said:** {user_input}")
                if result.get('processed_query'):
                    st.write(f"**AI processed it as:** {result['processed_query']}")
                if result.get('is_emergency'):
                    st.write("**Emergency detected:** Yes - prioritized processing")

            # Technical details (collapsed by default)
            with st.expander("📄 Policy Details (for the curious)"):
                st.write("**Detailed AI reasoning:**")
                st.write(result['justification'])

                if result.get('relevant_documents'):
                    st.write("**Policy documents consulted:**")
                    for doc in result['relevant_documents']:
                        st.write(f"• {doc}")

                if result.get('clauses_analyzed'):
                    st.write(f"**Number of clauses analyzed:** {result['clauses_analyzed']}")

            # What to do next
            st.markdown("### 🎯 What should you do next?")

            if result['decision'] == 'approved':
                st.success("""
                **Next Steps:**
                1. 📞 Contact your insurance company to file the official claim
                2. 📋 Gather any medical reports or bills
                3. 📝 Mention this AI pre-analysis showed coverage eligibility
                4. ⏰ File as soon as possible for faster processing
                """)
            else:
                st.info("""
                **Next Steps:**
                1. 📞 Call customer service to discuss your specific situation
                2. 📋 Ask about any alternative coverage options
                3. 📝 Mention any emergency circumstances
                4. 🔍 Consider if there are other policies that might apply
                """)

        except Exception as e:
            st.error(f"😕 Something went wrong: {str(e)}")
            st.info("💡 Try rephrasing your situation or contact customer service for help!")

if __name__ == "__main__":
    main()
