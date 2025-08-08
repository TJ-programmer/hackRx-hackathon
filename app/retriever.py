import logging
from typing import List, Dict
from app.logging_config import setup_logger
from app.vector_store import dimension, COLLECTION_NAME, client

logger = setup_logger(__name__)


def search(query_embedding: List[float], k: int = 5) -> List[Dict[str, str]]:
    if not query_embedding:
        logger.warning("Empty query embedding provided for search.")
        return []

    if len(query_embedding) != dimension:
        logger.error(
            f"Query embedding dimension mismatch. Expected {dimension}, got {len(query_embedding)}. Aborting search."
        )
        return []

    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=k,
            with_payload=True,
            with_vectors=False,
        )

        logger.info(f"Found {len(results)} search results.")
        return [
            {"text": hit.payload.get("text", ""), "score": round(hit.score, 4)}
            for hit in results
            if hit.payload and "text" in hit.payload
        ]

    except Exception:
        logger.exception("Error during Qdrant search")
        return []
