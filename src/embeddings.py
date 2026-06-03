from sentence_transformers import SentenceTransformer


def load_embedding_model():

    model = SentenceTransformer(
        "BAAI/bge-m3"
    )

    return model


def create_chunk_texts(sections):

    chunk_texts = []

    for sec in sections:

        text = f"""
Heading:
{sec['heading']}

Content:
{sec['content']}
"""

        chunk_texts.append(text)

    return chunk_texts


def create_embeddings(model, chunk_texts):

    embeddings = model.encode(
        chunk_texts,
        batch_size=16,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings