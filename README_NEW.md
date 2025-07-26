# 🏥 Intelligent Insurance Claims Processing System

> **Built with Large Language Models (LLMs) to process natural language queries and retrieve relevant information from insurance policy documents.**

## 🎯 Overview

This system takes natural language queries like *"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"* and automatically:

1. **Parses** the query to identify key details (age, procedure, location, policy duration)
2. **Searches** policy documents using advanced semantic understanding
3. **Evaluates** coverage eligibility based on policy clauses
4. **Returns** structured decisions with clear justifications

## ✨ Key Features

- 🧠 **Smart Natural Language Processing**: Understands casual language and medical terms
- 🔍 **Semantic Document Search**: Goes beyond keyword matching to find relevant policy clauses
- ⚡ **Emergency Detection**: Automatically fast-tracks emergency claims
- 📋 **Structured Decisions**: Returns JSON responses with decision, amount, and justification
- 🔗 **Clause Mapping**: References specific policy clauses used in decisions
- 👥 **User-Friendly**: Explains decisions in plain English

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file with your Google API key:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 3. Add Policy Documents

Place your policy documents in the `docs/` folder:
- ✅ `sample_policy_merged.pdf` (included)
- ✅ Any other policy PDFs or Word documents
- ❌ Exclude `document.txt` files (system will ignore them)

### 4. Test the System

```bash
# Run system health check
python test_system_health.py

# Run comprehensive demo
python demo.py

# Run interactive mode
python main.py
```

## 📊 Sample Usage

### Input Query Examples:
```python
# Formal medical query
"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"

# Casual language
"my kid broke his arm playing soccer we have insurance for 2 years"

# Emergency situation
"emergency heart attack, 55 year old man, 6 month policy"

# Abbreviated format
"25F, appendix surgery, Mumbai, 1 year policy"
```

### Sample Response:
```json
{
  "decision": "approved",
  "amount": 75000,
  "justification": "Knee surgery is covered under orthopedic benefits. Policy duration of 3 months meets emergency coverage requirements.",
  "emergency_override": false,
  "user_friendly_explanation": "Your knee surgery is covered! The policy covers orthopedic procedures, and your 3-month policy meets the minimum requirements.",
  "clause_references": ["Section 4.2 - Orthopedic Coverage", "Clause 1.3 - Emergency Provisions"]
}
```

## 🏗️ System Architecture

```
📁 Project Structure
├── main.py                 # Core claims processor
├── demo.py                 # Comprehensive demo
├── smart_processor.py      # Natural language understanding
├── utils.py               # Document processing utilities
├── test_system_health.py  # System testing
├── requirements.txt       # Python dependencies
└── docs/
    └── sample_policy_merged.pdf  # Policy documents
```

### Key Components:

1. **IntelligentClaimsProcessor** - Main orchestrator
2. **SmartQueryProcessor** - Converts casual language to medical terms
3. **Semantic Search** - FAISS-powered document search
4. **AI Decision Engine** - Gemini-powered claim evaluation

## 🔧 Technical Details

### Dependencies:
- **Google Gemini AI** - For natural language processing and decision making
- **Sentence Transformers** - For semantic embeddings
- **FAISS** - For fast similarity search
- **PyMuPDF** - For high-quality PDF text extraction
- **Colorama** - For enhanced console output

### Processing Pipeline:
1. **Query Understanding**: Converts natural language to structured medical information
2. **Document Loading**: Extracts and chunks policy documents
3. **Semantic Search**: Finds relevant policy clauses using embeddings
4. **AI Evaluation**: Uses LLM to make coverage decisions
5. **Response Generation**: Returns structured JSON with explanations

## 🎮 Usage Examples

### Command Line Interface:
```bash
# Run the main system
python main.py

# Output:
# 🏥 INTELLIGENT INSURANCE CLAIMS PROCESSING SYSTEM
# Enter your claim: my 8 year old broke his leg at school
#
# 🧠 AI Understanding: 8-year-old child with leg fracture injury at school
# 🔍 Searching for relevant policy clauses...
# ✅ CLAIM APPROVED
# 💰 Estimated Amount: ₹45,000
# 📋 Explanation: Pediatric fractures are covered under your policy...
```

### Programmatic Usage:
```python
from main import IntelligentClaimsProcessor

# Initialize
processor = IntelligentClaimsProcessor()
processor.load_documents("docs")

# Process claim
decision = processor.process_claim_query(
    "25 year old female appendix surgery emergency Mumbai 6 month policy"
)

print(f"Decision: {decision['decision']}")
print(f"Amount: {decision['amount']}")
```

## 🧪 Testing

The system includes comprehensive testing:

```bash
# Health check
python test_system_health.py

# Demo with multiple test cases
python demo.py
```

**Test Scenarios:**
- Middle-aged orthopedic surgery
- Pediatric sports injuries
- Emergency cardiac events
- Routine preventive care
- Pre-existing condition detection
- Casual vs formal language processing

## 🌟 Advanced Features

### Emergency Detection:
- Automatically identifies urgent medical situations
- Applies fast-track processing rules
- Prioritizes immediate care coverage

### Smart Language Processing:
- Converts "broke my arm" → "arm fracture"
- Understands "tummy" → "abdomen"
- Processes "46M" → "46-year-old male"

### Policy Intelligence:
- Distinguishes coverage clauses from procedural requirements
- Applies age and policy duration rules
- References specific policy sections in decisions

## 📈 Performance

- **Processing Time**: ~2-3 seconds per query
- **Accuracy**: High semantic understanding of medical terms
- **Coverage**: Handles policy documents up to 100+ pages
- **Scalability**: Processes multiple policy documents simultaneously

## 🤝 Applications

This system can be adapted for:
- **Insurance**: Health, auto, property claims processing
- **Legal**: Contract analysis and compliance checking
- **HR**: Policy interpretation and employee queries
- **Healthcare**: Treatment authorization and coverage verification

## 🛠️ Customization

### Adding New Policy Documents:
1. Place PDF/Word files in `docs/` folder
2. Ensure filenames contain "policy" or "sample"
3. System automatically processes and indexes them

### Modifying Decision Logic:
- Edit prompts in `main.py` → `_evaluate_claim_with_ai()`
- Adjust coverage rules and approval criteria
- Customize emergency detection rules

### Language Processing:
- Update `smart_processor.py` for new medical terms
- Add industry-specific vocabulary
- Modify chunking strategy in `utils.py`

## 📝 License

This project is for educational and demonstration purposes. Ensure compliance with your organization's data and AI usage policies.

## 🆘 Support

If you encounter issues:
1. Run `python test_system_health.py` to diagnose problems
2. Check that your `.env` file contains a valid Google API key
3. Ensure policy documents are in the `docs/` folder
4. Verify all dependencies are installed correctly

---

**Built with ❤️ using Google Gemini AI, designed to make insurance claims processing more intelligent and user-friendly.**
