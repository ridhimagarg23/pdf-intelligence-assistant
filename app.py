
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

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

[data-testid="stAlert"]{
    background-color:#fdf2f8 !important;
    color:#9d174d !important;
    border:1px solid #fbcfe8 !important;
}

[data-testid="stFileUploader"]{
    background-color:#f9edf2;
    border:2px dashed #e8a4bf;
    border-radius:14px;
    padding:12px;
}

.stTextInput input{
    background-color:#fcf4f7 !important;
    border:1px solid #fbcfe8 !important;
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
            
[data-testid="chatAvatarIcon-user"]{
    display:none;
}

[data-testid="chatAvatarIcon-assistant"]{
    display:none;
}

[data-testid="stChatMessageAvatarUser"]{
    display:none;
}

[data-testid="stChatMessageAvatarAssistant"]{
    display:none;
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
- Heading-Aware Semantic Chunking
- BGE-M3 Embeddings
- FAISS Vector Search
- Gemini 2.5 Flash
- Multi-PDF RAG Chatbot

### Features

- PDF Parsing
- Semantic Retrieval
- Source Grounding
- AI Answer Generation
- Multi-PDF Question Answering
- Source Citations
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

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

import os

if uploaded_files:

    try:

        os.makedirs("data", exist_ok=True)

        all_document_text = ""
        all_pdf_names = []

        # -----------------------------
        # SAVE + PARSE ALL PDFs
        # -----------------------------

        with st.spinner("Parsing PDFs..."):

            for uploaded_file in uploaded_files:

                pdf_path = os.path.join(
                    "data",
                    uploaded_file.name
                )

                with open(pdf_path, "wb") as f:
                    f.write(
                        uploaded_file.getbuffer()
                    )

                document = extract_document(
                    pdf_path
                )

                all_document_text += "\n\n"
                all_document_text += document

                all_pdf_names.append(
                    uploaded_file.name
                )

        st.success(
            f"{len(uploaded_files)} PDF(s) parsed successfully"
        )

        # -----------------------------
        # CHUNKING
        # -----------------------------

        with st.spinner("Creating chunks..."):

            sections = build_sections(
                all_document_text
            )

        st.success(
            f"Knowledge chunks created: {len(sections)}"
        )

        # -----------------------------
        # EMBEDDING MODEL
        # -----------------------------

        if "embedding_model" not in st.session_state:

            with st.spinner(
                "Loading BGE-M3 model..."
            ):

                st.session_state.embedding_model = (
                    load_embedding_model()
                )

        # -----------------------------
        # VECTOR STORE
        # -----------------------------

        pdf_signature = "_".join(
            sorted(all_pdf_names)
        )

        if (
            "index" not in st.session_state
            or st.session_state.get("current_pdf")
            != pdf_signature
        ):

            with st.spinner(
                "Building vector database..."
            ):

                chunk_texts = create_chunk_texts(
                    sections
                )

                embeddings = create_embeddings(
                    st.session_state.embedding_model,
                    chunk_texts
                )

                st.session_state.index = (
                    create_index(
                        embeddings
                    )
                )

                st.session_state.sections = (
                    sections
                )

                st.session_state.current_pdf = (
                    pdf_signature
                )

                st.session_state.messages = []

        st.success(
            "Document knowledge base ready"
        )

        st.caption(
            f"{len(uploaded_files)} PDFs Loaded"
        )

        with st.expander(
            "Loaded Documents"
        ):

            for pdf_name in all_pdf_names:

                st.write(
                    f"📄 {pdf_name}"
                )

        st.divider()

        query = ""
        st.markdown("### Suggested Questions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Summarize Document"):
                query = "Summarize the uploaded document"
                
            if st.button("📚 Key Concepts"):
                query = "What are the key concepts in this document?"
                
        with col2:
            if st.button("⭐ Important Topics"):
                query = "List the important topics from this document"
            
            if st.button("📝 Create Study Notes"):
                query = "Create concise study notes from this document"


        # -----------------------------
        # QUESTION INPUT
        # -----------------------------

        user_query = st.text_input(
            "Ask a question about the uploaded PDFs"
        )

        if user_query:
            query = user_query

        if query:

            retrieved_ids, scores = retrieve(
                query,
                st.session_state.embedding_model,
                st.session_state.index,
                top_k=6
            )

            context = ""

            sources = []

            for idx in retrieved_ids:

                section = (
                    st.session_state.sections[idx]
                )

                context += f"""
                Heading:
                {section['heading']}
                Content:
                {section['content']}
"""

                sources.append(
                    {
                        "heading": section["heading"],
                        "content": section["content"]
                    }
                )

            with st.spinner(
                "Generating answer..."
            ):

                answer = generate_answer(
                    query,
                    context
                )

                st.session_state.messages.append(
                    {
                        "role": "user",
                        "content": query
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )
            
        st.markdown("## Conversation")
            
        for message in st.session_state.messages:
                
            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        if query:

            with st.expander(
                "Sources Used"
            ):

                for source in sources:

                    with st.expander(
                        f"{source['heading']}"
                    ):
                        
                        st.write(
                            source["content"][:500]
                        )

    except Exception as e:

        st.error(
            f"ERROR: {str(e)}"
        )

        st.exception(e)