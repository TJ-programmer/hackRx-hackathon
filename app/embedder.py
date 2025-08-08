
from app.logging_config import setup_logger
from sentence_transformers import SentenceTransformer
from typing import List

logger = setup_logger(__name__)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_chunks(texts: List[str]) -> List[List[float]]:
    if not texts:
        logger.warning("No texts provided for embedding.")
        return []
    try:
        embeddings = model.encode(texts).tolist()
        logger.info(f"Generated {len(embeddings)} embeddings.")
        return embeddings
    except Exception as e:
        logger.exception(f"Error generating embeddings: {e}")
        return []
    

