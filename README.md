# 🏥 LLM Claims Processing System

An intelligent insurance claims processing system that uses Large Language Models (LLMs) and semantic search to automatically evaluate claims based on policy documents.

## 🎯 Features

- **Natural Language Query Processing**: Submit claims in plain English
- **Semantic Document Search**: Uses sentence transformers and FAISS for intelligent clause retrieval
- **LLM-Powered Decision Making**: Gemini 1.5 Flash evaluates claims based on retrieved policy clauses
- **Structured JSON Responses**: Consistent output format for downstream applications
- **Multiple Document Formats**: Supports PDF, DOCX, and EML files
- **Web Interface**: Streamlit-based UI for easy interaction

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
```bash
git clone <your-repo>
cd llm_claims_system_gemini
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. **Add your policy documents**
Place your policy documents in the `docs/` folder (PDF, DOCX, or EML format)

### Usage

#### Command Line
```bash
python main.py
```

#### Web Interface
```bash
streamlit run app.py
```

#### Testing Multiple Scenarios
```bash
python test_system.py
```

## 📝 Example Queries

- `"46-year-old male, knee surgery in Pune, 3-month-old insurance policy"`
- `"25-year-old female, dental treatment, Mumbai, 6-month policy"`
- `"60-year-old male, heart surgery, emergency, Delhi, 2-year policy"`

## 📊 Sample Response

```json
{
  "decision": "approved",
  "amount": 50000,
  "justification": "Based on Clause 3, inpatient hospitalization for surgical treatment is covered. The knee surgery qualifies as medically necessary treatment. However, since the policy is only 3 months old, please verify if the waiting period requirements are met according to Clause 7."
}
```

## 🏗️ System Architecture

```
Input Query → Semantic Search → LLM Processing → Structured Output
     ↓              ↓              ↓              ↓
Natural Language → Relevant     → Decision    → JSON Response
                   Clauses       Making
```

### Components

1. **Document Processing** (`utils.py`)
   - Text extraction from multiple formats
   - Intelligent text chunking

2. **Semantic Search** (`main.py`)
   - Sentence transformer embeddings
   - FAISS vector similarity search

3. **LLM Decision Engine** (`main.py`)
   - Gemini 1.5 Flash integration
   - Structured prompt engineering
   - JSON response parsing

## 🔧 Configuration

### Model Settings
- **Embedding Model**: `all-MiniLM-L6-v2`
- **LLM Model**: `gemini-1.5-flash`
- **Chunk Size**: 500 words
- **Top-K Retrieval**: 3 clauses

### API Limits
- Using Gemini 1.5 Flash for better rate limits
- Automatic error handling for quota exceeded

## 📁 Project Structure

```
llm_claims_system_gemini/
├── main.py              # Core system logic
├── utils.py             # Document processing utilities
├── app.py               # Streamlit web interface
├── test_system.py       # Multi-query testing
├── requirements.txt     # Dependencies
├── .env                 # Environment variables
└── docs/               # Policy documents
    └── sample_policy_merged.pdf
```

## 🎛️ Advanced Usage

### Custom Document Processing
```python
from main import extract_text_from_file, chunk_text, get_embeddings

# Process your own document
text = extract_text_from_file("path/to/sample_policy_merged.pdf")
chunks = chunk_text(text, max_length=600)  # Custom chunk size
embeddings = get_embeddings(chunks)
```

### Batch Processing
```python
# Process multiple queries
queries = [
    "query1...",
    "query2...",
    "query3..."
]

for query in queries:
    relevant = semantic_search(query, chunks, embeddings)
    result = ask_llm(query, relevant)
    print(f"Query: {query}")
    print(f"Result: {result}")
```

## 🔍 Applications

- **Insurance Claims Processing**
- **Legal Document Analysis**
- **Contract Compliance Checking**
- **HR Policy Queries**
- **Regulatory Compliance**

## 🛠️ Troubleshooting

### Common Issues

1. **API Quota Exceeded**
   - Wait for quota reset
   - Switch to paid plan
   - Use different API key

2. **Missing Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Document Loading Errors**
   - Check file path
   - Verify file format (PDF, DOCX, EML)
   - Ensure file is not corrupted

## 📈 Performance Metrics

- **Document Processing**: ~1-2 seconds for typical policy documents
- **Embedding Generation**: ~3-5 seconds for 60 chunks
- **Query Processing**: ~2-3 seconds per query
- **Accuracy**: Depends on policy document quality and query specificity

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini API for LLM capabilities
- Hugging Face for sentence transformers
- Facebook AI for FAISS vector search
- Streamlit for the web interface
