"""
Skill Gap Analysis Service - RAG Enhanced Version
Compare extracted skills with job requirements using semantic matching
"""
import os
import json
import re
from typing import List, Dict, Any


class SkillGapAnalyzer:
    """
    Analyze skill gaps using RAG-based semantic matching
    Falls back to basic matching if RAG is not available
    """
    
    def __init__(self):
        self.rag_service = None
        self.gemini_model = None
        self._init_services()
    
    def _init_services(self):
        """Initialize RAG and Gemini services"""
        # Try to initialize RAG service
        try:
            from app.services.rag_service import get_rag_service
            self.rag_service = get_rag_service()
        except Exception as e:
            print(f"RAG service initialization failed: {e}")
            self.rag_service = None
        
        # Initialize direct Gemini as backup
        try:
            import google.generativeai as genai
            api_key = os.environ.get('GEMINI_API_KEY', '')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            print(f"Gemini initialization failed: {e}")
            self.gemini_model = None
    
    def analyze(self, extracted_skills: List[str], job_role_data: Dict) -> Dict[str, Any]:
        """
        Analyze skill gaps using RAG-based semantic matching
        
        Args:
            extracted_skills: List of skills extracted from resume
            job_role_data: Dictionary containing job role requirements
            
        Returns:
            Dictionary containing match results, gaps, and recommendations
        """
        # Try RAG-based analysis first
        if self.rag_service and (self.rag_service.llm or self.rag_service.gemini_model):
            try:
                result = self.rag_service.analyze_skill_gaps_with_rag(
                    extracted_skills, 
                    job_role_data
                )
                
                # Enhance with additional analysis
                if self.gemini_model and result.get('missing_skills'):
                    result = self._enhance_with_gemini(result, job_role_data)
                
                return result
                
            except Exception as e:
                print(f"RAG analysis failed: {e}")
        
        # Fallback to basic analysis
        return self._basic_skill_gap_analysis(extracted_skills, job_role_data)
    
    def _enhance_with_gemini(self, result: Dict, job_role_data: Dict) -> Dict:
        """Enhance results with additional Gemini analysis"""
        try:
            missing_skills = result.get('missing_skills', [])[:10]
            job_title = job_role_data.get('title', 'Unknown')
            
            prompt = f"""
            Analyze skill gap for {job_title} role.
            
            Missing Skills: {', '.join(missing_skills)}
            Current Match: {result.get('match_percentage', 0)}%
            
            Provide brief JSON insights:
            {{
                "foundational_skills": ["top 3 skills to learn first"],
                "estimated_readiness_weeks": number,
                "overall_assessment": "one sentence assessment"
            }}
            
            Return ONLY the JSON.
            """
            
            response = self.gemini_model.generate_content(prompt)
            response_text = response.text
            
            json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                result['ai_insights'] = json.loads(json_match.group())
            
        except Exception as e:
            print(f"Gemini enhancement failed: {e}")
        
        return result
    
    def _basic_skill_gap_analysis(self, extracted_skills: List[str], 
                                   job_role_data: Dict) -> Dict[str, Any]:
        """
        Basic skill gap analysis using fuzzy string matching
        """
        required_skills = job_role_data.get('required_skills', [])
        preferred_skills = job_role_data.get('preferred_skills', [])
        
        if isinstance(required_skills, str):
            required_skills = json.loads(required_skills)
        if isinstance(preferred_skills, str):
            preferred_skills = json.loads(preferred_skills)
        
        # Normalize skills
        extracted_lower = {s.lower(): s for s in extracted_skills}
        
        # Find matches
        matched_required = []
        missing_required = []
        
        for skill in required_skills:
            matched = False
            for ext_lower, ext_skill in extracted_lower.items():
                if self._fuzzy_match(skill.lower(), ext_lower):
                    matched_required.append({
                        'required': skill,
                        'matched_with': ext_skill,
                        'match_type': 'exact' if skill.lower() == ext_lower else 'fuzzy'
                    })
                    matched = True
                    break
            
            if not matched:
                missing_required.append(skill)
        
        matched_preferred = []
        missing_preferred = []
        
        for skill in preferred_skills:
            matched = False
            for ext_lower, ext_skill in extracted_lower.items():
                if self._fuzzy_match(skill.lower(), ext_lower):
                    matched_preferred.append({
                        'preferred': skill,
                        'matched_with': ext_skill,
                        'match_type': 'exact' if skill.lower() == ext_lower else 'fuzzy'
                    })
                    matched = True
                    break
            
            if not matched:
                missing_preferred.append(skill)
        
        # Calculate match percentage
        total_required = len(required_skills)
        match_percentage = (len(matched_required) / total_required * 100) if total_required > 0 else 0
        
        # Generate priority list
        priority_skills = self._generate_priorities(missing_required, missing_preferred)
        
        return {
            'matched_skills': [m.get('required') or m.get('preferred') for m in matched_required + matched_preferred],
            'semantic_matches': matched_required + matched_preferred,
            'missing_skills': missing_required + missing_preferred,
            'missing_required': missing_required,
            'missing_preferred': missing_preferred,
            'match_percentage': round(match_percentage, 1),
            'priority_skills': priority_skills,
            'total_required': total_required,
            'matched_count': len(matched_required),
            'analysis_method': 'basic_fuzzy_match'
        }
    
    def _fuzzy_match(self, skill1: str, skill2: str) -> bool:
        """Check if two skills match using fuzzy logic"""
        if skill1 == skill2:
            return True
        
        if skill1 in skill2 or skill2 in skill1:
            return True
        
        # Common variations
        variations = {
            'javascript': ['js', 'ecmascript', 'es6'],
            'typescript': ['ts'],
            'python': ['py', 'python3'],
            'machine learning': ['ml', 'machinelearning'],
            'deep learning': ['dl', 'deeplearning'],
            'artificial intelligence': ['ai'],
            'natural language processing': ['nlp'],
            'computer vision': ['cv'],
            'amazon web services': ['aws'],
            'google cloud platform': ['gcp', 'google cloud'],
            'microsoft azure': ['azure'],
            'kubernetes': ['k8s'],
            'postgresql': ['postgres', 'psql'],
            'mongodb': ['mongo'],
            'tensorflow': ['tf'],
            'react': ['reactjs', 'react.js'],
            'angular': ['angularjs', 'angular.js'],
            'vue': ['vuejs', 'vue.js'],
            'node': ['nodejs', 'node.js'],
        }
        
        for canonical, aliases in variations.items():
            all_forms = [canonical] + aliases
            if skill1 in all_forms and skill2 in all_forms:
                return True
        
        return False
    
    def _generate_priorities(self, missing_required: List[str],
                              missing_preferred: List[str]) -> List[Dict]:
        """Generate priority list"""
        priorities = []
        
        for i, skill in enumerate(missing_required):
            priorities.append({
                'skill': skill,
                'priority': 'critical' if i < 2 else 'high',
                'reason': 'Required skill for this role',
                'estimated_learning_weeks': self._estimate_time(skill)
            })
        
        for skill in missing_preferred:
            priorities.append({
                'skill': skill,
                'priority': 'medium',
                'reason': 'Preferred skill that enhances candidacy',
                'estimated_learning_weeks': self._estimate_time(skill)
            })
        
        return priorities[:10]
    
    def _estimate_time(self, skill: str) -> int:
        """Estimate learning time in weeks"""
        skill_lower = skill.lower()
        
        complex_skills = ['machine learning', 'deep learning', 'kubernetes', 'system design']
        medium_skills = ['python', 'java', 'javascript', 'react', 'aws', 'docker']
        
        for s in complex_skills:
            if s in skill_lower:
                return 12
        
        for s in medium_skills:
            if s in skill_lower:
                return 6
        
        return 4