
import streamlit as st

from src.parser import extract_document
from src.chunking import build_sections

from src.embeddings import (
    load_embedding_model,
    create_chunk_texts,
    create_embeddings
)

from src.retrieval import (
    create_index,
    retrieve
)

from src.llm import generate_answer


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="PDF Intelligence Assistant",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color:#f7e8ee;
}

/* Hero Title */
.hero-title{
    font-size:42px;
    font-weight:700;
    color:#374151;
}

/* Hero Subtitle */
.hero-subtitle{
    color:#6b7280;
    font-size:18px;
    margin-top:8px;
}

/* Tech Badges */
.badge{
    display:inline-block;
    padding:6px 12px;
    margin:5px;
    border-radius:20px;
    background:#f9d4e3;
    color:#9d174d;
    font-size:12px;
    font-weight:500;
}

[data-testid="stFileUploader"]{
    background-color:#f9edf2;
    border:2px dashed #e8a4bf;
    border-radius:14px;
    padding:12px;
}
            
/* Answer Card */
.answer-card{
    padding:22px;
    border-radius:14px;
    background:#ffffff;
    border-left:5px solid #db2777;
    border-top:1px solid #e5e7eb;
    border-right:1px solid #e5e7eb;
    border-bottom:1px solid #e5e7eb;
}

/* Metrics */
[data-testid="metric-container"]{
    border-radius:12px;
    border:1px solid #e5e7eb;
    background:#fcf4f7;
}

/* Sources Expander */
.streamlit-expanderHeader{
    border-radius:10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("PDF Intelligence Assistant")

    st.markdown("""
### About

Upload a PDF and ask natural language questions.

### Tech Stack

- Docling
- Semantic Chunking
- BGE-M3
- FAISS
- Gemini

### Features

- PDF Parsing

- Semantic Retrieval

- Source Grounding

- AI Answer Generation
""")


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------

st.markdown("""
<div class="hero">

<div class="hero-title">
PDF Intelligence Assistant
</div>

<div class="hero-subtitle">
Ask questions from any PDF using Retrieval-Augmented Generation (RAG)
</div>

<br>

<span class="badge">Docling</span>
<span class="badge">BGE-M3</span>
<span class="badge">FAISS</span>
<span class="badge">Gemini</span>

</div>
""", unsafe_allow_html=True)

st.divider()


# --------------------------------------------------
# PDF UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


import os

if uploaded_file:

    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)

    pdf_path = os.path.join(
        "data",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Processing PDF..."):

        document = extract_document(pdf_path)

        sections = build_sections(document)

    # ------------------------------------------
    # EMBEDDING MODEL
    # ------------------------------------------

    if "embedding_model" not in st.session_state:

        with st.spinner("Loading embedding model..."):

            st.session_state.embedding_model = (
                load_embedding_model()
            )

    # ------------------------------------------
    # VECTOR STORE
    # ------------------------------------------

    if (
        "index" not in st.session_state
        or st.session_state.get("current_pdf")
        != uploaded_file.name
    ):

        with st.spinner("Building knowledge base..."):

            chunk_texts = create_chunk_texts(
                sections
            )

            embeddings = create_embeddings(
                st.session_state.embedding_model,
                chunk_texts
            )

            st.session_state.index = create_index(
                embeddings
            )

            st.session_state.sections = sections

            st.session_state.current_pdf = (
                uploaded_file.name
            )

    st.success("PDF processed successfully.")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Chunks Created",
            len(sections)
        )

    with col2:
        st.metric(
            "Document",
            uploaded_file.name
        )

    st.divider()

    # ------------------------------------------
    # QUESTION INPUT
    # ------------------------------------------

    query = st.text_input(
        "💬 Ask your PDF anything"
    )

    if query:

        retrieved_ids, scores = retrieve(
            query,
            st.session_state.embedding_model,
            st.session_state.index,
            top_k=5
        )

        context = ""

        sources = []

        for idx in retrieved_ids:

            section = st.session_state.sections[idx]

            context += f"""

Heading:
{section['heading']}

Content:
{section['content']}

"""

            sources.append(
                section["heading"]
            )

        with st.spinner("Generating answer..."):

            answer = generate_answer(
                query,
                context
            )

        st.markdown("## Answer")

        st.markdown(
            f"""
            <div class="answer-card">
            {answer}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("📚 Sources Used"):

            unique_sources = list(
                dict.fromkeys(sources)
            )

            for source in unique_sources:

                st.write(f"• {source}")