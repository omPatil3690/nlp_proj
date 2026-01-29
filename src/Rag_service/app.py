import streamlit as st
from task_builder import LLMtool
from json_chunker import JSONQuestionChunker
from vectorstore import FaissVectorStore
from search import RAGSearch

# ----------------------------
# Streamlit App Configuration
# ----------------------------
st.set_page_config(page_title="RAG Search Interface", layout="centered")

st.title("📘 RAG-based Question Answering System")
st.caption("Get questions from your previous year papers course PDFs or any uploaded new papers")

# ----------------------------
# Load or Initialize Components
# ----------------------------
@st.cache_resource
def load_components():
    llm_tool = LLMtool()
    chunker = JSONQuestionChunker()
    store = FaissVectorStore("faiss_store")
    try:
        store.load()
    except Exception as e:
        st.warning(f"Could not load FAISS index: {e}")
    rag_search = RAGSearch(llm_model="gemini-2.5-flash")
    return llm_tool, chunker, store, rag_search

llm_tool, chunker, store, rag_search = load_components()

# ----------------------------
# Sidebar: Upload & Process PDFs
# ----------------------------
st.sidebar.header("📄 Add PDF to Knowledge Base")
uploaded_pdf = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    with st.spinner("🔍 Extracting and processing PDF..."):
        extracted_text = llm_tool.ocr_pdf_with_genai(uploaded_pdf)
        tagged = llm_tool.tagger(extracted_text)
        question_chunks = chunker.json_to_chunks(tagged)
        embeddings = chunker.embed_chunks(question_chunks)
        store.build_from_question_chunks(question_chunks)
        st.sidebar.success("✅ PDF processed and added to FAISS store!")

# ----------------------------
# Main Interface: Ask a Question
# ----------------------------
st.subheader("💬 Ask a Question")
query = st.text_input("Enter your question Topic:", placeholder="e.g., Explain Unipolar and Differential Manchester encoding")

if st.button("🔎 Get questions") and query.strip():
    with st.spinner("Running hybrid RAG search..."):
        try:
            summary = rag_search.hybrid_search_and_summarize(query, top_k=3)
            st.success("✅ Retrieved successfully!")
            st.markdown("### 🧩 **Answer Summary:**")
            st.write(summary)

        except Exception as e:
            st.error(f"⚠️ Error during search: {e}")

# ----------------------------
# Optional: Debugging / Exploration
# ----------------------------
with st.expander("🔍 View Questions "):
    if query.strip():
        try:
            results = store.hybrid_query(query, top_k=3)
            for i, r in enumerate(results, start=1):
                st.markdown(f"**Chunk {i}:** {r.get('text', '')}")
                st.caption(f"Metadata: {r.get('metadata', {})}")
        except Exception:
            st.info("No chunks retrieved yet.")
