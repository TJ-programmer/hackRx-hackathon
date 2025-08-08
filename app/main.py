import logging
from fastapi import FastAPI, HTTPException
from app.models import Request, Response
from app.parser import parse_document
from app.chunker import chunk_text
from app.embedder import embed_chunks
from app.vector_store import init_qdrant, store_vectors, search_similar
from app.llm import generate_answer
from typing import List
from dotenv import load_dotenv
from app.logging_config import setup_logger

load_dotenv()

logger = setup_logger(__name__)

app = FastAPI()

try:
    init_qdrant()
    logger.info("Qdrant collection initialized successfully.")
except Exception:
    logger.exception("Failed to initialize Qdrant.")
    raise


@app.post("/process", response_model=Response)
def process_qa(data: Request):
    try:
        logger.info(
            f"Received QA request with URL: {data.document_url} and {len(data.questions)} questions"
        )

        raw_text = parse_document(data.document_url)
        if not raw_text:
            logger.warning("No text extracted from document.")
            raise HTTPException(
                status_code=400, detail="Failed to extract content from document."
            )
        logger.info(f"Document parsed with {len(raw_text)} characters.")

        chunks = chunk_text(raw_text)
        if not chunks:
            logger.warning("Document chunking resulted in no chunks.")
            raise HTTPException(status_code=400, detail="Document chunking failed.")
        logger.info(f"Generated {len(chunks)} text chunks.")

        embeddings = embed_chunks(chunks)
        if not embeddings:
            logger.error("Embedding chunks failed.")
            raise HTTPException(status_code=500, detail="Failed to embed chunks.")
        logger.info(f"Generated {len(embeddings)} embeddings.")

        store_vectors(chunks, embeddings)
        logger.info("Document chunks stored in vector store.")

        answers: List[str] = []
        sources: List[str] = []

        for idx, question in enumerate(data.questions):
            logger.info(f"Processing question {idx+1}: {question}")
            try:
                query_vec = embed_chunks([question])[0]
                top_chunks = search_similar(query_vec)
                if not top_chunks:
                    logger.warning(f"No results retrieved for question: {question}")
                    answers.append("Sorry, I couldn't find relevant information.")
                    sources.append("No matched content.")
                    continue

                context = "\n".join(top_chunks)
                answer = generate_answer(context, question)
                answers.append(answer)
                sources.append("Matched Chunks:\n" + context[:300] + "...")
                logger.info(f"Answered question {idx+1}")
            except Exception:
                logger.exception(f"Failed to process question {idx+1}")
                answers.append("An error occurred while processing the question.")
                sources.append("Error during retrieval or generation.")

        return Response(answers=answers)

    except HTTPException as http_exc:
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise http_exc
    except Exception:
        logger.exception("Unexpected error occurred during QA processing.")
        raise HTTPException(status_code=500, detail="Internal server error.")
