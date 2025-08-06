"""
🚀 REAL DOCUMENT-PROCESSING SERVER
=================================
Actually reads and processes your PDF documents!
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
import json
import logging

# Import the REAL processors that actually read documents
from main import IntelligentClaimsProcessor
from ultra_fast_processor import UltraFastProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Real Document Processing API")

class QueryRequest(BaseModel):
    documents: str
    questions: List[str]

# Global processors - REAL ONES
processor = None
ultra_fast_processor = None
documents_loaded = False

@app.on_event("startup")
async def startup_event():
    """Load actual documents on startup"""
    global processor, ultra_fast_processor, documents_loaded

    try:
        logger.info("🚀 Initializing REAL document processors...")

        # Initialize the REAL processors
        processor = IntelligentClaimsProcessor()
        ultra_fast_processor = UltraFastProcessor()

        # Load ACTUAL documents from docs folder
        docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
        logger.info(f"📂 Loading documents from: {docs_path}")

        if os.path.exists(docs_path):
            if processor.load_documents("docs"):
                documents_loaded = True
                logger.info(f"✅ Successfully loaded {len(processor.document_chunks)} document chunks")
                logger.info(f"📊 Documents processed from: {set(processor.document_sources)}")
            else:
                logger.error("❌ Failed to load documents")
        else:
            logger.error(f"❌ Docs folder not found: {docs_path}")

    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "🏥 REAL Document Processing API",
        "status": "healthy",
        "documents_loaded": documents_loaded,
        "document_count": len(processor.document_chunks) if processor and processor.document_chunks else 0
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "message": "Ready for REAL document processing!",
        "documents_loaded": documents_loaded,
        "document_chunks": len(processor.document_chunks) if processor and processor.document_chunks else 0,
        "document_sources": list(set(processor.document_sources)) if processor and processor.document_sources else []
    }

@app.post("/hackrx/run")
async def hackrx_run(request: QueryRequest):
    """REAL hackathon endpoint that processes actual documents with instant pattern matching"""

    if not processor or not documents_loaded:
        return JSONResponse(
            content={
                "error": "Documents not loaded",
                "message": "Document processing system not ready"
            },
            status_code=500
        )

    answers = []

    for question in request.questions:
        try:
            logger.info(f"🔍 Processing question: {question[:100]}...")

            # FIRST: Try instant pattern matching
            instant_result = ultra_fast_processor.instant_decision(question)
            if instant_result:
                answer = instant_result.get('answer', 'No answer available')
                logger.info(f"⚡ Instant match: {question[:50]}...")
                answers.append({
                    "question": question,
                    "answer": answer
                })
                continue

            # Use REAL document search and processing
            relevant_chunks, relevant_sources = processor.semantic_search(question, top_k=5)

            if relevant_chunks:
                # Try AI processing first
                try:
                    result = processor.process_claim_query(question)
                    answer = result.get('user_friendly_explanation', 'Unable to process this query.')
                    logger.info(f"✅ AI processed: {question[:50]}...")
                except Exception as ai_error:
                    logger.warning(f"⚠️ AI failed, using ultra-fast: {str(ai_error)}")
                    # Fallback to ultra-fast processor
                    ultra_result = ultra_fast_processor.ultra_fast_process(question, relevant_chunks)
                    answer = ultra_result.get('answer', 'Unable to process this query.')
            else:
                # No relevant chunks found
                answer = f"No relevant information found in the policy documents for this query: {question}"
                logger.warning(f"❌ No relevant chunks for: {question[:50]}...")

        except Exception as e:
            logger.error(f"❌ Error processing question: {str(e)}")
            answer = f"Error processing query: {str(e)}"

        answers.append({
            "question": question,
            "answer": answer
        })

    logger.info(f"🎉 Processed {len(answers)} questions")

    response_data = {"answers": answers}
    return JSONResponse(
        content=response_data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )

@app.get("/debug/documents")
async def debug_documents():
    """Debug endpoint to check what documents are loaded"""
    if not processor:
        return {"error": "Processor not initialized"}

    return {
        "documents_loaded": documents_loaded,
        "total_chunks": len(processor.document_chunks) if processor.document_chunks else 0,
        "document_sources": list(set(processor.document_sources)) if processor.document_sources else [],
        "sample_chunks": processor.document_chunks[:3] if processor.document_chunks else [],
        "docs_folder_exists": os.path.exists("docs"),
        "docs_folder_contents": os.listdir("docs") if os.path.exists("docs") else []
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting REAL document processing server on port {port}")
    print("📄 This server ACTUALLY reads your PDF documents!")
    uvicorn.run("real_server:app", host="0.0.0.0", port=port, log_level="info")
