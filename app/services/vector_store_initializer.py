import json
from typing import List, Dict


def initialize_vector_store() -> bool:
    try:
        from flask import current_app
        from app import db
        from app.models import JobRole
        from app.services.rag_service import get_rag_service
        
        with current_app.app_context():
            job_roles = JobRole.query.all()
            
            if not job_roles:
                print("No job roles found in database")
                return False
            
            job_role_data = []
            for job in job_roles:
                job_dict = {
                    'title': job.title,
                    'industry': job.industry,
                    'required_skills': json.loads(job.required_skills) if job.required_skills else [],
                    'preferred_skills': json.loads(job.preferred_skills) if job.preferred_skills else [],
                    'description': job.description or '',
                }
                job_role_data.append(job_dict)
            
            rag_service = get_rag_service()
            
            if not rag_service.embeddings or not rag_service.embeddings.model:
                print("Embeddings not available - RAG will use Gemini-only mode")
                return True
            
            if not rag_service.collection:
                print("ChromaDB collection not available - RAG will use Gemini-only mode")
                return True
            
            print("Clearing existing documents...")
            rag_service.clear_vector_store()
            
            print(f"Adding {len(job_role_data)} job roles to vector store...")
            success = rag_service.add_job_role_documents(job_role_data)
            
            if success:
                doc_count = rag_service.collection.count() if rag_service.collection else 0
                print(f"✓ Vector store initialized ({doc_count} documents)")
                return True
            else:
                print("✗ Failed to add documents, but app will work with Gemini-only mode")
                return True  # Return True to not block app startup
                
    except Exception as e:
        print(f"Error initializing vector store: {e}")
        import traceback
        traceback.print_exc()
        return True


def refresh_vector_store() -> bool:
    return initialize_vector_store()