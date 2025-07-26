"""
Enhanced Insurance Claims System with Real Policy Data and Web Search
"""

import os
import json
import re
from main import IntelligentClaimsProcessor
import google.generativeai as genai
from dotenv import load_dotenv

class EnhancedClaimsSystem(IntelligentClaimsProcessor):
    def __init__(self):
        super().__init__()

        # Policy-specific data extracted from actual document
        self.policy_data = {
            'waiting_periods': {
                'general_illness': 30,  # 30 days
                'specified_diseases': 90,  # 90 days
                'accidents': 0,  # No waiting period
                'emergency': 0   # No waiting period
            },
            'coverage_types': [
                'inpatient hospitalization',
                'surgery',
                'emergency treatment',
                'accident coverage',
                'cardiac procedures',
                'orthopedic treatment',
                'cancer treatment',
                'maternity benefits',
                'kidney treatment',
                'liver treatment'
            ],
            'exclusions': [
                'pre-existing conditions (first 48 months)',
                'cosmetic surgery',
                'dental treatment (unless accident)',
                'experimental treatments'
            ]
        }

    def get_web_info_with_gemini(self, query, location=None):
        """Use Gemini API to search for real-time information"""
        try:
            search_prompt = f"""
            You are a helpful assistant that provides accurate, up-to-date information about hospitals and emergency services.

            Query: {query}
            Location: {location if location else 'India'}

            Please provide:
            1. Top 3-5 relevant hospitals/medical centers for this condition in the specified location
            2. Emergency contact numbers for the area
            3. 3-5 practical immediate care tips for this medical condition

            Be concise and accurate. Format your response as JSON:
            {{
                "hospitals": ["hospital1", "hospital2", "hospital3"],
                "emergency_contacts": ["contact1", "contact2"],
                "care_tips": ["tip1", "tip2", "tip3"]
            }}
            """

            response = self.llm.generate_content(search_prompt)
            response_text = response.text.strip()

            # Clean JSON response
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            return json.loads(response_text)

        except Exception as e:
            return {
                "hospitals": ["Contact customer service for hospital network information"],
                "emergency_contacts": ["108 (Emergency)", "100 (Police)", "101 (Fire)"],
                "care_tips": ["Seek medical attention immediately", "Follow doctor's instructions"]
            }

    def enhanced_evaluate_claim(self, original_query, enhanced_query, is_emergency, relevant_chunks, document_sources):
        """Enhanced claim evaluation with real policy data"""

        # Extract key information from query
        location = self.extract_location(original_query)
        medical_condition = self.extract_medical_condition(original_query)
        policy_age_months = self.extract_policy_age(original_query)

        # Get web information
        web_info = self.get_web_info_with_gemini(
            f"{medical_condition} treatment hospitals",
            location
        )

        # Policy-based decision logic
        decision = self.make_policy_decision(
            medical_condition, policy_age_months, is_emergency
        )

        return {
            "decision": decision['status'],
            "justification": decision['reason'],
            "user_friendly_explanation": decision['explanation'],
            "emergency_override": is_emergency,
            "location_detected": location or "Not specified",
            "nearby_hospitals": web_info.get('hospitals', [])[:3],  # Limit to 3
            "emergency_contacts": web_info.get('emergency_contacts', [])[:3],
            "immediate_care_tips": web_info.get('care_tips', [])[:3],
            "specialist_recommendation": self.get_specialist_for_condition(medical_condition),
            "processed_query": enhanced_query,
            "emergency_detected": is_emergency,
            "clauses_analyzed": len(relevant_chunks)
        }

    def extract_location(self, query):
        """Extract location from query"""
        cities = ['pune', 'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad',
                 'kolkata', 'ahmedabad', 'jaipur', 'lucknow', 'kanpur', 'nagpur']

        query_lower = query.lower()
        for city in cities:
            if city in query_lower:
                return city.title()
        return None

    def extract_medical_condition(self, query):
        """Extract medical condition from query"""
        conditions = {
            'knee': 'knee injury/surgery',
            'heart': 'cardiac condition',
            'surgery': 'surgical procedure',
            'accident': 'accidental injury',
            'fracture': 'bone fracture',
            'cancer': 'cancer treatment',
            'diabetes': 'diabetes management',
            'kidney': 'kidney treatment',
            'liver': 'liver condition',
            'pregnancy': 'maternity care',
            'emergency': 'emergency treatment'
        }

        query_lower = query.lower()
        for keyword, condition in conditions.items():
            if keyword in query_lower:
                return condition
        return 'general medical condition'

    def extract_policy_age(self, query):
        """Extract policy age from query"""
        # Look for patterns like "3 month", "2 year", etc.
        month_match = re.search(r'(\d+)\s*month', query.lower())
        year_match = re.search(r'(\d+)\s*year', query.lower())

        if month_match:
            return int(month_match.group(1))
        elif year_match:
            return int(year_match.group(1)) * 12
        return 6  # Default assumption

    def make_policy_decision(self, condition, policy_age_months, is_emergency):
        """Make decision based on actual policy rules"""

        # Emergency or accident - always approve
        if is_emergency or 'accident' in condition.lower():
            return {
                'status': 'approved',
                'reason': 'Emergency/accident coverage - no waiting period applies',
                'explanation': 'Your claim is approved. Emergency and accidental injuries are covered immediately.'
            }

        # Check waiting periods
        if 'cardiac' in condition or 'heart' in condition:
            if policy_age_months < 90:
                return {
                    'status': 'rejected',
                    'reason': f'Cardiac conditions have 90-day waiting period. Policy age: {policy_age_months} months',
                    'explanation': 'Cardiac procedures require a 90-day waiting period. Please reapply after this period.'
                }

        # General illness waiting period
        if policy_age_months < 1:  # Less than 30 days
            return {
                'status': 'rejected',
                'reason': f'30-day waiting period for illnesses. Policy age: {policy_age_months} months',
                'explanation': 'General medical conditions have a 30-day waiting period. Please wait until this period expires.'
            }

        # Approve if all checks pass
        return {
            'status': 'approved',
            'reason': f'Condition covered under policy. Policy age: {policy_age_months} months meets requirements.',
            'explanation': 'Your claim is approved based on your policy coverage and waiting period completion.'
        }

    def get_specialist_for_condition(self, condition):
        """Get appropriate specialist for condition"""
        specialists = {
            'knee': 'Orthopedic Surgeon',
            'cardiac': 'Cardiologist',
            'heart': 'Cardiologist',
            'cancer': 'Oncologist',
            'kidney': 'Nephrologist',
            'liver': 'Hepatologist',
            'pregnancy': 'Gynecologist',
            'emergency': 'Emergency Medicine Specialist',
            'fracture': 'Orthopedic Surgeon'
        }

        for keyword, specialist in specialists.items():
            if keyword in condition.lower():
                return specialist
        return 'General Physician'

    def process_claim_query(self, query):
        """Override parent method with enhanced processing"""
        print(f"\n🔄 Processing enhanced claim: {query}")

        # Use parent's smart processing
        processed_query_info = self.smart_processor.process_query(query)
        enhanced_query = processed_query_info['processed']
        is_emergency = processed_query_info['is_emergency']

        print(f"✨ Enhanced understanding: {enhanced_query}")
        if is_emergency:
            print("🚨 EMERGENCY - Fast processing!")

        # Get relevant chunks
        relevant_chunks, relevant_sources = self.semantic_search(enhanced_query)

        if not relevant_chunks:
            return self.get_default_error_response()

        # Use enhanced evaluation
        return self.enhanced_evaluate_claim(
            query, enhanced_query, is_emergency, relevant_chunks, relevant_sources
        )

    def get_default_error_response(self):
        """Default response for errors"""
        return {
            "decision": "error",
            "justification": "Unable to process claim",
            "user_friendly_explanation": "Please contact customer service for assistance",
            "location_detected": "Not specified",
            "nearby_hospitals": ["Contact customer service"],
            "emergency_contacts": ["108 (Emergency)", "100 (Police)", "101 (Fire)"],
            "immediate_care_tips": ["Seek medical attention", "Contact customer service"],
            "specialist_recommendation": "General Physician"
        }

# Quick test function
def test_enhanced_system():
    """Test the enhanced system"""
    system = EnhancedClaimsSystem()

    if not system.load_documents("docs"):
        print("❌ Failed to load documents")
        return

    # Test queries
    test_queries = [
        "knee surgery in Pune, 3 month old policy",
        "heart attack emergency in Mumbai, 6 month policy",
        "accident fracture in Delhi, 1 month policy"
    ]

    for query in test_queries:
        print(f"\n{'='*60}")
        result = system.process_claim_query(query)
        system.display_decision(result)
        print(f"{'='*60}")

if __name__ == "__main__":
    test_enhanced_system()
