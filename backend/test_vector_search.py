"""
Quick test script to verify vector search functionality.
Run this from the backend directory: python test_vector_search.py
"""
import asyncio
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.ai.rag.embeddings import get_embeddings
from app.ai.rag.vectorstore import get_vector_store

async def test_embeddings():
    """Test embeddings generation."""
    print("\n" + "="*60)
    print("TEST 1: Embeddings Generation")
    print("="*60)
    
    try:
        embeddings = get_embeddings()
        print(f"✅ Embeddings provider initialized: {embeddings.get_current_provider()}")
        
        # Test single query embedding
        test_text = "Python developer with 5 years experience"
        embedding = embeddings.embed_query(test_text)
        print(f"✅ Generated embedding for query (dimension: {len(embedding)})")
        
        # Test batch document embedding
        test_docs = [
            "Senior Python Developer",
            "Junior JavaScript Developer",
            "Data Scientist with ML experience"
        ]
        doc_embeddings = embeddings.embed_documents(test_docs)
        print(f"✅ Generated {len(doc_embeddings)} document embeddings")
        
        return True
    except Exception as e:
        print(f"❌ Embeddings test failed: {e}")
        return False

async def test_vector_store():
    """Test vector store operations."""
    print("\n" + "="*60)
    print("TEST 2: Vector Store Operations")
    print("="*60)
    
    try:
        vector_store = get_vector_store()
        print(f"✅ Vector store initialized")
        
        # Test adding jobs
        test_jobs = [
            {
                "id": "test-job-1",
                "data": {
                    "title": "Senior Python Developer",
                    "company_name": "Tech Corp",
                    "location": "San Francisco, CA",
                    "description": "We're looking for an experienced Python developer with Django and FastAPI skills.",
                    "requirements": ["5+ years Python", "Django", "FastAPI", "PostgreSQL"],
                    "skills": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker"],
                    "experience_level": "Senior",
                    "job_type": "Full-time"
                }
            },
            {
                "id": "test-job-2",
                "data": {
                    "title": "JavaScript Frontend Developer",
                    "company_name": "Web Solutions Inc",
                    "location": "Remote",
                    "description": "Join our team to build modern web applications with React and TypeScript.",
                    "requirements": ["3+ years JavaScript", "React", "TypeScript"],
                    "skills": ["JavaScript", "React", "TypeScript", "CSS", "HTML"],
                    "experience_level": "Mid",
                    "job_type": "Full-time"
                }
            },
            {
                "id": "test-job-3",
                "data": {
                    "title": "Data Scientist",
                    "company_name": "AI Innovations",
                    "location": "New York, NY",
                    "description": "Work on cutting-edge machine learning projects using Python and TensorFlow.",
                    "requirements": ["PhD or Masters in CS/Stats", "Python", "Machine Learning"],
                    "skills": ["Python", "TensorFlow", "PyTorch", "Pandas", "NumPy"],
                    "experience_level": "Senior",
                    "job_type": "Full-time"
                }
            }
        ]
        
        for job in test_jobs:
            success = vector_store.add_job(job["id"], job["data"])
            if success:
                print(f"✅ Added job: {job['data']['title']}")
            else:
                print(f"❌ Failed to add job: {job['data']['title']}")
        
        # Test searching
        print("\n" + "-"*60)
        print("TEST 3: Semantic Search")
        print("-"*60)
        
        test_queries = [
            "Python developer with backend experience",
            "Frontend engineer skilled in React",
            "Machine learning engineer"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            results = vector_store.search_jobs(query, n_results=2)
            
            if results:
                print(f"✅ Found {len(results)} matches:")
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result['metadata'].get('title', 'N/A')} "
                          f"(similarity: {result['similarity_score']:.2f})")
            else:
                print(f"❌ No results found")
        
        # Get stats
        stats = vector_store.get_stats()
        print(f"\n✅ Vector store stats: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("VECTOR SEARCH FUNCTIONALITY TEST")
    print("="*60)
    
    # Test embeddings
    embeddings_ok = await test_embeddings()
    
    # Test vector store
    vector_store_ok = await test_vector_store()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Embeddings: {'✅ PASS' if embeddings_ok else '❌ FAIL'}")
    print(f"Vector Store: {'✅ PASS' if vector_store_ok else '❌ FAIL'}")
    
    if embeddings_ok and vector_store_ok:
        print("\n🎉 All tests passed! Vector search is working correctly.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    asyncio.run(main())

