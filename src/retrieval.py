import faiss
import numpy as np


def create_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(
        embeddings.astype(np.float32)
    )

    return index


def retrieve(
    query,
    embedding_model,
    index,
    top_k=5
):

    query_embedding = embedding_model.encode(
        query,
        normalize_embeddings=True
    )

    scores, indices = index.search(
        np.array([query_embedding], dtype=np.float32),
        top_k
    )

    return indices[0], scores[0]