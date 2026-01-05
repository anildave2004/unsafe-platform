"""
Mock vector store for context retrieval.
Simulates a vector database for storing and retrieving contextual information.
"""
from typing import List, Dict, Any, Optional
import json


class MockVectorStore:
    """Mock vector store for similarity search and context retrieval."""
    
    def __init__(self):
        """Initialize the mock vector store with sample data."""
        self.documents = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Populate store with sample historical incident data."""
        self.documents = [
            {
                "id": "doc_001",
                "content": "Historical incident: Temperature spike in industrial equipment led to $45,000 in damages.",
                "metadata": {
                    "incident_type": "temperature_anomaly",
                    "severity": "critical",
                    "cost": 45000
                }
            },
            {
                "id": "doc_002",
                "content": "Historical incident: Vibration anomaly in motor caused bearing failure, $30,000 repair cost.",
                "metadata": {
                    "incident_type": "vibration_anomaly",
                    "severity": "high",
                    "cost": 30000
                }
            },
            {
                "id": "doc_003",
                "content": "Historical incident: Network connectivity loss resulted in $5,000 operational delay.",
                "metadata": {
                    "incident_type": "network_issue",
                    "severity": "medium",
                    "cost": 5000
                }
            },
            {
                "id": "doc_004",
                "content": "Best practice: Temperature anomalies require immediate shutdown to prevent catastrophic failure.",
                "metadata": {
                    "type": "best_practice",
                    "topic": "temperature_management"
                }
            },
            {
                "id": "doc_005",
                "content": "Mitigation strategy: For vibration issues, schedule preventive maintenance within 24 hours.",
                "metadata": {
                    "type": "mitigation_strategy",
                    "topic": "vibration_management"
                }
            }
        ]
    
    def search(
        self,
        query: str,
        top_k: int = 3,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant documents.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional metadata filters
            
        Returns:
            List of relevant documents with content and metadata
        """
        # Simple keyword-based mock search
        results = []
        query_lower = query.lower()
        
        for doc in self.documents:
            relevance_score = 0.0
            content_lower = doc["content"].lower()
            
            # Calculate simple relevance score based on keyword matching
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in content_lower:
                    relevance_score += 1.0
            
            # Apply filters if provided
            if filters:
                match = all(
                    doc["metadata"].get(key) == value
                    for key, value in filters.items()
                )
                if not match:
                    continue
            
            if relevance_score > 0:
                results.append({
                    "document": doc,
                    "score": relevance_score
                })
        
        # Sort by relevance score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return [r["document"] for r in results[:top_k]]
    
    def add_document(
        self,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        doc_id: Optional[str] = None
    ) -> str:
        """Add a document to the vector store.
        
        Args:
            content: Document content text
            metadata: Optional metadata dictionary
            doc_id: Optional document ID (auto-generated if not provided)
            
        Returns:
            Document ID
        """
        if doc_id is None:
            doc_id = f"doc_{len(self.documents) + 1:03d}"
        
        document = {
            "id": doc_id,
            "content": content,
            "metadata": metadata or {}
        }
        
        self.documents.append(document)
        return doc_id
    
    def get_context(self, incident_type: str, severity: str) -> str:
        """Get contextual information for an incident.
        
        Args:
            incident_type: Type of incident
            severity: Severity level
            
        Returns:
            Formatted context string
        """
        query = f"{incident_type} {severity}"
        results = self.search(query, top_k=2)
        
        if not results:
            return "No relevant historical context found."
        
        context_parts = []
        for i, doc in enumerate(results, 1):
            context_parts.append(f"Context {i}: {doc['content']}")
        
        return "\n".join(context_parts)


def get_vector_store() -> MockVectorStore:
    """Factory function to get vector store instance.
    
    Returns:
        MockVectorStore instance
    """
    return MockVectorStore()
