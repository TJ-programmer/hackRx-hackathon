
from app.logging_config import setup_logger
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List

logger = setup_logger(__name__)

# Initialize TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    max_features=384,  # Match the original dimension
    stop_words='english',
    ngram_range=(1, 2),
    min_df=1,
    max_df=0.9
)

def embed_chunks(texts: List[str]) -> List[List[float]]:
    if not texts:
        logger.warning("No texts provided for embedding.")
        return []
    try:
        # Fit and transform the texts
        tfidf_matrix = vectorizer.fit_transform(texts)
        
        # Convert to dense array and normalize
        embeddings = tfidf_matrix.toarray()
        
        # Normalize to unit vectors for cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1, norms)  # Avoid division by zero
        embeddings = embeddings / norms
        
        # Pad or truncate to 384 dimensions
        target_dim = 384
        if embeddings.shape[1] < target_dim:
            # Pad with zeros
            padding = np.zeros((embeddings.shape[0], target_dim - embeddings.shape[1]))
            embeddings = np.hstack([embeddings, padding])
        elif embeddings.shape[1] > target_dim:
            # Truncate
            embeddings = embeddings[:, :target_dim]
        
        logger.info(f"Generated {len(embeddings)} TF-IDF embeddings.")
        return embeddings.tolist()
    except Exception as e:
        logger.exception(f"Error generating embeddings: {e}")
        return []
    

