import chromadb
from ..vdb_interface import VDBInterface
from chromadb.utils import embedding_functions
from config import settings
from typing import Dict, Any, List, Optional
import logging

class ChromaProvider(VDBInterface):
    def __init__(self, db_path: str, embedding_model: str, distance_method: str = "cosine"):
        self.logger = logging.getLogger(__name__)

        self.client = None
        self.collection = None
        self.embedding_fn = None

        self.db_path = db_path
        self.distance_method = distance_method
        self.embedding_model = embedding_model

        self._initialize_client()
        
    def _initialize_client(self):
        try:
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.distance_method
        )
            self.logger.info(f"ChromaDB client initialized with model: {self.distance_method}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise

    def initialize_collection(self, collection_name: str) -> None:
        try:
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": self.distance_method},
                embedding_function=self.embedding_fn)
            
            self.logger.info(f"Collection '{collection_name}' initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize collection '{collection_name}': {e}")
            raise
    
    def is_collection_empty(self) -> bool:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            return len(self.collection.get()["ids"]) == 0
        except Exception as e:
            self.logger.error(f"Error checking if collection is empty: {e}")
            return True
        
    def store_document(self, document: Dict[str, Any]) -> None:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            self.collection.add(
                documents=[document["content"]],
                metadatas=[document.get("metadata", {})],
                ids=[document["id"]]
            )
            self.logger.debug(f"Document stored with ID: {document['id']}")
            
        except Exception as e:
            self.logger.error(f"Failed to store document {document.get('id', 'unknown')}: {e}")
            raise

    def store_documents_batch(self, documents: List[Dict[str, Any]]) -> None:
        """Store multiple documents in batch."""
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        if not documents:
            return
        
        try:
            contents = [doc["content"] for doc in documents]
            metadatas = [doc.get("metadata", {}) for doc in documents]
            ids = [doc["id"] for doc in documents]
            
            self.collection.add(
                documents=contents,
                metadatas=metadatas,
                ids=ids
            )
            
            self.logger.info(f"Batch stored {len(documents)} documents")
            
        except Exception as e:
            self.logger.error(f"Failed to store documents batch: {e}")
            raise
    
    def search_documents(self, query: str, top_k: int = 5, **kwargs) -> List[Dict[str, Any]]:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            include_fields = kwargs.get("include", ["metadatas", "documents"])
            
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                include=include_fields
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                result = {
                    "id": results["ids"][0][i],
                    "metadata": results.get("metadatas", [{}])[0][i] if results.get("metadatas") else {},
                }
                
                if "documents" in include_fields and results.get("documents"):
                    result["content"] = results["documents"][0][i]
                
                formatted_results.append(result)
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Search failed for query '{query}': {e}")
            raise

    def delete_document(self, document_id: str) -> bool:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            self.collection.delete(ids=[document_id])
            self.logger.debug(f"Document deleted with ID: {document_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete document {document_id}: {e}")
            return False
    
    def update_document(self, document_id: str, document: Dict[str, Any]) -> bool:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            self.collection.update(
                ids=[document_id],
                documents=[document["content"]],
                metadatas=[document.get("metadata", {})]
            )
            self.logger.debug(f"Document updated with ID: {document_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update document {document_id}: {e}")
            return False
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID."""
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            results = self.collection.get(
                ids=[document_id],
                include=["metadatas", "documents"]
            )
            
            if not results["ids"]:
                return None
            
            return {
                "id": results["ids"][0],
                "content": results["documents"][0] if results.get("documents") else "",
                "metadata": results["metadatas"][0] if results.get("metadatas") else {}
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get document {document_id}: {e}")
            return None
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection."""
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            all_data = self.collection.get()
            return {
                "total_documents": len(all_data["ids"]),
                "collection_name": self.collection.name,
                "embedding_model": self.config.get("embedding_model"),
                "distance_metric": self.collection.metadata.get("hnsw:space", "unknown")
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def clear_collection(self) -> None:
        if not self.collection:
            raise ValueError("Collection not initialized")
        
        try:
            # Get all document IDs
            all_data = self.collection.get()
            if all_data["ids"]:
                self.collection.delete(ids=all_data["ids"])
                self.logger.info("Collection cleared successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to clear collection: {e}")
            raise
    
    def close_connection(self) -> None:
        """Close the database connection."""
        try:
            if self.client:
                # ChromaDB doesn't have an explicit close method but we will reset
                self.collection = None
                self.client = None
                self.logger.info("ChromaDB connection closed")
                
        except Exception as e:
            self.logger.error(f"Error closing ChromaDB connection: {e}")
            raise