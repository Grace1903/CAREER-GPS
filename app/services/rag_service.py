# import os
# import json
# import gc
# import time
# from typing import List, Dict, Any, Optional

# try:
#     import google.generativeai as genai
#     GENAI_AVAILABLE = True
# except ImportError:
#     GENAI_AVAILABLE = False
#     print("google-generativeai not available")

# CHROMA_AVAILABLE = False
# try:
#     import chromadb
#     CHROMA_AVAILABLE = True
# except ImportError:
#     print("ChromaDB not available - using basic matching")

# EMBEDDINGS_AVAILABLE = False
# try:
#     from sentence_transformers import SentenceTransformer
#     EMBEDDINGS_AVAILABLE = True
# except ImportError:
#     print("Sentence Transformers not available")


# class HuggingFaceEmbeddings:
    
#     def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
#         self.model = None
#         self.model_name = model_name
        
#         if EMBEDDINGS_AVAILABLE:
#             try:
#                 print(f"Loading embedding model: {model_name}")
#                 self.model = SentenceTransformer(model_name)
#                 print("Embedding model loaded successfully")
#             except Exception as e:
#                 print(f"Failed to load embedding model: {e}")
    
#     def embed_documents(self, texts: List[str]) -> List[List[float]]:
#         if self.model:
#             try:
#                 embeddings = self.model.encode(texts, show_progress_bar=False)
#                 return embeddings.tolist()
#             except Exception as e:
#                 print(f"Embedding error: {e}")
#         return [[0.0] * 384 for _ in texts]
    
#     def embed_query(self, text: str) -> List[float]:
#         if self.model:
#             try:
#                 embedding = self.model.encode([text], show_progress_bar=False)[0]
#                 return embedding.tolist()
#             except Exception as e:
#                 print(f"Query embedding error: {e}")
#         return [0.0] * 384
    
#     def __call__(self, texts: List[str]) -> List[List[float]]:
#         return self.embed_documents(texts)


# class RAGService:
    
#     def __init__(self):
#         self.gemini_model = None
#         self.embeddings = None
#         self.chroma_client = None
#         self.collection = None
#         self.persist_directory = os.path.join(
#             os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
#             'vector_store'
#         )
#         self.is_initialized = False
#         self._collection_name = "job_skills"
        
#         self._initialize_components()
    
#     def _initialize_components(self):
#         api_key = os.environ.get('GEMINI_API_KEY', '')
        
#         if api_key and GENAI_AVAILABLE:
#             try:
#                 genai.configure(api_key=api_key)
#                 self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
#                 print("Gemini model initialized")
#             except Exception as e:
#                 print(f"Gemini initialization failed: {e}")
#         else:
#             print("GEMINI_API_KEY not set or google-generativeai not available")
        
#         if EMBEDDINGS_AVAILABLE:
#             try:
#                 self.embeddings = HuggingFaceEmbeddings('all-MiniLM-L6-v2')
#                 if self.embeddings.model:
#                     print("HuggingFace embeddings initialized")
#                 else:
#                     print("HuggingFace embeddings failed to load model")
#                     self.embeddings = None
#             except Exception as e:
#                 print(f"Embeddings initialization failed: {e}")
#                 self.embeddings = None
        
#         if CHROMA_AVAILABLE and self.embeddings and self.embeddings.model:
#             self._initialize_chroma()
        
#         self.is_initialized = bool(self.gemini_model)
    
#     def _initialize_chroma(self):
#         try:
#             os.makedirs(self.persist_directory, exist_ok=True)
            
#             self.chroma_client = chromadb.PersistentClient(
#                 path=self.persist_directory
#             )
            
#             self.collection = self.chroma_client.get_or_create_collection(
#                 name=self._collection_name,
#                 metadata={"hnsw:space": "cosine"},
#                 embedding_function=self.embeddings
#             )
            
#             doc_count = self.collection.count()
#             print(f"ChromaDB initialized (collection has {doc_count} documents)")
            
#         except Exception as e:
#             print(f"ChromaDB initialization failed: {e}")
#             import traceback
#             traceback.print_exc()
#             self.collection = None
    
#     @property
#     def llm(self):
#         return self.gemini_model
    
#     def add_job_role_documents(self, job_roles: List[Dict]) -> bool:
#         if not self.collection:
#             print("Vector store not available")
#             return False
        
#         if not self.embeddings or not self.embeddings.model:
#             print("Embeddings not available")
#             return False
        
#         try:
#             documents = []
#             metadatas = []
#             ids = []
            
#             doc_id = 0
#             timestamp = int(time.time())
            
#             for job in job_roles:
#                 title = job.get('title', '')
#                 industry = job.get('industry', 'Technology')
#                 required_skills = job.get('required_skills', [])
#                 preferred_skills = job.get('preferred_skills', [])
#                 description = job.get('description', '')
                
#                 for skill in required_skills:
#                     doc_text = self._create_skill_text(
#                         skill, title, industry, "required",
#                         description, required_skills + preferred_skills
#                     )
#                     documents.append(doc_text)
#                     metadatas.append({
#                         "type": "skill",
#                         "skill_name": skill,
#                         "skill_type": "required",
#                         "job_title": title,
#                         "industry": industry
#                     })
#                     ids.append(f"req_{timestamp}_{doc_id}")
#                     doc_id += 1
                
#                 for skill in preferred_skills:
#                     doc_text = self._create_skill_text(
#                         skill, title, industry, "preferred",
#                         description, required_skills + preferred_skills
#                     )
#                     documents.append(doc_text)
#                     metadatas.append({
#                         "type": "skill",
#                         "skill_name": skill,
#                         "skill_type": "preferred",
#                         "job_title": title,
#                         "industry": industry
#                     })
#                     ids.append(f"pref_{timestamp}_{doc_id}")
#                     doc_id += 1
                
#                 job_doc = f"""
#                 Job Role: {title}
#                 Industry: {industry}
#                 Description: {description}
#                 Required Skills: {', '.join(required_skills)}
#                 Preferred Skills: {', '.join(preferred_skills)}
#                 This role requires expertise in {', '.join(required_skills[:3])}.
#                 """
#                 documents.append(job_doc)
#                 metadatas.append({
#                     "type": "job_role",
#                     "job_title": title,
#                     "industry": industry
#                 })
#                 ids.append(f"job_{timestamp}_{doc_id}")
#                 doc_id += 1
            
#             batch_size = 50
#             total_added = 0
            
#             for i in range(0, len(documents), batch_size):
#                 batch_docs = documents[i:i+batch_size]
#                 batch_metas = metadatas[i:i+batch_size]
#                 batch_ids = ids[i:i+batch_size]
                
#                 try:
#                     self.collection.add(
#                         documents=batch_docs,
#                         metadatas=batch_metas,
#                         ids=batch_ids
#                     )
#                     total_added += len(batch_docs)
#                 except Exception as batch_error:
#                     print(f"Batch add error: {batch_error}")
#                     for j, (doc, meta, id_) in enumerate(zip(batch_docs, batch_metas, batch_ids)):
#                         try:
#                             self.collection.add(
#                                 documents=[doc],
#                                 metadatas=[meta],
#                                 ids=[id_]
#                             )
#                             total_added += 1
#                         except Exception as single_error:
#                             print(f"Single add error for {id_}: {single_error}")
            
#             print(f"Added {total_added} documents to vector store")
#             return total_added > 0
            
#         except Exception as e:
#             print(f"Error adding documents: {e}")
#             import traceback
#             traceback.print_exc()
#             return False
    
#     def _create_skill_text(self, skill: str, job_title: str, industry: str,
#                            skill_type: str, description: str, 
#                            related_skills: List[str]) -> str:
#         context = self._get_skill_context(skill)
#         related = [s for s in related_skills if s.lower() != skill.lower()][:5]
        
#         return f"""
#         Skill: {skill}
#         Type: {skill_type} for {job_title}
#         Industry: {industry}
#         Context: {context}
#         Related: {', '.join(related)}
#         Description: {description[:150] if description else 'Technology role'}
#         """
    
#     def _get_skill_context(self, skill: str) -> str:
#         contexts = {
#             "python": "Python - versatile language for web, data science, ML, automation",
#             "java": "Java - object-oriented language for enterprise and Android",
#             "javascript": "JavaScript - essential for web development and Node.js",
#             "typescript": "TypeScript - typed superset of JavaScript",
#             "sql": "SQL - database querying and management language",
#             "machine learning": "Machine Learning - systems that learn from data",
#             "deep learning": "Deep Learning - neural networks for complex patterns",
#             "aws": "AWS - Amazon cloud platform for scalable applications",
#             "azure": "Azure - Microsoft cloud computing platform",
#             "gcp": "GCP - Google Cloud Platform services",
#             "docker": "Docker - containerization for consistent deployment",
#             "kubernetes": "Kubernetes - container orchestration platform",
#             "react": "React - JavaScript library for user interfaces",
#             "angular": "Angular - TypeScript framework for web apps",
#             "vue": "Vue.js - progressive JavaScript framework",
#             "node.js": "Node.js - JavaScript runtime for servers",
#             "tensorflow": "TensorFlow - ML framework for neural networks",
#             "pytorch": "PyTorch - deep learning with dynamic graphs",
#             "pandas": "Pandas - Python data manipulation library",
#             "numpy": "NumPy - numerical computing in Python",
#             "git": "Git - version control system",
#             "linux": "Linux - operating system for servers",
#             "mongodb": "MongoDB - NoSQL document database",
#             "postgresql": "PostgreSQL - relational database system",
#             "redis": "Redis - in-memory data structure store",
#             "graphql": "GraphQL - API query language",
#             "rest api": "REST API - architectural style for web services",
#             "ci/cd": "CI/CD - continuous integration and deployment",
#             "jenkins": "Jenkins - automation server for CI/CD",
#             "terraform": "Terraform - infrastructure as code tool",
#             "nlp": "NLP - natural language processing",
#             "computer vision": "Computer Vision - image and video analysis",
#             "data visualization": "Data Visualization - presenting data graphically",
#             "statistical analysis": "Statistical Analysis - analyzing data patterns",
#         }
        
#         skill_lower = skill.lower()
#         for key, context in contexts.items():
#             if key in skill_lower or skill_lower in key:
#                 return context
        
#         return f"{skill} - professional technology skill"
    
#     def semantic_skill_match(self, extracted_skill: str, job_role: str) -> Dict[str, Any]:
#         """Match skill semantically"""
        
#         # Try vector search + Gemini
#         if self.collection and self.collection.count() > 0 and self.gemini_model:
#             try:
#                 return self._vector_match(extracted_skill, job_role)
#             except Exception as e:
#                 print(f"Vector match failed: {e}")
        
#         # Try Gemini only
#         if self.gemini_model:
#             try:
#                 return self._gemini_match(extracted_skill, job_role)
#             except Exception as e:
#                 print(f"Gemini match failed: {e}")
        
#         return self._basic_match(extracted_skill, job_role)
    
#     def _vector_match(self, extracted_skill: str, job_role: str) -> Dict[str, Any]:
#         """Match using vector similarity + Gemini"""
        
#         query = f"Skill similar to {extracted_skill} for {job_role}"
        
#         # Query vector store
#         try:
#             results = self.collection.query(
#                 query_texts=[query],
#                 n_results=10,
#                 where={"job_title": job_role}
#             )
#         except Exception:
#             # Try without job filter
#             results = self.collection.query(
#                 query_texts=[query],
#                 n_results=10
#             )
        
#         if not results['documents'] or not results['documents'][0]:
#             # Try without job filter
#             try:
#                 results = self.collection.query(
#                     query_texts=[query],
#                     n_results=10
#                 )
#             except Exception as e:
#                 print(f"Query error: {e}")
#                 return self._gemini_match(extracted_skill, job_role)
        
#         if results['documents'] and results['documents'][0]:
#             context = "\n".join(results['documents'][0][:5])
#             return self._analyze_match(extracted_skill, job_role, context)
        
#         return self._gemini_match(extracted_skill, job_role)
    
#     def _analyze_match(self, extracted_skill: str, job_role: str, context: str) -> Dict[str, Any]:
#         """Analyze match using Gemini with context"""
        
#         prompt = f"""
#         Context about {job_role} skills:
#         {context[:2000]}
        
#         Does "{extracted_skill}" match any skill above?
        
#         Consider abbreviations: ML=Machine Learning, JS=JavaScript, TS=TypeScript, K8s=Kubernetes, DL=Deep Learning, AI=Artificial Intelligence, NLP=Natural Language Processing, CV=Computer Vision, AWS=Amazon Web Services, GCP=Google Cloud Platform, DB=Database
        
#         Return ONLY valid JSON:
#         {{"is_match": true, "match_type": "exact", "matched_skill": "Machine Learning", "similarity_score": 0.95, "explanation": "ML is abbreviation for Machine Learning"}}
        
#         Or if no match:
#         {{"is_match": false, "match_type": "none", "matched_skill": null, "similarity_score": 0.0, "explanation": "No related skill found"}}
#         """
        
#         try:
#             response = self.gemini_model.generate_content(prompt)
#             text = response.text.strip()
            
#             # Extract JSON
#             import re
#             json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
#             if json_match:
#                 result = json.loads(json_match.group())
#                 result['extracted_skill'] = extracted_skill
#                 return result
#         except Exception as e:
#             print(f"Match analysis error: {e}")
        
#         return self._basic_match(extracted_skill, job_role)
    
#     def _gemini_match(self, extracted_skill: str, job_role: str) -> Dict[str, Any]:
#         """Match using Gemini only"""
        
#         prompt = f"""
#         For a "{job_role}" role, does the skill "{extracted_skill}" match any typically required skill?
        
#         Common abbreviations:
#         - ML = Machine Learning
#         - DL = Deep Learning  
#         - AI = Artificial Intelligence
#         - JS = JavaScript
#         - TS = TypeScript
#         - K8s = Kubernetes
#         - AWS = Amazon Web Services
#         - GCP = Google Cloud Platform
#         - NLP = Natural Language Processing
#         - CV = Computer Vision
#         - DB = Database
#         - API = Application Programming Interface
#         - CI/CD = Continuous Integration/Deployment
        
#         Return ONLY valid JSON (no markdown, no explanation):
#         {{"is_match": true/false, "match_type": "exact/semantic/related/none", "matched_skill": "skill name or null", "similarity_score": 0.0-1.0, "explanation": "brief reason"}}
#         """
        
#         try:
#             response = self.gemini_model.generate_content(prompt)
#             text = response.text.strip()
            
#             import re
#             # Remove markdown code blocks if present
#             text = re.sub(r'```json\s*', '', text)
#             text = re.sub(r'```\s*', '', text)
            
#             json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
#             if json_match:
#                 result = json.loads(json_match.group())
#                 result['extracted_skill'] = extracted_skill
#                 return result
#         except Exception as e:
#             print(f"Gemini match error: {e}")
        
#         return self._basic_match(extracted_skill, job_role)
    
#     def _basic_match(self, extracted_skill: str, job_role: str) -> Dict[str, Any]:
#         """Basic fallback matching"""
#         return {
#             "extracted_skill": extracted_skill,
#             "is_match": False,
#             "match_type": "none",
#             "matched_skill": None,
#             "similarity_score": 0.0,
#             "explanation": "Fallback - no semantic match available"
#         }
    
#     def analyze_skill_gaps_with_rag(self, extracted_skills: List[str],
#                                      job_role_data: Dict) -> Dict[str, Any]:
#         """Comprehensive skill gap analysis"""
        
#         job_title = job_role_data.get('title', 'Unknown')
#         required_skills = job_role_data.get('required_skills', [])
#         preferred_skills = job_role_data.get('preferred_skills', [])
        
#         if isinstance(required_skills, str):
#             required_skills = json.loads(required_skills)
#         if isinstance(preferred_skills, str):
#             preferred_skills = json.loads(preferred_skills)
        
#         # Match each extracted skill
#         matched_skills = []
#         matched_with_names = set()
        
#         for skill in extracted_skills:
#             match_result = self.semantic_skill_match(skill, job_title)
            
#             if match_result.get('is_match') and match_result.get('similarity_score', 0) >= 0.5:
#                 matched_skills.append({
#                     'extracted': skill,
#                     'matched_with': match_result.get('matched_skill'),
#                     'match_type': match_result.get('match_type'),
#                     'similarity': match_result.get('similarity_score')
#                 })
#                 if match_result.get('matched_skill'):
#                     matched_with_names.add(match_result['matched_skill'].lower())
        
#         # Also add direct matches (case insensitive)
#         extracted_lower = {s.lower() for s in extracted_skills}
#         for skill in required_skills + preferred_skills:
#             if skill.lower() in extracted_lower:
#                 matched_with_names.add(skill.lower())
        
#         # Find missing skills
#         missing_required = []
#         for skill in required_skills:
#             skill_lower = skill.lower()
#             is_matched = (
#                 skill_lower in matched_with_names or
#                 skill_lower in extracted_lower or
#                 any(skill_lower in m or m in skill_lower for m in matched_with_names) or
#                 any(skill_lower in e or e in skill_lower for e in extracted_lower)
#             )
#             if not is_matched:
#                 missing_required.append(skill)
        
#         missing_preferred = []
#         for skill in preferred_skills:
#             skill_lower = skill.lower()
#             is_matched = (
#                 skill_lower in matched_with_names or
#                 skill_lower in extracted_lower or
#                 any(skill_lower in m or m in skill_lower for m in matched_with_names) or
#                 any(skill_lower in e or e in skill_lower for e in extracted_lower)
#             )
#             if not is_matched:
#                 missing_preferred.append(skill)
        
#         # Calculate match percentage
#         total_required = len(required_skills)
#         matched_required = total_required - len(missing_required)
#         match_percentage = (matched_required / total_required * 100) if total_required > 0 else 0
        
#         # Get priorities
#         priority_skills = self._get_priority_skills(
#             missing_required, missing_preferred, job_role_data
#         )
        
#         return {
#             'matched_skills': [m['extracted'] for m in matched_skills] + 
#                              [s for s in extracted_skills if s.lower() in matched_with_names],
#             'semantic_matches': matched_skills,
#             'missing_skills': missing_required + missing_preferred,
#             'missing_required': missing_required,
#             'missing_preferred': missing_preferred,
#             'match_percentage': round(match_percentage, 1),
#             'priority_skills': priority_skills,
#             'total_required': total_required,
#             'matched_count': matched_required,
#             'analysis_method': 'rag_semantic' if (self.collection and self.collection.count() > 0) else 'gemini_direct'
#         }
    
#     def _get_priority_skills(self, missing_required: List[str],
#                               missing_preferred: List[str],
#                               job_role_data: Dict) -> List[Dict]:
        
#         if not self.gemini_model:
#             return self._basic_priorities(missing_required, missing_preferred)
        
#         try:
#             job_title = job_role_data.get('title', 'Unknown')
            
#             prompt = f"""
#             For {job_title}, prioritize these missing skills for learning:
            
#             Required (must have): {', '.join(missing_required[:8])}
#             Preferred (nice to have): {', '.join(missing_preferred[:5])}
            
#             Return JSON array of top 8 skills to learn, ordered by importance:
#             [
#                 {{"skill": "Python", "priority": "critical", "reason": "Foundation for ML", "estimated_learning_weeks": 6}},
#                 {{"skill": "SQL", "priority": "high", "reason": "Essential for data work", "estimated_learning_weeks": 3}}
#             ]
            
#             Priority levels: critical, high, medium, low
            
#             Return ONLY the JSON array, no other text.
#             """
            
#             response = self.gemini_model.generate_content(prompt)
#             text = response.text.strip()
            
#             import re
#             text = re.sub(r'```json\s*', '', text)
#             text = re.sub(r'```\s*', '', text)
            
#             json_match = re.search(r'\[.*\]', text, re.DOTALL)
#             if json_match:
#                 priorities = json.loads(json_match.group())
#                 if isinstance(priorities, list) and len(priorities) > 0:
#                     return priorities
                    
#         except Exception as e:
#             print(f"Priority generation error: {e}")
        
#         return self._basic_priorities(missing_required, missing_preferred)
    
#     def _basic_priorities(self, missing_required: List[str],
#                           missing_preferred: List[str]) -> List[Dict]:
#         priorities = []
        
#         for i, skill in enumerate(missing_required[:5]):
#             priorities.append({
#                 'skill': skill,
#                 'priority': 'critical' if i < 2 else 'high',
#                 'reason': 'Required skill for this role',
#                 'estimated_learning_weeks': 4
#             })
        
#         for skill in missing_preferred[:3]:
#             priorities.append({
#                 'skill': skill,
#                 'priority': 'medium',
#                 'reason': 'Preferred skill to enhance candidacy',
#                 'estimated_learning_weeks': 3
#             })
        
#         return priorities
    
#     def clear_vector_store(self) -> bool:
        
#         try:
#             if self.collection:
#                 try:
#                     count = self.collection.count()
#                     if count > 0:
#                         all_data = self.collection.get()
#                         if all_data and all_data.get('ids'):
#                             self.collection.delete(ids=all_data['ids'])
#                             print(f"✓ Deleted {len(all_data['ids'])} documents from collection")
#                     else:
#                         print("✓ Collection is already empty")
#                     return True
#                 except Exception as e:
#                     print(f"Error clearing documents: {e}")
#                     return self._recreate_collection()
            
#             if CHROMA_AVAILABLE and self.embeddings and self.embeddings.model:
#                 self._initialize_chroma()
#                 return True
            
#             return False
            
#         except Exception as e:
#             print(f"Error clearing vector store: {e}")
#             import traceback
#             traceback.print_exc()
#             return False
    
#     def _recreate_collection(self) -> bool:
#         try:
#             if self.chroma_client:
#                 # Delete collection
#                 try:
#                     self.chroma_client.delete_collection(self._collection_name)
#                     print("✓ Deleted collection")
#                 except Exception:
#                     pass
                
#                 # Create new collection
#                 self.collection = self.chroma_client.create_collection(
#                     name=self._collection_name,
#                     metadata={"hnsw:space": "cosine"},
#                     embedding_function=self.embeddings
#                 )
#                 print("✓ Created new collection")
#                 return True
#         except Exception as e:
#             print(f"Error recreating collection: {e}")
#         return False
    
#     def reset_vector_store(self) -> bool:
#         try:
#             self.collection = None
#             self.chroma_client = None
            
#             gc.collect()
#             time.sleep(0.5)
            
#             if CHROMA_AVAILABLE and self.embeddings and self.embeddings.model:
#                 self._initialize_chroma()
#                 return True
            
#             return False
            
#         except Exception as e:
#             print(f"Error resetting vector store: {e}")
#             return False


# _rag_service = None

# def get_rag_service() -> RAGService:
#     global _rag_service
#     if _rag_service is None:
#         _rag_service = RAGService()
#     return _rag_service


# def reset_rag_service():
#     global _rag_service
#     if _rag_service:
#         _rag_service.reset_vector_store()
#     _rag_service = None


import os
import json
from typing import List, Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
os.environ["TOKENIZERS_PARALLELISM"] = "false"
api_key = 'AIzaSyAf9qLthKYZMqBVAd4fVz4B4iKv1CNJuBI'
class RAGService:

    def __init__(self):

        self.persist_directory = "vector_store"
        os.makedirs(self.persist_directory, exist_ok=True)

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.environ.get(api_key),
            temperature=0.2
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
        )

        # self.vector_store = Chroma(
        #     persist_directory=self.persist_directory,
        #     embedding_function=self.embeddings
        # )
        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name="job_skills"
        )

        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})

        self.prompt = PromptTemplate(
            template="""
You are a skill matching assistant.

Context:
{context}

Question:
Does the skill "{skill}" match skills required for "{job_role}"?

Return ONLY JSON:
{{"is_match": true/false,
"match_type": "exact/semantic/related/none",
"matched_skill": "skill name or null",
"similarity_score": 0.0-1.0,
"explanation": "short reason"}}
""",
            input_variables=["context", "skill", "job_role"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.retriever,
            chain_type="stuff",
            return_source_documents=True
        )


    def add_job_role_documents(self, job_roles: List[Dict]):

        documents = []

        for job in job_roles:

            title = job.get("title", "")
            industry = job.get("industry", "")
            required_skills = job.get("required_skills", [])
            preferred_skills = job.get("preferred_skills", [])

            doc = f"""
Job Role: {title}
Industry: {industry}

Required Skills:
{", ".join(required_skills)}

Preferred Skills:
{", ".join(preferred_skills)}
"""

            documents.append(doc)

        self.vector_store.add_texts(documents)
        self.vector_store.persist()


    def semantic_skill_match(self, skill: str, job_role: str):

        query = f"skills required for {job_role}"

        docs = self.retriever.get_relevant_documents(query)

        context = "\n".join([d.page_content for d in docs])

        prompt = self.prompt.format(
            context=context,
            skill=skill,
            job_role=job_role
        )

        response = self.llm.invoke(prompt)

        try:
            return json.loads(response.content)
        except:
            return {
                "is_match": False,
                "match_type": "none",
                "matched_skill": None,
                "similarity_score": 0,
                "explanation": "JSON parse failed"
            }


    def analyze_skill_gaps(self,
                           extracted_skills: List[str],
                           job_role_data: Dict):

        required_skills = job_role_data.get("required_skills", [])
        preferred_skills = job_role_data.get("preferred_skills", [])

        matched = []

        for skill in extracted_skills:

            result = self.semantic_skill_match(
                skill,
                job_role_data.get("title")
            )

            if result["is_match"]:
                matched.append(skill)

        missing_required = [
            s for s in required_skills
            if s.lower() not in [m.lower() for m in matched]
        ]

        missing_preferred = [
            s for s in preferred_skills
            if s.lower() not in [m.lower() for m in matched]
        ]

        return {
            "matched_skills": matched,
            "missing_required": missing_required,
            "missing_preferred": missing_preferred
        }


_rag_service = None


def get_rag_service():

    global _rag_service

    if _rag_service is None:
        _rag_service = RAGService()

    return _rag_service