import os
import json
import re
from app.models import SkillTaxonomy


class SkillExtractor:
    
    def __init__(self):
        self.gemini_model = None
        self._init_gemini()
        self._load_default_taxonomy()
    
    def _init_gemini(self):
        try:
            import google.generativeai as genai
            api_key = 'AIzaSyAf9qLthKYZMqBVAd4fVz4B4iKv1CNJuBI'
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
            self.gemini_model = None
    
    def _load_default_taxonomy(self):
        self.skill_taxonomy = {
            "programming_languages": [
                {"name": "Python", "aliases": ["python", "py"]},
                {"name": "SQL", "aliases": ["sql", "mysql"]},
                {"name": "C", "aliases": ["c"]},
                {"name": "HTML", "aliases": ["html"]},
                {"name": "Java", "aliases": ["java"]},
                {"name": "JavaScript", "aliases": ["javascript", "js"]},
            ],
            "data_science": [
                {"name": "Machine Learning", "aliases": ["machine learning", "ml"]},
                {"name": "NLP", "aliases": ["nlp", "natural language processing"]},
                {"name": "Data Analysis", "aliases": ["data analysis", "analytics"]},
                {"name": "Data Visualization", "aliases": ["data visualization"]},
            ],
            "tools": [
                {"name": "Flask", "aliases": ["flask"]},
                {"name": "Git", "aliases": ["git"]},
                {"name": "Excel", "aliases": ["excel"]},
            ],
            "soft_skills": [
                {"name": "Analytical Thinking", "aliases": ["analytical thinking"]},
                {"name": "Problem Solving", "aliases": ["problem solving"]},
                {"name": "Teamwork", "aliases": ["teamwork"]},
                {"name": "Communication", "aliases": ["communication"]},
            ]
        }
    
    def extract_skills(self, processed_text, raw_text=None):
        text = raw_text if raw_text else processed_text
        
        if not text:
            return {'all_skills': [], 'technical_skills': [], 'soft_skills': []}
        
        all_skills = set()
        technical_skills = set()
        soft_skills = set()
        
        text_lower = text.lower()
        
        for category, skills in self.skill_taxonomy.items():
            for skill_data in skills:
                skill_name = skill_data['name']
                aliases = skill_data.get('aliases', [])
                
                for term in [skill_name.lower()] + [a.lower() for a in aliases]:
                    if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                        all_skills.add(skill_name)
                        if category == 'soft_skills':
                            soft_skills.add(skill_name)
                        else:
                            technical_skills.add(skill_name)
                        break
        
        return {
            'all_skills': list(all_skills),
            'technical_skills': list(technical_skills),
            'soft_skills': list(soft_skills),
            'extraction_methods': ['taxonomy']
        }
    
    def _extract_with_taxonomy(self, text):
        found_skills = {'all': set(), 'technical': set(), 'soft': set()}
        text_lower = text.lower()
        
        for category, skills in self.skill_taxonomy.items():
            for skill_data in skills:
                skill_name = skill_data['name']
                aliases = skill_data.get('aliases', [])
                
                for term in [skill_name.lower()] + [a.lower() for a in aliases]:
                    if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
                        found_skills['all'].add(skill_name)
                        if category == 'soft_skills':
                            found_skills['soft'].add(skill_name)
                        else:
                            found_skills['technical'].add(skill_name)
                        break
        
        return found_skills
    
    def _extract_with_gemini(self, text):
        return {'technical': [], 'soft': []}