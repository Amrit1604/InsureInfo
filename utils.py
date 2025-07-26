import os
import PyPDF2
from docx import Document
from email import policy
from email.parser import BytesParser
import fitz  # PyMuPDF for better PDF text extraction

def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF for better quality"""
    try:
        # Try PyMuPDF first (better text extraction)
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except:
        # Fallback to PyPDF2
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_eml(file_path):
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)
    return msg.get_body(preferencelist=('plain')).get_content()

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    elif ext == ".eml":
        return extract_text_from_eml(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def process_multiple_documents(docs_folder="docs"):
    """
    Process multiple policy documents from a folder and return combined text chunks
    Only processes sample policy documents, excludes document.txt files
    """
    all_chunks = []
    document_sources = []  # Track which document each chunk came from

    if not os.path.exists(docs_folder):
        raise ValueError(f"Documents folder '{docs_folder}' not found!")

    # Get only policy documents (exclude document.txt files)
    supported_extensions = ['.pdf', '.docx']
    files = []

    for file in os.listdir(docs_folder):
        file_path = os.path.join(docs_folder, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()
            filename = os.path.splitext(file)[0].lower()

            # Only process sample policy files, exclude document.txt
            if (ext in supported_extensions and
                ('policy' in filename or 'sample' in filename) and
                'document' not in filename):
                files.append((file, file_path))

    if not files:
        raise ValueError(f"No sample policy documents found in '{docs_folder}' folder!")

    print(f"Processing {len(files)} policy documents:")

    for filename, file_path in files:
        print(f"  - {filename}")
        try:
            # Extract text from each document
            text = extract_text_from_file(file_path)

            # Chunk the text with improved chunking for policy documents
            chunks = chunk_text_for_policy(text)

            # Add source information to each chunk
            for chunk in chunks:
                all_chunks.append(chunk)
                document_sources.append(filename)

            print(f"    → {len(chunks)} chunks extracted")

        except Exception as e:
            print(f"    → Error processing {filename}: {e}")
            continue

    print(f"\nTotal chunks across all policy documents: {len(all_chunks)}")
    return all_chunks, document_sources

def chunk_text_for_policy(text, max_length=600):
    """
    Improved text chunking specifically for policy documents
    Tries to preserve clause boundaries and policy structure
    """
    # Clean up text first
    text = text.replace('\n\n', '\n').replace('  ', ' ').strip()

    # Policy-specific clause indicators
    clause_indicators = [
        '\n\n',  # Paragraph breaks
        'Clause ',
        'Section ',
        'Article ',
        'Coverage ',
        'Benefit ',
        'Exclusion ',
        'Definition ',
        'Policy ',
        'Terms ',
        'Conditions ',
        'Eligibility ',
        'Waiting Period',
        'Sum Insured'
    ]

    # First try to split by major clause indicators
    chunks = []
    current_chunk = ""

    sentences = text.split('. ')

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Check if this sentence starts a new major clause
        is_new_clause = any(indicator.lower() in sentence.lower()[:50]
                           for indicator in clause_indicators)

        # If adding this sentence would exceed max_length or it's a new major clause
        if ((len(current_chunk) + len(sentence) > max_length and current_chunk) or
            (is_new_clause and current_chunk and len(current_chunk) > 100)):

            if current_chunk.strip():
                chunks.append(current_chunk.strip() + '.')
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += '. ' + sentence
            else:
                current_chunk = sentence

    # Add the last chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out very short chunks (likely noise) and very long chunks
    filtered_chunks = []
    for chunk in chunks:
        words = chunk.split()
        if 15 <= len(words) <= 120:  # Keep chunks between 15-120 words
            filtered_chunks.append(chunk)

    # If no good chunks found, fall back to simple chunking
    if not filtered_chunks:
        return chunk_text(text, max_length)

    return filtered_chunks

def chunk_text(text, max_length=500):
    """
    Improved text chunking that tries to preserve clause boundaries
    """
    # First try to split by common clause indicators
    clause_indicators = [
        '\n\n',  # Paragraph breaks
        'Clause ',
        'Section ',
        'Article ',
        'Coverage ',
        'Benefit ',
        'Exclusion ',
        'Definition '
    ]

    # Split text into sentences first
    sentences = text.replace('\n', ' ').split('. ')

    chunks = []
    current_chunk = []
    current_length = 0

    for sentence in sentences:
        words = sentence.split()
        sentence_length = len(words)

        # If adding this sentence would exceed max_length, save current chunk
        if current_length + sentence_length > max_length and current_chunk:
            chunks.append(' '.join(current_chunk) + '.')
            current_chunk = []
            current_length = 0

        current_chunk.extend(words)
        current_length += sentence_length

    # Add the last chunk if it exists
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    # Filter out very short chunks (likely noise)
    chunks = [chunk for chunk in chunks if len(chunk.split()) > 10]

    return chunks