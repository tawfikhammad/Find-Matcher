from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class VDBInterface(ABC):
    
    @abstractmethod
    def initialize_collection(self, collection_name: str, **kwargs) -> None:
        """Initialize or create a collection in the vector database."""
        pass
    
    @abstractmethod
    def is_collection_empty(self) -> bool:
        """Check if the collection is empty."""
        pass
    
    @abstractmethod
    def store_document(self, document: Dict[str, Any]) -> None:
        """Store a document in the vector database.
        
        Args:
            document: Dictionary containing document data with keys:
                - content: Document text content
                - metadata: Document metadata
                - id: Unique document identifier
        """
        pass
    
    @abstractmethod
    def store_documents_batch(self, documents: List[Dict[str, Any]]) -> None:
        """Store multiple documents in batch.
        
        Args:
            documents: List of document dictionaries
        """
        pass
    
    @abstractmethod
    def search_documents(self, query: str, top_k: int = 5, **kwargs) -> List[Dict[str, Any]]:
        """Search for similar documents.
        
        Args:
            query: Search query text
            top_k: Number of top results to return
            **kwargs: Additional search parameters
            
        Returns:
            List of matching documents with metadata
        """
        pass
    
    @abstractmethod
    def delete_document(self, document_id: str) -> bool:
        """Delete a document by ID.
        
        Args:
            document_id: Unique identifier of the document
            
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def update_document(self, document_id: str, document: Dict[str, Any]) -> bool:
        """Update an existing document.
        
        Args:
            document_id: Unique identifier of the document
            document: Updated document data
            
        Returns:
            True if update was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a document by ID.
        
        Args:
            document_id: Unique identifier of the document
            
        Returns:
            Document data if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection.
        
        Returns:
            Dictionary containing collection statistics
        """
        pass
    
    @abstractmethod
    def clear_collection(self) -> None:
        """Clear all documents from the collection."""
        pass
    
    @abstractmethod
    def close_connection(self) -> None:
        """Close the database connection."""
        pass