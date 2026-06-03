from sentence_transformers import SentenceTransformer


def load_embedding_model():

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    return model


def create_chunk_texts(sections):

    chunk_texts = []

    current_context = "Document"

    for sec in sections:

        heading = sec["heading"]

        if heading.upper().startswith("LAB EXPERIMENT"):
            current_context = heading

        text = f"""
Document Context:
Software Engineering Lab

Section Context:
{current_context}

Heading:
{heading}

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