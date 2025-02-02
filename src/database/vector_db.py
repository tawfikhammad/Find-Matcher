import chromadb
from chromadb.utils import embedding_functions
from config import settings

class VectorDBManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.vector_db_config["path"])
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.vector_db_config["embedding_model"]
        )
        
        self.collection = self.client.get_or_create_collection(
            name=settings.vector_db_config["name"],
            metadata={"hnsw:space": "cosine"},
            embedding_function=self.embedding_fn
        )

    def is_collection_empty(self) -> bool:
        return len(self.collection.get()["ids"]) == 0

    def store_document(self, document: dict):
        self.collection.add(
            documents=document["content"],
            metadatas=document["metadata"],
            ids=document["pdf_filename"]
        )

    def search_documents(self, query: str, top_k: int = 5) -> list:
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["metadatas"]  
        )
        return results["metadatas"][0]