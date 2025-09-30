#!/usr/bin/env python3
"""
Script to initialize Pinecone vector database with BJJ techniques
Run this once to set up the vector database
"""

from vector_db import BJJVectorDB
import os

def main():
    print("🤼 Initializing BJJ Vector Database...")
    
    # Check for Pinecone API key
    if not os.getenv('PINECONE_API_KEY'):
        print("❌ PINECONE_API_KEY not found in environment variables")
        print("Please set your Pinecone API key:")
        print("1. Go to https://app.pinecone.io/")
        print("2. Create an account and get your API key")
        print("3. Set PINECONE_API_KEY in your .env file")
        return
    
    # Initialize vector database
    vector_db = BJJVectorDB()
    
    if not vector_db.model:
        print("❌ Failed to initialize vector database")
        return
    
    # Load and process techniques
    try:
        stats = vector_db.initialize_from_json("bjj_moves.json")
        print(f"✅ Success! Vector database initialized with {stats['total_vectors']} techniques")
        print(f"📊 Index dimension: {stats['dimension']}")
        print(f"📈 Index fullness: {stats['index_fullness']:.2%}")
        
    except Exception as e:
        print(f"❌ Error initializing vector database: {e}")

if __name__ == "__main__":
    main()
