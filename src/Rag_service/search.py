import os
from dotenv import load_dotenv
from vectorstore import FaissVectorStore
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

class RAGSearch:
    def __init__(self, persist_dir: str = "faiss_store", embedding_model: str = "all-MiniLM-L6-v2", llm_model: str = "gemma2-9b-it"):
        self.vectorstore = FaissVectorStore(persist_dir, embedding_model)
        # Load or build vectorstore
        faiss_path = os.path.join(persist_dir, "faiss.index")
        meta_path = os.path.join(persist_dir, "metadata.pkl")
        if not (os.path.exists(faiss_path) and os.path.exists(meta_path)):
            from src.Rag_service.data_loader import load_all_documents
            docs = load_all_documents("data")
            self.vectorstore.build_from_documents(docs)
        else:
            self.vectorstore.load()
        # Initialize Groq LLM
        if "GROQ_API_KEY" in os.environ:
            groq_api_key = os.environ["GROQ_API_KEY"]
            # self.llm = ChatGroq(groq_api_key=groq_api_key, model_name=llm_model)
            print(f"[INFO] Groq LLM initialized: {llm_model}")
        elif "GOOGLE_API_KEY" in os.environ:
            google_api_key = os.environ["GOOGLE_API_KEY"]
            self.llm = ChatGoogleGenerativeAI(google_api_key=google_api_key, model=llm_model)
            print(f"[INFO] Google LLM initialized: {llm_model}")

    def search_and_summarize(self, query: str, top_k: int = 5) -> str:
        results = self.vectorstore.query(query, top_k=top_k)
        texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        context = "\n\n".join(texts)
        if not context:
            return "No relevant documents found."
        prompt = f"""Summarize the following context for the query: '{query}'\n\nContext:\n{context}\n\nSummary:"""
        response = self.llm.invoke([prompt])
        return response.content

    def hybrid_search_and_summarize(self, query: str, alpha: float = 0.7, top_k: int = 5):
        results = self.vectorstore.hybrid_query(query, alpha=alpha, top_k=top_k)
        # texts = [r["metadata"].get("text", "") for r in results if r["metadata"]]
        texts = results
        # context = "\n\n".join(texts)
        context = texts
        if not context:
            return "No relevant questions found."
        prompt = f"""
            You are an expert exam assistant. Use only the below question paper context to answer the user's query clearly and concisely.

            Each context entry represents a real exam question with metadata.

            Context:
            {{
            {chr(10).join([
                f"- [{i+1}] ({c['metadata']['subject_name']} | {c['metadata']['paper_code']} | {c['metadata']['type_of_exam']} on {c['metadata']['date_of_exam']}) "
                f"QID: {c['metadata']['question_id']} → {c['metadata']['question_text']}"
                for i, c in enumerate(context)
            ])}
            }}

            User Query:
            {query}

            Instructions:
            - Identify which one or more context questions are most relevant to the user’s query.
            - Use only those relevant context questions to form your answer.
            - Do not invent or assume any new information outside the given context.
            - If none of the questions are relevant, respond with: "No relevant information found in the given question papers."

            Final Answer:
            """
        response = self.llm.invoke([prompt])
        return response.content

# Example usage
if __name__ == "__main__":
    rag_search = RAGSearch()
    query = "What is attention mechanism?"
    summary = rag_search.search_and_summarize(query, top_k=3)
    print("Summary:", summary)
