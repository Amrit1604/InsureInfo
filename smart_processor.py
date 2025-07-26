"""
🧠 SMART QUERY PROCESSOR
Converts everyday language into proper insurance claim analysis
"""

import re
from datetime import datetime, timedelta

class SmartQueryProcessor:
    def __init__(self):
        # Common ways people describe ages
        self.age_patterns = {
            r'(\d+)\s*(?:year|yr)s?\s*old': r'\1-year-old',
            r'i\s*am\s*(\d+)': r'\1-year-old',
            r'my\s*age\s*is\s*(\d+)': r'\1-year-old',
            r'(\d+)\s*yrs?\s*old': r'\1-year-old',
            r'age\s*(\d+)': r'\1-year-old',
        }

        # Common casual medical terms to proper terms
        self.medical_mappings = {
            # Injuries
            'broke my arm': 'arm fracture',
            'broke my leg': 'leg fracture',
            'broke my hand': 'hand fracture',
            'twisted my ankle': 'ankle sprain',
            'hurt my back': 'back injury',
            'torn muscle': 'muscle tear',
            'pulled muscle': 'muscle strain',
            'dislocated': 'dislocation',
            'cut myself': 'laceration',
            'burned': 'burn injury',
            'fell down': 'fall injury',
            'car accident': 'motor vehicle accident',
            'bike accident': 'bicycle accident',
            'sports injury': 'athletic injury',

            # Body parts (casual to medical)
            'tummy': 'abdomen',
            'belly': 'abdomen',
            'stomach': 'abdomen',
            'chest': 'thoracic',
            'neck': 'cervical',
            'lower back': 'lumbar spine',
            'upper back': 'thoracic spine',

            # Common conditions
            'heart attack': 'myocardial infarction',
            'stroke': 'cerebrovascular accident',
            'diabetes': 'diabetes mellitus',
            'high blood pressure': 'hypertension',
            'can\'t breathe': 'respiratory distress',
            'chest pain': 'chest pain syndrome',
            'headache': 'cephalgia',
            'dizzy': 'dizziness',
            'nauseous': 'nausea',
            'throwing up': 'vomiting',
            'can\'t sleep': 'insomnia',
            'depressed': 'depression',
            'anxious': 'anxiety',
            'stressed': 'stress disorder',

            # Treatments
            'operation': 'surgery',
            'stitches': 'sutures',
            'cast': 'immobilization',
            'x-ray': 'radiography',
            'scan': 'imaging',
            'blood test': 'laboratory tests',
            'checkup': 'examination',
            'shots': 'vaccination',
            'medicine': 'medication',
            'pills': 'medication',
            'therapy': 'treatment',
        }

        # Policy duration patterns
        self.policy_patterns = {
            r'(\d+)\s*month\s*old\s*policy': r'\1-month policy',
            r'(\d+)\s*year\s*old\s*policy': r'\1-year policy',
            r'had\s*insurance\s*for\s*(\d+)\s*months?': r'\1-month policy',
            r'had\s*insurance\s*for\s*(\d+)\s*years?': r'\1-year policy',
            r'policy\s*is\s*(\d+)\s*months?\s*old': r'\1-month policy',
            r'policy\s*is\s*(\d+)\s*years?\s*old': r'\1-year policy',
            r'new\s*policy': '1-month policy',
            r'recent\s*policy': '3-month policy',
            r'old\s*policy': '5-year policy',
        }

        # Family member patterns
        self.family_patterns = {
            'my kid': 'child',
            'my son': 'child',
            'my daughter': 'child',
            'my baby': 'infant',
            'my mom': 'parent',
            'my dad': 'parent',
            'my mother': 'parent',
            'my father': 'parent',
            'my wife': 'spouse',
            'my husband': 'spouse',
            'my grandma': 'elderly family member',
            'my grandpa': 'elderly family member',
        }

        # Emergency indicators
        self.emergency_keywords = [
            'emergency', 'urgent', 'ambulance', 'hospital', 'ER', 'emergency room',
            'rushed to', 'immediately', 'couldn\'t wait', 'life threatening',
            'severe pain', 'intense pain', 'unbearable', 'critical'
        ]

    def process_query(self, raw_query):
        """Transform everyday language into proper insurance query"""

        # Store original for reference
        original_query = raw_query.strip()
        processed_query = original_query.lower()

        # Extract and normalize age
        processed_query = self._normalize_age(processed_query)

        # Normalize medical terms
        processed_query = self._normalize_medical_terms(processed_query)

        # Normalize policy duration
        processed_query = self._normalize_policy_duration(processed_query)

        # Handle family members
        processed_query = self._normalize_family_references(processed_query)

        # Detect emergency context
        is_emergency = self._detect_emergency(processed_query)

        # Generate enhanced query
        enhanced_query = self._enhance_query(processed_query, is_emergency)

        return {
            'original': original_query,
            'processed': enhanced_query,
            'is_emergency': is_emergency,
            'analysis': self._generate_analysis(original_query, enhanced_query)
        }

    def _normalize_age(self, text):
        """Extract and normalize age expressions"""
        for pattern, replacement in self.age_patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _normalize_medical_terms(self, text):
        """Convert casual medical terms to proper terms"""
        for casual, proper in self.medical_mappings.items():
            text = re.sub(r'\b' + re.escape(casual) + r'\b', proper, text, flags=re.IGNORECASE)
        return text

    def _normalize_policy_duration(self, text):
        """Extract and normalize policy duration"""
        for pattern, replacement in self.policy_patterns.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def _normalize_family_references(self, text):
        """Handle family member references"""
        for family_term, replacement in self.family_patterns.items():
            text = re.sub(r'\b' + re.escape(family_term) + r'\b', replacement, text, flags=re.IGNORECASE)
        return text

    def _detect_emergency(self, text):
        """Detect if this is an emergency situation"""
        return any(keyword in text.lower() for keyword in self.emergency_keywords)

    def _enhance_query(self, processed_query, is_emergency):
        """Generate enhanced query with medical context"""
        enhanced = processed_query

        # Add emergency context if detected
        if is_emergency:
            enhanced = f"EMERGENCY: {enhanced}"

        # Add medical necessity context
        if any(word in enhanced for word in ['surgery', 'operation', 'treatment']):
            enhanced = f"Medically necessary {enhanced}"

        return enhanced

    def _generate_analysis(self, original, enhanced):
        """Generate analysis of what was understood"""
        changes = []

        if original.lower() != enhanced.lower():
            changes.append("Converted casual language to medical terminology")

        if 'emergency' in enhanced.lower() and 'emergency' not in original.lower():
            changes.append("Detected emergency situation")

        if any(term in enhanced for term in ['fracture', 'sprain', 'tear']):
            changes.append("Identified specific injury type")

        return changes


def smart_claims_analyzer():
    """Demo of smart query processing"""

    processor = SmartQueryProcessor()

    # Real examples of how people actually talk
    real_user_queries = [
        "hey my kid broke his arm playing soccer and we have had insurance for 2 years",
        "I am 25 and hurt my back lifting weights, insurance is 6 months old",
        "my mom fell down stairs broke her hip emergency surgery needed policy 4 years old",
        "car accident broke my leg ambulance to hospital i am 30 policy is 1 year",
        "my baby has fever throwing up rushed to ER we have new insurance",
        "twisted ankle playing basketball am 22 had insurance 3 years",
        "my wife needs operation for stomach pain she is 28 old policy",
        "can't breathe chest pain went to emergency room age 45 insurance 2 years",
        "my son cut himself needs stitches he is 8 insurance 5 years old",
        "fell off bike broke my wrist am 19 have insurance 3 months"
    ]

    print("🧠 SMART QUERY PROCESSOR DEMO")
    print("=" * 50)
    print("See how the AI understands everyday language!\n")

    for i, query in enumerate(real_user_queries, 1):
        print(f"📝 Example {i}:")
        print(f"User said: \"{query}\"")

        result = processor.process_query(query)

        print(f"🧠 AI understood: \"{result['processed']}\"")

        if result['is_emergency']:
            print("🚨 EMERGENCY DETECTED!")

        if result['analysis']:
            print(f"✨ Intelligence applied: {', '.join(result['analysis'])}")

        print("-" * 50)


if __name__ == "__main__":
    smart_claims_analyzer()
