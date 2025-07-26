"""
Enhanced Insurance Claims System - Standalone Version
Real policy data + Gemini web search + Hospitality assistance
"""

import os
import json
import re
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from utils import extract_text_from_file, chunk_text
from smart_processor import SmartQueryProcessor
import google.generativeai as genai
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

class CleanEnhancedSystem:
    def __init__(self):
        """Initialize the enhanced claims system"""
        # Load environment variables
        load_dotenv()

        # Check API key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print(f"{Fore.RED}❌ Error: GOOGLE_API_KEY not found!")
            exit(1)

        # Configure Gemini AI
        genai.configure(api_key=self.api_key)
        self.llm = genai.GenerativeModel("gemini-1.5-flash")

        # Initialize components
        self.smart_processor = SmartQueryProcessor()
        self.sentence_model = SentenceTransformer("all-MiniLM-L6-v2")

        # Document processing variables
        self.document_chunks = []
        self.document_sources = []
        self.embeddings = None

        # Real policy data extracted from actual document
        self.policy_data = {
            'waiting_periods': {
                'general_illness': 30,  # 30 days
                'cardiac_conditions': 90,  # 90 days
                'accidents': 0,  # No waiting period
                'emergency': 0   # No waiting period
            },
            'covered_conditions': [
                'surgery', 'heart', 'cardiac', 'orthopedic', 'bone', 'fracture',
                'emergency', 'accident', 'cancer', 'kidney', 'liver', 'maternity'
            ]
        }

        print(f"{Fore.GREEN}✅ Enhanced Claims System initialized!")

    def load_documents(self, docs_folder="docs"):
        """Load and process policy documents"""
        print(f"\n{Fore.CYAN}📚 Loading policy documents...")

        try:
            all_chunks, document_sources = self._process_documents(docs_folder)

            if not all_chunks:
                print(f"{Fore.RED}❌ No documents found!")
                return False

            self.document_chunks = all_chunks
            self.document_sources = document_sources

            # Generate embeddings
            print(f"{Fore.YELLOW}🧠 Generating embeddings...")
            self.embeddings = self.sentence_model.encode(self.document_chunks)

            print(f"{Fore.GREEN}✅ Loaded {len(self.document_chunks)} chunks")
            return True

        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")
            return False

    def _process_documents(self, docs_folder):
        """Process policy documents"""
        all_chunks = []
        document_sources = []

        if not os.path.exists(docs_folder):
            raise ValueError(f"Folder '{docs_folder}' not found!")

        supported_extensions = ['.pdf', '.docx']
        files = []

        for file in os.listdir(docs_folder):
            file_path = os.path.join(docs_folder, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                if ext in supported_extensions:
                    files.append((file, file_path))

        for filename, file_path in files:
            try:
                print(f"   📄 Processing: {filename}")
                text = extract_text_from_file(file_path)
                chunks = chunk_text(text)

                for chunk in chunks:
                    all_chunks.append(chunk)
                    document_sources.append(filename)

                print(f"      → {len(chunks)} chunks")

            except Exception as e:
                print(f"      → ❌ Error: {e}")
                continue

        return all_chunks, document_sources

    def semantic_search(self, query, top_k=5):
        """Semantic search in documents"""
        if not self.embeddings.size:
            return [], []

        query_emb = self.sentence_model.encode([query])
        embeddings = self.embeddings.astype('float32')
        query_emb = query_emb.astype('float32')

        # FAISS search
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        distances, indices = index.search(query_emb, top_k)

        chunks = [self.document_chunks[i] for i in indices[0]]
        sources = [self.document_sources[i] for i in indices[0]]

        return chunks, sources

    def get_web_info(self, query, location=None):
        """Get real-time info using Gemini"""
        try:
            search_prompt = f"""
            Provide current information for: {query}
            Location: {location if location else 'India'}

            Return JSON format:
            {{
                "hospitals": ["hospital1 with area", "hospital2 with area", "hospital3 with area"],
                "emergency_contacts": ["108 - Emergency Ambulance", "112 - National Emergency", "100 - Police"],
                "care_tips": ["tip1", "tip2", "tip3"]
            }}

            Be concise and accurate. Include actual hospital names for the location.
            """

            response = self.llm.generate_content(search_prompt)
            response_text = response.text.strip()

            # Clean JSON
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            return json.loads(response_text)

        except Exception as e:
            return {
                "hospitals": ["Contact insurance helpline for network hospitals"],
                "emergency_contacts": ["108 - Emergency", "100 - Police", "101 - Fire"],
                "care_tips": ["Seek immediate medical attention", "Follow doctor's instructions"]
            }

    def process_claim_query(self, query):
        """Process claim with enhanced analysis"""
        print(f"\n{Fore.CYAN}🔄 Processing: {query}")

        # Smart processing
        processed_info = self.smart_processor.process_query(query)
        enhanced_query = processed_info['processed']
        is_emergency = processed_info['is_emergency']

        print(f"{Fore.GREEN}✨ Understanding: {enhanced_query}")
        if is_emergency:
            print(f"{Fore.RED}🚨 EMERGENCY detected!")

        # Search relevant chunks
        relevant_chunks, relevant_sources = self.semantic_search(enhanced_query)

        if not relevant_chunks:
            return self._get_error_response()

        # Enhanced evaluation
        return self._evaluate_claim(query, enhanced_query, is_emergency, relevant_chunks)

    def _evaluate_claim(self, original_query, enhanced_query, is_emergency, relevant_chunks):
        """Evaluate claim with real policy rules and web search"""

        # Extract information
        location = self._extract_location(original_query)
        condition = self._extract_condition(original_query)
        policy_age = self._extract_policy_age(original_query)

        # Get web info
        web_info = self.get_web_info(f"{condition} hospitals", location)

        # Policy decision
        decision = self._make_decision(condition, policy_age, is_emergency)

        return {
            "decision": decision['status'],
            "justification": decision['reason'],
            "user_friendly_explanation": decision['explanation'],
            "emergency_override": is_emergency,
            "location_detected": location or "Not specified",
            "nearby_hospitals": web_info.get('hospitals', [])[:3],
            "emergency_contacts": web_info.get('emergency_contacts', [])[:3],
            "immediate_care_tips": web_info.get('care_tips', [])[:3],
            "specialist_recommendation": self._get_specialist(condition),
            "processed_query": enhanced_query,
            "clauses_analyzed": len(relevant_chunks)
        }

    def _extract_location(self, query):
        """Extract location from query"""
        cities = ['pune', 'mumbai', 'delhi', 'bangalore', 'chennai', 'hyderabad',
                 'kolkata', 'ahmedabad', 'jaipur', 'lucknow']

        query_lower = query.lower()
        for city in cities:
            if city in query_lower:
                return city.title()
        return None

    def _extract_condition(self, query):
        """Extract medical condition"""
        conditions = {
            'knee': 'knee surgery',
            'heart': 'cardiac condition',
            'surgery': 'surgical procedure',
            'accident': 'accidental injury',
            'fracture': 'bone fracture',
            'cancer': 'cancer treatment',
            'kidney': 'kidney treatment',
            'emergency': 'emergency treatment'
        }

        query_lower = query.lower()
        for keyword, condition in conditions.items():
            if keyword in query_lower:
                return condition
        return 'general condition'

    def _extract_policy_age(self, query):
        """Extract policy age in months"""
        month_match = re.search(r'(\d+)\s*month', query.lower())
        year_match = re.search(r'(\d+)\s*year', query.lower())

        if month_match:
            return int(month_match.group(1))
        elif year_match:
            return int(year_match.group(1)) * 12
        return 12  # Default

    def _make_decision(self, condition, policy_age_months, is_emergency):
        """Make policy decision based on real rules"""

        # Emergency/accident - immediate approval
        if is_emergency or 'accident' in condition.lower():
            return {
                'status': 'approved',
                'reason': 'Emergency coverage applies - no waiting period',
                'explanation': 'Approved! Emergency and accidents are covered immediately.'
            }

        # Cardiac conditions - 90 day waiting
        if 'cardiac' in condition or 'heart' in condition:
            if policy_age_months < 3:  # Less than 90 days
                return {
                    'status': 'rejected',
                    'reason': f'Cardiac conditions need 90-day waiting period. Current: {policy_age_months} months',
                    'explanation': 'Cardiac treatments require 90-day waiting period. Please reapply after this period.'
                }

        # General illness - 30 day waiting
        if policy_age_months < 1:  # Less than 30 days
            return {
                'status': 'rejected',
                'reason': f'30-day waiting period for illnesses. Current: {policy_age_months} months',
                'explanation': 'General medical conditions have 30-day waiting period.'
            }

        # Approve if all checks pass
        return {
            'status': 'approved',
            'reason': f'Coverage approved. Policy age: {policy_age_months} months meets requirements',
            'explanation': 'Your claim is approved based on policy terms and waiting periods.'
        }

    def _get_specialist(self, condition):
        """Get specialist for condition"""
        specialists = {
            'knee': 'Orthopedic Surgeon',
            'cardiac': 'Cardiologist',
            'heart': 'Cardiologist',
            'cancer': 'Oncologist',
            'kidney': 'Nephrologist',
            'emergency': 'Emergency Specialist',
            'fracture': 'Orthopedic Surgeon'
        }

        for key, specialist in specialists.items():
            if key in condition.lower():
                return specialist
        return 'General Physician'

    def _get_error_response(self):
        """Default error response"""
        return {
            "decision": "error",
            "justification": "Unable to find relevant policy information",
            "user_friendly_explanation": "Please contact customer service for assistance",
            "location_detected": "Not specified",
            "nearby_hospitals": ["Contact customer service"],
            "emergency_contacts": ["108 - Emergency", "100 - Police"],
            "immediate_care_tips": ["Contact customer service"],
            "specialist_recommendation": "General Physician"
        }

    def hospitality_assistant(self, question):
        """General hospitality assistant"""
        try:
            response = self.llm.generate_content(f"""
            You are a helpful hospitality assistant in India. Answer this concisely:

            Question: {question}

            Provide practical, accurate information in 2-3 sentences.
            """)

            return response.text.strip()

        except Exception as e:
            return f"Sorry, I couldn't process that request: {str(e)}"
