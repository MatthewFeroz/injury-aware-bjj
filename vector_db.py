import os
import json
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BJJVectorDB:
    def __init__(self):
        """Initialize Pinecone vector database for BJJ techniques"""
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.index_name = "bjj-techniques"
        
        if not self.pinecone_api_key:
            print("Warning: PINECONE_API_KEY not found in environment variables")
            self.model = None
            self.index = None
            return
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Pinecone
        self.pc = Pinecone(api_key=self.pinecone_api_key)
        
        # Get or create index
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384,  # all-MiniLM-L6-v2 dimension
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
        
        self.index = self.pc.Index(self.index_name)
    
    def load_techniques_from_json(self, json_file: str) -> List[Dict[str, Any]]:
        """Load BJJ techniques from JSON file"""
        with open(json_file, 'r') as f:
            return json.load(f)
    
    def create_embeddings(self, techniques: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create embeddings for BJJ techniques"""
        if not self.model:
            return []
        
        embeddings_data = []
        
        for i, technique in enumerate(techniques):
            # Create text representation of the technique
            text = f"{technique['technique']} "
            text += f"Primary joint: {technique['primary_joint']} "
            text += f"Stress type: {' '.join(technique['stress_type'])} "
            text += f"Unsafe for: {' '.join(technique['unsafe_for'])} "
            text += f"Safe for: {' '.join(technique['safe_for'])}"
            
            # Generate embedding
            embedding = self.model.encode(text)
            
            embeddings_data.append({
                'id': f"technique_{i}",
                'values': embedding.tolist(),
                'metadata': {
                    'technique': technique['technique'],
                    'primary_joint': technique['primary_joint'],
                    'stress_type': technique['stress_type'],
                    'unsafe_for': technique['unsafe_for'],
                    'safe_for': technique['safe_for']
                }
            })
        
        return embeddings_data
    
    def upsert_techniques(self, embeddings_data: List[Dict[str, Any]]):
        """Upload techniques to Pinecone"""
        if not self.index:
            print("Pinecone not initialized")
            return
        
        # Upsert in batches
        batch_size = 100
        for i in range(0, len(embeddings_data), batch_size):
            batch = embeddings_data[i:i + batch_size]
            self.index.upsert(vectors=batch)
            print(f"Uploaded batch {i//batch_size + 1}/{(len(embeddings_data) + batch_size - 1)//batch_size}")
    
    def search_similar_techniques(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for similar techniques based on query"""
        if not self.model or not self.index:
            return []
        
        # Generate embedding for query
        query_embedding = self.model.encode(query)
        
        # Search Pinecone
        results = self.index.query(
            vector=query_embedding.tolist(),
            top_k=top_k,
            include_metadata=True
        )
        
        return results['matches']
    
    def search_by_injuries(self, injuries: List[str], top_k: int = 10) -> List[Dict[str, Any]]:
        """Search for techniques based on injury descriptions"""
        if not injuries:
            return []
        
        # Create query from injuries
        query = f"Injuries: {' '.join(injuries)}"
        return self.search_similar_techniques(query, top_k)
    
    def get_technique_stats(self) -> Dict[str, int]:
        """Get statistics about the vector database"""
        if not self.index:
            return {"total_vectors": 0}
        
        stats = self.index.describe_index_stats()
        return {
            "total_vectors": stats.total_vector_count,
            "dimension": stats.dimension,
            "index_fullness": stats.index_fullness
        }
    
    def initialize_from_json(self, json_file: str = "bjj_moves.json"):
        """Initialize the vector database from JSON file"""
        print("Loading techniques from JSON...")
        techniques = self.load_techniques_from_json(json_file)
        
        print(f"Creating embeddings for {len(techniques)} techniques...")
        embeddings_data = self.create_embeddings(techniques)
        
        print("Uploading to Pinecone...")
        self.upsert_techniques(embeddings_data)
        
        print("Vector database initialized successfully!")
        return self.get_technique_stats()
