from app.logging_config import setup_logger
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from typing import List
import uuid

logger = setup_logger(__name__)
client = QdrantClient(location=":memory:")
dimension = 384
COLLECTION_NAME = "documents"


def init_qdrant() -> None:
    logger.info(f"QdrantClient initialized (in-memory). Collection: {COLLECTION_NAME}")
    try:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
        )
        logger.info(f"Qdrant collection '{COLLECTION_NAME}' recreated/initialized.")
    except Exception as e:
        logger.exception(f"Error initializing Qdrant collection: {e}")
        raise


def store_vectors(chunks: List[str], embeddings: List[List[float]]) -> None:
    if not embeddings or not chunks:
        logger.warning("No chunks or embeddings provided for storage.")
        return

    valid_points: List[PointStruct] = []
    for text, vec in zip(chunks, embeddings):
        if len(vec) != dimension:
            logger.warning(
                f"Skipping chunk due to embedding size mismatch: expected {dimension}, got {len(vec)}"
            )
            continue
        valid_points.append(
            PointStruct(id=str(uuid.uuid4()), vector=vec, payload={"text": text})
        )

    if not valid_points:
        logger.warning("No valid vectors to upsert into Qdrant.")
        return

    try:
        client.upsert(collection_name=COLLECTION_NAME, points=valid_points, wait=True)
        logger.info(
            f"Successfully upserted {len(valid_points)} vectors into Qdrant collection '{COLLECTION_NAME}'."
        )
    except Exception as e:
        logger.exception(f"Failed to upsert vectors into Qdrant: {e}")


def search_similar(query_vector: List[float], k: int = 5) -> List[str]:
    try:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=k,
            with_payload=True,
        )
        return [r.payload.get("text", "") for r in results if r.payload]
    except Exception as e:
        logger.exception(f"Failed to search similar vectors: {e}")
        return []



