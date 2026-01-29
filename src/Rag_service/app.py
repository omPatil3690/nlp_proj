import streamlit as st
import os
from task_builder import LLMtool
from json_chunker import JSONQuestionChunker
from vectorstore import FaissVectorStore
from search import RAGSearch

# ----------------------------
# Streamlit App Configuration
# ----------------------------
st.set_page_config(page_title="RAG Search Interface", layout="wide")

# Initialize session state for API key
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

st.title("🧠 Hybrid Search RAG System")
st.markdown("""
<div style='font-size: 16px; color: #888;'>
LLM-powered document Q&A using vector + keyword retrieval
</div>
""", unsafe_allow_html=True)
st.caption("Ask questions from your document collection. The system retrieves relevant context and generates answers using Google Gemini API.")

# ----------------------------
# API Key Section at Top
# ----------------------------
st.markdown("---")
api_col1, api_col2 = st.columns([3, 1])

with api_col1:
    api_input = st.text_input(
        "🔑 Enter your Google Gemini API Key (Required for RAG & PDF processing):",
        type="password",
        placeholder="paste-your-api-key-here",
        value=st.session_state.user_api_key,
        key="api_key_main"
    )
    
    if api_input != st.session_state.user_api_key:
        st.session_state.user_api_key = api_input
        if api_input:
            os.environ["GOOGLE_API_KEY"] = api_input
            st.success("✅ API Key set!")

with api_col2:
    if st.link_button("Get Free API Key", "https://aistudio.google.com/"):
        pass

if not st.session_state.user_api_key:
    st.info("⚠️ Enter your API key above to use RAG search and PDF upload features. Get it free at aistudio.google.com")

st.markdown("---")

# ----------------------------
# Helper Function: Check and Get API Key
# ----------------------------
def get_api_key():
    """Check for API key in environment or session"""
    if st.session_state.user_api_key:
        return st.session_state.user_api_key
    if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"]:
        return os.environ["GOOGLE_API_KEY"]
    return None

def require_api_key(feature_name="this feature"):
    """Check if API key is provided"""
    api_key = get_api_key()
    
    if not api_key:
        st.error(f"🔑 API Key Required: Please enter your Google Gemini API key at the top to use {feature_name}")
        return None
    
    return api_key

# ----------------------------
# Load or Initialize Components
# ----------------------------
@st.cache_resource
def load_components(api_key=None):
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    
    llm_tool = LLMtool()
    chunker = JSONQuestionChunker()
    store = FaissVectorStore("faiss_store")
    try:
        store.load()
        st.sidebar.success("✅ FAISS index loaded")
    except Exception as e:
        st.sidebar.warning(f"Could not load FAISS index: {e}")
    rag_search = RAGSearch(llm_model="gemini-2.5-flash")
    return llm_tool, chunker, store, rag_search

# Initialize components
api_key = get_api_key()
llm_tool, chunker, store, rag_search = load_components(api_key)

# ----------------------------
# Sidebar: Upload & Process PDFs
# ----------------------------
st.sidebar.header("📄 Add PDF to Knowledge Base")

if st.sidebar.button("ℹ️ How to add PDFs?"):
    st.sidebar.info("""
    1. Click 'Browse files' below
    2. Select a PDF from your computer
    3. The system will extract text, create embeddings, and add to knowledge base
    """)

uploaded_pdf = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_pdf:
    api_key = require_api_key("PDF processing")
    
    if api_key:
        with st.spinner("🔍 Extracting and processing PDF..."):
            try:
                extracted_text = llm_tool.ocr_pdf_with_genai(uploaded_pdf)
                tagged = llm_tool.tagger(extracted_text)
                question_chunks = chunker.json_to_chunks(tagged)
                embeddings = chunker.embed_chunks(question_chunks)
                store.build_from_question_chunks(question_chunks)
                st.sidebar.success("✅ PDF processed and added to FAISS store!")
            except Exception as e:
                error_str = str(e).lower()
                if "api_key_invalid" in error_str or "invalid api key" in error_str or "400" in error_str:
                    st.sidebar.error("""
                    ❌ **Invalid API Key**
                    
                    Your API key appears to be invalid. Please:
                    1. Go to https://aistudio.google.com/
                    2. Generate a new API key
                    3. Copy and paste it in the 🔑 API Key field at the top
                    4. Try uploading the PDF again
                    """)
                elif "quota" in error_str or "rate" in error_str:
                    st.sidebar.error("""
                    ⚠️ **API Quota Exceeded**
                    
                    You've exceeded your daily API quota. Please:
                    - Try again tomorrow, or
                    - Upgrade your Google Gemini API plan
                    """)
                else:
                    st.sidebar.error(f"""
                    ❌ **PDF Processing Error**
                    
                    Error: {e}
                    
                    **Try:**
                    1. Ensure the PDF is not corrupted
                    2. Check your API key is correct
                    3. Try a smaller PDF file
                    """)


# ----------------------------
# Main Interface: Ask a Question
# ----------------------------
st.subheader("💬 Ask a Question")
query = st.text_input("Enter your question Topic:", placeholder="e.g., Explain Unipolar and Differential Manchester encoding")

if st.button("🔎 Get questions") and query.strip():
    api_key = require_api_key("RAG search")
    
    if api_key:
        with st.spinner("Running hybrid RAG search..."):
            try:
                summary = rag_search.hybrid_search_and_summarize(query, top_k=3)
                st.success("✅ Retrieved successfully!")
                st.markdown("### 🧩 **Answer Summary:**")
                st.write(summary)

            except Exception as e:
                error_str = str(e).lower()
                if "api_key_invalid" in error_str or "invalid api key" in error_str or "400" in error_str:
                    st.error("""
                    ❌ **Invalid or Missing API Key**
                    
                    The API key you entered is invalid. Please:
                    1. Check that you copied the API key correctly from https://aistudio.google.com/
                    2. Ensure there are no extra spaces or characters
                    3. Update the 🔑 API Key field at the top with a new/correct key
                    4. Try your search again
                    """)
                elif "quota" in error_str or "rate" in error_str:
                    st.error("""
                    ⚠️ **API Usage Limit Reached**
                    
                    You've hit your daily API quota. Please:
                    - Try again tomorrow, or
                    - Upgrade your plan at https://aistudio.google.com/
                    """)
                elif "no chunks" in error_str or "not found" in error_str:
                    st.warning("""
                    📭 **No Results Found**
                    
                    The system couldn't find relevant documents. Try:
                    1. Upload more PDF documents first
                    2. Use different search keywords
                    3. Check that documents are in the knowledge base
                    """)
                else:
                    st.error(f"""
                    ❌ **Search Error**
                    
                    **Issue:** {e}
                    
                    **Try:**
                    1. Verify your API key is correct
                    2. Check your internet connection
                    3. Try a simpler search query
                    4. Upload sample documents first
                    """)

# ----------------------------
# Optional: Debugging / Exploration
# ----------------------------
with st.expander("🔍 View Questions "):
    if query.strip():
        api_key = get_api_key()
        if api_key and store:
            try:
                results = store.hybrid_query(query, top_k=3)
                for i, r in enumerate(results, start=1):
                    st.markdown(f"**Chunk {i}:** {r.get('text', '')}")
                    st.caption(f"Metadata: {r.get('metadata', {})}")
            except Exception:
                st.info("No chunks retrieved yet.")
        else:
            st.info("📌 Enter an API key and ask a question first to see results.")
