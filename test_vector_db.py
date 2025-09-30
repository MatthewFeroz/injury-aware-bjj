#!/usr/bin/env python3
"""
Test script for Pinecone vector database integration
"""

from vector_db import BJJVectorDB
import os

def test_vector_db():
    print("🧪 Testing BJJ Vector Database...")
    
    # Check for Pinecone API key
    if not os.getenv('PINECONE_API_KEY'):
        print("❌ PINECONE_API_KEY not found")
        print("Please set your Pinecone API key in .env file")
        return False
    
    # Initialize vector database
    vector_db = BJJVectorDB()
    
    if not vector_db.model:
        print("❌ Failed to initialize vector database")
        return False
    
    # Test search functionality
    print("🔍 Testing search functionality...")
    
    # Test 1: Search by injury
    injuries = ["ACL reconstruction", "knee pain"]
    results = vector_db.search_by_injuries(injuries, top_k=3)
    
    if results:
        print(f"✅ Found {len(results)} similar techniques for injuries: {injuries}")
        for i, result in enumerate(results):
            technique = result['metadata']['technique']
            score = result['score']
            print(f"  {i+1}. {technique} (similarity: {score:.3f})")
    else:
        print("❌ No results found")
        return False
    
    # Test 2: Search by technique name
    print("\n🔍 Testing technique search...")
    technique_results = vector_db.search_similar_techniques("armbar submission", top_k=3)
    
    if technique_results:
        print(f"✅ Found {len(technique_results)} similar techniques for 'armbar submission'")
        for i, result in enumerate(technique_results):
            technique = result['metadata']['technique']
            score = result['score']
            print(f"  {i+1}. {technique} (similarity: {score:.3f})")
    else:
        print("❌ No technique results found")
        return False
    
    # Test 3: Get stats
    print("\n📊 Database statistics:")
    stats = vector_db.get_technique_stats()
    print(f"  Total vectors: {stats['total_vectors']}")
    print(f"  Dimension: {stats['dimension']}")
    print(f"  Index fullness: {stats['index_fullness']:.2%}")
    
    print("\n✅ All tests passed! Vector database is working correctly.")
    return True

if __name__ == "__main__":
    test_vector_db()
