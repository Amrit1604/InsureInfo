"""
🏥 INTELLIGENT INSURANCE CLAIMS PROCESSING SYSTEM
==================================================
Built with LLMs to process natural language queries and retrieve relevant
information from large unstructured policy documents.

✨ Features:
- Parse natural language queries (e.g., "46M, knee surgery, Pune, 3-month policy")
- Smart semantic search through policy documents
- AI-powered decision making with clear justifications
- Reference specific clauses used in decisions
- User-friendly explanations in plain English
"""

import os
import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from utils import extract_text_from_file, chunk_text, process_multiple_documents
from smart_processor import SmartQueryProcessor
import google.generativeai as genai
import json
from colorama import init, Fore, Back, Style

# Initialize colorama for better console output
init(autoreset=True)

class IntelligentClaimsProcessor:
    def __init__(self):
        """Initialize the claims processing system"""
        # Load environment variables
        load_dotenv()

        # Check if API key is available
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            print(f"{Fore.RED}❌ Error: GOOGLE_API_KEY not found in environment variables.")
            print("Please create a .env file with your Google API key.")
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

        print(f"{Fore.GREEN}✅ Intelligent Claims Processor initialized successfully!")

    def load_documents(self, docs_folder="docs"):
        """Load and process all policy documents from the docs folder"""
        print(f"\n{Fore.CYAN}📚 Loading policy documents...")

        try:
            # Process only sample policy documents (exclude document.txt files)
            all_chunks, document_sources = self._process_policy_documents(docs_folder)

            if not all_chunks:
                print(f"{Fore.RED}❌ No policy documents found in '{docs_folder}' folder!")
                return False

            self.document_chunks = all_chunks
            self.document_sources = document_sources

            # Generate embeddings
            print(f"{Fore.YELLOW}🧠 Generating semantic embeddings...")
            self.embeddings = self.sentence_model.encode(self.document_chunks)

            print(f"{Fore.GREEN}✅ Successfully loaded {len(self.document_chunks)} document chunks")
            print(f"📊 Embeddings shape: {self.embeddings.shape}")

            # Show document statistics
            unique_docs = list(set(self.document_sources))
            print(f"{Fore.BLUE}📋 Documents processed:")
            for doc in unique_docs:
                count = self.document_sources.count(doc)
                print(f"   • {doc}: {count} chunks")

            return True

        except Exception as e:
            print(f"{Fore.RED}❌ Error loading documents: {str(e)}")
            return False

    def _process_policy_documents(self, docs_folder):
        """Process only sample policy documents, exclude document.txt files"""
        all_chunks = []
        document_sources = []

        if not os.path.exists(docs_folder):
            raise ValueError(f"Documents folder '{docs_folder}' not found!")

        # Get all files, but exclude document.txt files
        supported_extensions = ['.pdf', '.docx']  # Only policy documents
        files = []

        for file in os.listdir(docs_folder):
            file_path = os.path.join(docs_folder, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                filename = os.path.splitext(file)[0].lower()

                # Only process sample policy files
                if (ext in supported_extensions and
                    ('policy' in filename or 'sample' in filename) and
                    'document' not in filename):
                    files.append((file, file_path))

        if not files:
            raise ValueError(f"No sample policy documents found in '{docs_folder}' folder!")

        for filename, file_path in files:
            try:
                print(f"   📄 Processing: {filename}")
                text = extract_text_from_file(file_path)
                chunks = chunk_text(text)

                for chunk in chunks:
                    all_chunks.append(chunk)
                    document_sources.append(filename)

                print(f"      → {len(chunks)} chunks extracted")

            except Exception as e:
                print(f"      → ❌ Error processing {filename}: {e}")
                continue

        return all_chunks, document_sources


    def semantic_search(self, query, top_k=5):
        """
        Enhanced semantic search that filters for relevant coverage clauses
        and focuses on policy-specific content
        """
        if not self.embeddings.size:
            print(f"{Fore.RED}❌ No documents loaded! Please load documents first.")
            return []

        print(f"{Fore.YELLOW}🔍 Searching for relevant policy clauses...")

        query_emb = self.sentence_model.encode([query])

        # Ensure embeddings are numpy arrays with correct dtype
        embeddings = self.embeddings.astype('float32')
        query_emb = query_emb.astype('float32')

        # Create FAISS index for semantic search
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        # Search for more candidates initially to filter better
        search_k = min(top_k * 3, len(self.document_chunks))
        distances, indices = index.search(query_emb, search_k)

        # Enhanced filtering and ranking
        candidates = []
        for idx, i in enumerate(indices[0]):
            if i < len(self.document_chunks):
                chunk = self.document_chunks[i]
                score = float(distances[0][idx])

                # Calculate relevance based on coverage keywords
                relevance_score = self._calculate_chunk_relevance(chunk, query)

                # Combine semantic similarity with relevance
                combined_score = score * (1 / max(relevance_score, 0.1))

                candidates.append({
                    'chunk': chunk,
                    'score': combined_score,
                    'source': self.document_sources[i],
                    'relevance': relevance_score
                })

        # Sort by combined score and return top k
        candidates.sort(key=lambda x: x['score'])
        top_candidates = candidates[:top_k]

        print(f"{Fore.GREEN}✅ Found {len(top_candidates)} relevant clauses")

        return [candidate['chunk'] for candidate in top_candidates], \
               [candidate['source'] for candidate in top_candidates]

    def _calculate_chunk_relevance(self, chunk, query):
        """Calculate how relevant a chunk is for the query"""
        chunk_lower = chunk.lower()
        query_lower = query.lower()

        # Policy-specific keywords that indicate important clauses
        coverage_keywords = [
            'coverage', 'covered', 'benefit', 'treatment', 'surgery',
            'medical', 'hospital', 'injury', 'accident', 'emergency',
            'inpatient', 'outpatient', 'rehabilitation', 'therapy',
            'policy', 'claim', 'eligible', 'exclusion', 'inclusion',
            'deductible', 'copay', 'premium', 'waiting period'
        ]

        # Keywords that suggest procedural/administrative content (less relevant)
        procedural_keywords = [
            'helpline', 'notify', 'inform', 'contact', 'call', 'phone',
            'documentation', 'submit', 'forms', 'application',
            'within 48 hours', 'deadline', 'timeframe', 'office hours'
        ]

        # Calculate scores
        coverage_score = sum(2 if keyword in chunk_lower else 0 for keyword in coverage_keywords)
        procedural_penalty = sum(1 if keyword in chunk_lower else 0 for keyword in procedural_keywords)

        # Query-specific relevance
        query_words = query_lower.split()
        query_match_score = sum(3 if word in chunk_lower else 0 for word in query_words if len(word) > 2)

        # Final relevance score
        relevance = max(coverage_score + query_match_score - procedural_penalty, 0.1)
        return relevance


    def process_claim_query(self, query):
        """
        Main method to process a user's claim query and return a decision
        """
        print(f"\n{Fore.CYAN}🔄 Processing claim query: {Style.BRIGHT}{query}")

        # Step 1: Smart processing to understand the query
        print(f"{Fore.YELLOW}🧠 AI is analyzing your request...")
        processed_query_info = self.smart_processor.process_query(query)
        enhanced_query = processed_query_info['processed']
        is_emergency = processed_query_info['is_emergency']

        print(f"{Fore.GREEN}✨ AI Understanding: {enhanced_query}")
        if is_emergency:
            print(f"{Fore.RED}🚨 EMERGENCY DETECTED - Fast-track processing!")
        if processed_query_info['analysis']:
            print(f"{Fore.BLUE}📋 Details: {', '.join(processed_query_info['analysis'])}")

        # Step 2: Search for relevant policy clauses
        relevant_chunks, relevant_sources = self.semantic_search(enhanced_query)

        if not relevant_chunks:
            return {
                "decision": "error",
                "justification": "No relevant policy clauses found for this query.",
                "user_friendly_explanation": "Sorry, I couldn't find relevant information in the policy documents to process your claim.",
                "location_detected": "Not specified",
                "nearby_hospitals": ["Please contact customer service for assistance"],
                "emergency_contacts": ["National Emergency: 108", "Police: 100", "Fire: 101"],
                "immediate_care_tips": ["Contact customer service for guidance", "Visit nearest hospital if urgent"],
                "specialist_recommendation": "General physician"
            }

        # Step 3: Use AI to make the decision
        print(f"{Fore.YELLOW}🤖 AI is evaluating your claim against policy rules...")
        decision = self._evaluate_claim_with_ai(query, enhanced_query, is_emergency, relevant_chunks, relevant_sources)

        return decision

    def _evaluate_claim_with_ai(self, original_query, enhanced_query, is_emergency, relevant_chunks, document_sources):
        """Use AI to evaluate the claim and make a decision based on actual policy content"""

        # Create context from relevant clauses
        clauses_context = "\n".join([
            f"Clause {i+1} (from {document_sources[i]}): {clause}"
            for i, clause in enumerate(relevant_chunks)
        ])

        # Emergency context
        emergency_context = "⚠️ EMERGENCY CLAIM - Prioritize immediate coverage and emergency provisions." if is_emergency else ""

        # Enhanced prompt based on actual Bajaj Allianz Global Health Care policy
        prompt = f"""
You are an expert insurance claims evaluator for Bajaj Allianz Global Health Care Policy (UIN: BAJHLIP23020V012223).
Analyze this claim based on the ACTUAL policy content provided.

{emergency_context}

CLAIM DETAILS:
- Original User Input: "{original_query}"
- Processed Claim: "{enhanced_query}"
- Emergency Status: {"YES - Fast-track processing" if is_emergency else "NO - Standard processing"}

ACTUAL POLICY CLAUSES:
{clauses_context}

BAJAJ ALLIANZ POLICY GUIDELINES (Based on actual policy):
1. **Waiting Periods**:
   - 30 days for general illnesses
   - 90 days for specific conditions (cardiac, cancer, etc.)
   - No waiting period for accidents and emergencies

2. **Coverage Includes**:
   - Inpatient hospitalization treatment
   - Day care procedures (listed surgeries)
   - Emergency ambulance services
   - AYUSH treatments
   - Organ transplant coverage
   - Cancer treatment
   - Cardiac procedures
   - Orthopedic surgeries

3. **Location-Based Hospital Network**:
   - Network hospitals for cashless facility
   - Emergency treatment at any hospital initially
   - Reimbursement available for non-network hospitals

4. **Age Considerations**:
   - Pediatric coverage included
   - Senior citizen coverage with specific conditions
   - Maternity benefits (if covered under specific plans)

5. **Emergency Override**: Always prioritize life-threatening conditions regardless of waiting periods

RESPONSE FORMAT (JSON only):
{{
  "decision": "approved" or "rejected",
  "justification": "Clear explanation referencing specific Bajaj Allianz policy clauses",
  "emergency_override": true_or_false,
  "user_friendly_explanation": "Simple explanation in everyday language",
  "clause_references": ["Specific Bajaj Allianz policy clauses that influenced the decision"],
  "location_detected": "City/area from query or 'Not specified'",
  "nearby_hospitals": ["List of 3-5 hospitals in the detected area - prioritize network hospitals"],
  "emergency_contacts": ["Area-specific emergency numbers including Bajaj Allianz helpline"],
  "immediate_care_tips": ["3-5 medical care tips specific to the condition"],
  "specialist_recommendation": "Type of specialist needed",
  "policy_specific_info": "Additional Bajaj Allianz policy-specific guidance"
}}
"""

        try:
            response = self.llm.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response (remove markdown if present)
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]

            # Parse JSON response
            decision = json.loads(response_text)

            # Add metadata
            decision['processed_query'] = enhanced_query
            decision['emergency_detected'] = is_emergency
            decision['clauses_analyzed'] = len(relevant_chunks)
            decision['policy_name'] = "Bajaj Allianz Global Health Care"
            decision['policy_uin'] = "BAJHLIP23020V012223"

            return decision

        except (json.JSONDecodeError, Exception) as e:
            # Fallback with basic policy information
            return {
                "decision": "error",
                "justification": f"AI processing error: {str(e)}. Please contact Bajaj Allianz customer service.",
                "user_friendly_explanation": "Sorry, there was an error processing your claim. Please contact Bajaj Allianz support for assistance.",
                "emergency_override": False,
                "location_detected": "Not specified",
                "nearby_hospitals": ["Contact Bajaj Allianz for network hospital list"],
                "emergency_contacts": ["Bajaj Allianz: 1800 209 5858", "National Emergency: 108"],
                "immediate_care_tips": ["Seek immediate medical attention if emergency", "Contact Bajaj Allianz for guidance"],
                "specialist_recommendation": "General physician",
                "policy_specific_info": "Bajaj Allianz Global Health Care policy holder"
            }

    def display_decision(self, decision):
        """Display the decision in a user-friendly format with healthcare assistance"""
        print(f"\n{Back.BLUE}{Fore.WHITE}{'=' * 60}")
        print(f"  🏥 BAJAJ ALLIANZ GLOBAL HEALTH CARE - CLAIM ANALYSIS")
        print(f"{'=' * 60}{Style.RESET_ALL}")

        # Policy information
        if decision.get('policy_name'):
            print(f"{Fore.CYAN}📋 Policy: {decision['policy_name']}")
        if decision.get('policy_uin'):
            print(f"{Fore.CYAN}🔢 UIN: {decision['policy_uin']}")

        # Decision status
        if decision['decision'] == 'approved':
            print(f"{Fore.GREEN}✅ CLAIM APPROVED")
        elif decision['decision'] == 'rejected':
            print(f"{Fore.RED}❌ CLAIM REJECTED")
        else:
            print(f"{Fore.YELLOW}⚠️  PROCESSING ERROR")

        # Location detected
        if decision.get('location_detected') and decision['location_detected'] != 'Not specified':
            print(f"{Fore.CYAN}📍 Location: {decision['location_detected']}")

        # User-friendly explanation
        print(f"\n{Fore.YELLOW}📋 Coverage Explanation:")
        print(f"   {decision.get('user_friendly_explanation', 'No explanation available')}")

        # Policy-specific information
        if decision.get('policy_specific_info'):
            print(f"\n{Fore.BLUE}🏛️ Bajaj Allianz Policy Info:")
            print(f"   {decision['policy_specific_info']}")

        # Emergency status
        if decision.get('emergency_override'):
            print(f"\n{Fore.RED}🚨 Emergency Override Applied - Fast-track processing")

        # Healthcare Assistance Section
        print(f"\n{Back.GREEN}{Fore.WHITE} 🏥 HEALTHCARE ASSISTANCE {Style.RESET_ALL}")

        # Nearby hospitals
        if decision.get('nearby_hospitals'):
            print(f"\n{Fore.CYAN}🏥 Recommended Hospitals/Centers:")
            for i, hospital in enumerate(decision['nearby_hospitals'], 1):
                print(f"   {i}. {hospital}")

        # Emergency contacts
        if decision.get('emergency_contacts'):
            print(f"\n{Fore.RED}📞 Emergency Contacts:")
            for contact in decision['emergency_contacts']:
                print(f"   • {contact}")

        # Immediate care tips
        if decision.get('immediate_care_tips'):
            print(f"\n{Fore.YELLOW}💡 Immediate Care Tips:")
            for i, tip in enumerate(decision['immediate_care_tips'], 1):
                print(f"   {i}. {tip}")

        # Specialist recommendation
        if decision.get('specialist_recommendation'):
            print(f"\n{Fore.MAGENTA}👨‍⚕️ Specialist Needed: {decision['specialist_recommendation']}")

        # Technical justification
        if decision.get('justification'):
            print(f"\n{Fore.BLUE}🔍 Technical Analysis:")
            print(f"   {decision['justification']}")

        # Metadata
        if decision.get('clauses_analyzed'):
            print(f"\n{Fore.MAGENTA}📊 Analysis Details:")
            print(f"   • Clauses analyzed: {decision['clauses_analyzed']}")
            if decision.get('processed_query'):
                print(f"   • AI processed query: {decision['processed_query']}")

        print(f"\n{Fore.WHITE}{'=' * 60}")



    def general_hospitality_assistant(self, user_query):
        """Handle general hospitality queries using Gemini API"""

        # Check if query is insurance-related
        insurance_keywords = [
            'claim', 'policy', 'coverage', 'insurance', 'medical', 'hospital',
            'treatment', 'surgery', 'doctor', 'emergency', 'health', 'bajaj', 'allianz'
        ]

        is_insurance_related = any(keyword in user_query.lower() for keyword in insurance_keywords)

        if is_insurance_related:
            # Process as insurance claim
            return self.process_claim_query(user_query)

        # Handle general hospitality queries
        print(f"\n{Fore.CYAN}💬 General Hospitality Assistant")
        print(f"{Fore.YELLOW}🤖 Processing your query with AI assistance...")

        hospitality_prompt = f"""
You are a helpful hospitality and general assistance AI. The user has asked: "{user_query}"

Provide helpful, accurate, and friendly assistance. If the query is about:
- Travel: Provide travel tips, destinations, booking advice
- Hotels: Suggest accommodations, amenities, booking platforms
- Restaurants: Recommend dining options, cuisines, reservation tips
- Local attractions: Suggest places to visit, activities, cultural sites
- Transportation: Help with travel options, routes, booking methods
- General help: Provide useful information and guidance

Be conversational, helpful, and provide practical advice. If you don't know something specific, suggest reliable resources where they can find more information.

Keep your response concise but informative (2-3 paragraphs maximum).
"""

        try:
            response = self.llm.generate_content(hospitality_prompt)

            print(f"\n{Fore.GREEN}✨ AI Assistant Response:")
            print(f"{Fore.WHITE}{response.text}")

            return {
                "type": "general_assistance",
                "query": user_query,
                "response": response.text,
                "status": "success"
            }

        except Exception as e:
            error_response = f"I'm sorry, I encountered an error while processing your request: {str(e)}. Please try rephrasing your question or contact customer support for assistance."

            print(f"\n{Fore.RED}❌ Error: {error_response}")

            return {
                "type": "general_assistance",
                "query": user_query,
                "response": error_response,
                "status": "error"
            }


# ...existing code...
def main():
    """Main function to run the intelligent claims processor"""
    print(f"{Back.GREEN}{Fore.WHITE}{Style.BRIGHT}")
    print("🏥 INTELLIGENT INSURANCE CLAIMS PROCESSING SYSTEM")
    print("=================================================")
    print("Built with LLMs for natural language claim processing")
    print(f"{Style.RESET_ALL}")

    # Initialize the processor
    processor = IntelligentClaimsProcessor()

    # Load documents
    if not processor.load_documents("docs"):
        print(f"{Fore.RED}❌ Failed to load documents. Exiting...")
        return

    print(f"\n{Fore.GREEN}🚀 System ready!")

    # Sample queries for demonstration
    sample_queries = [
        "46-year-old male, knee surgery in Pune, 3-month-old insurance policy",
        "my kid broke his arm playing soccer we have insurance for 2 years",
        "25F, appendix surgery, Mumbai, 1 year policy",
        "emergency heart attack, 55 year old man, 6 month policy",
        "dental cleaning, 30 years old, 2 year policy"
    ]

    print(f"\n{Fore.CYAN}📝 Sample queries you can try:")
    for i, query in enumerate(sample_queries, 1):
        print(f"   {i}. {query}")

    # Process a sample query
    print(f"\n{Fore.YELLOW}🔄 Processing sample query...")
    sample_query = sample_queries[0]  # Process the first sample

    decision = processor.process_claim_query(sample_query)
    processor.display_decision(decision)

    # Interactive mode
    print(f"\n{Fore.GREEN}💬 Interactive Mode - Ask about claims or get general assistance:")
    print(f"{Fore.WHITE}(Type 'quit' to exit)")

    while True:
        try:
            user_input = input(f"\n{Fore.CYAN}Enter your query: {Fore.WHITE}")

            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.GREEN}👋 Thank you for using the Intelligent Claims Processor!")
                break

            if user_input.strip():
                # Check if it's an insurance claim or general hospitality query
                insurance_keywords = [
                    'claim', 'policy', 'coverage', 'insurance', 'medical', 'hospital',
                    'treatment', 'surgery', 'doctor', 'emergency', 'health', 'bajaj', 'allianz'
                ]

                is_insurance_related = any(keyword in user_input.lower() for keyword in insurance_keywords)

                if is_insurance_related:
                    decision = processor.process_claim_query(user_input)
                    processor.display_decision(decision)
                else:
                    result = processor.general_hospitality_assistant(user_input)
            else:
                print(f"{Fore.YELLOW}Please enter a valid query.")

        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}👋 Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}")


if __name__ == "__main__":
    main()