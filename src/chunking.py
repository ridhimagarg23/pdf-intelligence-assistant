def build_sections(markdown_text):

    chunks = []

    chunk_size = 1000
    overlap = 200

    start = 0

    while start < len(markdown_text):

        end = start + chunk_size

        chunk = markdown_text[start:end]

        chunks.append(
            {
                "heading": f"Chunk {len(chunks)+1}",
                "content": chunk
            }
        )

        start += (chunk_size - overlap)

    return chunks