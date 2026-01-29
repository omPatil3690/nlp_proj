# 🧠 Hybrid Search RAG System

A powerful Retrieval-Augmented Generation (RAG) system using hybrid search combining vector similarity and keyword-based retrieval for intelligent document analysis and question answering.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Setup Instructions](#project-setup-instructions)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Technology Stack](#technology-stack)
- [Usage](#usage)
- [Key Components](#key-components)
- [Results](#results)

---

## 🎯 Overview

This project implements a sophisticated RAG (Retrieval-Augmented Generation) system that leverages Google Gemini API for intelligent document analysis. The system uses a hybrid search approach combining vector embeddings (FAISS) with traditional keyword matching to retrieve the most relevant documents and generate accurate, context-aware responses.

**Perfect for**: Research paper analysis, document Q&A, information retrieval, and intelligent summarization.

---

## ✨ Features

- **🔍 Hybrid Search**: Combines vector similarity search with keyword-based retrieval
- **📚 PDF Processing**: Automatic extraction and chunking of PDF documents
- **🧬 Embeddings**: Uses advanced embedding models for semantic search
- **🤖 AI-Powered Responses**: Google Gemini API for intelligent answer generation
- **💾 Vector Database**: FAISS-based persistent storage for scalable retrieval
- **🎨 Interactive UI**: Streamlit-based user-friendly interface
- **📊 Metadata Management**: Comprehensive tracking of document sources and metadata

---

## 🚀 Project Setup Instructions

### Step 1: Download the Project Code Base

Clone or download the project repository to your local system:

```bash
git clone <repository_url>
cd nlp_proj
```

---

### Step 2: Create a Virtual Environment

Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

---

### Step 3: Set up Google Gemini API Key

1. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/)
2. Create a `.env` file in the main directory of your project
3. Add your API key as follows:

```env
GOOGLE_API_KEY="your_api_key_here"
```

---

### Step 4: Install Required Dependencies

In the terminal (with the virtual environment active), run:

```bash
pip install -r requirements.txt
```

---

### Step 5: Navigate to RAG Service Directory

Move into the RAG service directory:

```bash
cd src/Rag_service
```

---

### Step 6: Run the Streamlit App

Finally, launch the app using:

```bash
streamlit run app.py
```

The application will start on `http://localhost:8501`

---

## 📁 Project Structure

```
nlp_proj/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── notes.txt                          # Project notes
├── .env                               # Environment variables (API keys)
├── hybrid_search_rag (1).ipynb        # Jupyter notebook for experimentation
└── src/
    └── Rag_service/
        ├── app.py                     # Main Streamlit application
        ├── data_loader.py             # PDF and document loading utilities
        ├── embedding.py               # Embedding generation and management
        ├── vectorstore.py             # FAISS vector database management
        ├── search.py                  # Hybrid search implementation
        ├── json_chunker.py            # JSON document chunking
        ├── task_builder.py            # Task/prompt building
        ├── test.py                    # Unit tests
        ├── test2.py                   # Additional tests
        ├── data/                      # Sample PDF documents
        │   ├── 𝗔 𝗗𝗲𝗲𝗽𝗲𝗿 𝗗𝗶𝘃𝗲 𝗢𝘂𝗿 𝗝.txt
        │   └── 𝗢𝗽𝗲𝗻 𝗦𝗼𝘂𝗿𝗰𝗲 𝗔𝗱𝘃𝗲𝗻𝘁.txt
        ├── faiss_store/               # FAISS index storage
        │   ├── faiss.index            # Vector index
        │   ├── metadata_summary.csv   # Metadata in CSV format
        │   └── metadata_summary.json  # Metadata in JSON format
        └── __pycache__/               # Python cache files
```

---

## 🖼️ Screenshots

### Data Ingestion Phase

> **Note**: In this demo, we've added sample documents to the embedding database. In production, we have 30+ research papers indexed in the embedding database. When querying the model, it performs vector searching across all embeddings.

**Screenshot 1: Application Interface**
```
[Insert Screenshot 1 - App.py running interface]
```

**Screenshot 2: Data Processing**
```
[Insert Screenshot 2 - Data ingestion/processing]
```

**Screenshot 3: Search and Results**
```
[Insert Screenshot 3 - Query results]
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **LLM** | Google Gemini API |
| **Embeddings** | Advanced embedding models |
| **Vector DB** | FAISS (Facebook AI Similarity Search) |
| **Frontend** | Streamlit |
| **Backend** | Python 3.x |
| **PDF Processing** | PyPDF2 / pdf2image |
| **Data Format** | JSON, CSV |

---

## 💻 Usage

1. **Start the Application**
   ```bash
   cd src/Rag_service
   streamlit run app.py
   ```

2. **Upload Documents** (Optional)
   - Use the interface to upload PDF files
   - Documents are automatically processed and indexed

3. **Ask Questions**
   - Enter your query in the search box
   - The system performs hybrid search across the vector database
   - Gemini AI generates a contextual answer based on retrieved documents

4. **View Results**
   - Get relevant document chunks with similarity scores
   - AI-generated comprehensive answers
   - Source attribution for transparency

---

## 🔧 Key Components

### `app.py`
Main Streamlit application providing the user interface and orchestrating the RAG pipeline.

### `data_loader.py`
Handles PDF/document loading and preprocessing for ingestion into the system.

### `embedding.py`
Manages embedding generation and encoding of documents and queries.

### `vectorstore.py`
Manages FAISS vector index creation, storage, and retrieval operations.

### `search.py`
Implements the hybrid search algorithm combining vector similarity and keyword matching.

### `json_chunker.py`
Handles chunking of JSON-formatted documents into manageable segments.

### `task_builder.py`
Constructs prompts and tasks for the Gemini API to generate responses.

---

## 📊 Results

### Data Ingestion Phase

The system successfully ingests and processes documents through the following pipeline:

1. **Document Loading**: PDFs and text files are loaded from the `data/` directory
2. **Chunking**: Documents are intelligently chunked into semantic segments
3. **Embedding Generation**: Each chunk is converted to vector embeddings
4. **Index Creation**: Vectors are indexed in FAISS for fast retrieval
5. **Metadata Storage**: Document metadata is stored in JSON and CSV formats

### Search and Retrieval

- **Hybrid Search**: Combines BM25 keyword matching with vector similarity
- **Relevance Ranking**: Results ranked by combined relevance scores
- **Context Preservation**: Retrieved chunks maintain document context
- **Source Attribution**: All answers include source references

### AI-Powered Responses

- **Context-Aware Answers**: Gemini API generates responses based on retrieved context
- **Multi-Source Synthesis**: Combines information from multiple documents
- **Citation Support**: Includes references to source documents

---

## 🎓 How Hybrid Search Works

```
User Query
    ↓
┌───────────────────────────────────┐
│   Vector Embedding Generation     │
└───────────────────────────────────┘
    ↓                    ↓
┌─────────────┐   ┌──────────────┐
│Vector Search│   │Keyword Search│
│  (FAISS)    │   │   (BM25)     │
└─────────────┘   └──────────────┘
    ↓                    ↓
┌───────────────────────────────────┐
│    Hybrid Result Ranking          │
└───────────────────────────────────┘
    ↓
┌───────────────────────────────────┐
│  Context-Aware LLM Response       │
│     (Google Gemini API)           │
└───────────────────────────────────┘
    ↓
User Gets Answer with Sources
```

---

## 📝 Notes

- **Demo Setup**: Currently configured with sample documents for demonstration purposes
- **Production Scaling**: System is designed to handle large document collections (30+ papers tested)
- **API Limits**: Ensure your Gemini API quota is sufficient for your use case
- **Vector Index**: FAISS index is persistent and stored locally in `faiss_store/`

---

## 🔐 Environment Variables

Ensure your `.env` file contains:

```env
GOOGLE_API_KEY=your_actual_api_key_here
```

**⚠️ Important**: Never commit the `.env` file to version control!

---

## 📚 Dependencies

See `requirements.txt` for the complete list of dependencies. Key packages include:

- `streamlit` - Web framework
- `google-generativeai` - Gemini API client
- `faiss-cpu` - Vector similarity search
- `PyPDF2` - PDF processing
- `python-dotenv` - Environment variable management

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests

---

## 📄 License

This project is part of IIIT Nanded 5th Semester NLP coursework.

---

## 👨‍💻 Author

**Sandesh Lavshetty**
- IIIT Nanded, 1st Year, 5th Semester
- NLP Project

---

## 🆘 Troubleshooting

### Issue: "GOOGLE_API_KEY not found"
**Solution**: Ensure your `.env` file exists in the project root with your API key.

### Issue: "No module named 'streamlit'"
**Solution**: Run `pip install -r requirements.txt` with your virtual environment activated.

### Issue: "FAISS index not found"
**Solution**: Run the data ingestion process first or check the `faiss_store/` directory exists.

### Issue: "Port 8501 already in use"
**Solution**: Run `streamlit run app.py --server.port 8502` to use a different port.

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the project notes in `notes.txt`
3. Check the Jupyter notebook `hybrid_search_rag.ipynb` for examples

---

**Happy Searching! 🔍**
