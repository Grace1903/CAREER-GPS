"""
Career Roadmap Generation Service
Generate structured learning paths with phases and timelines
"""
import os
import json
import re


class RoadmapGenerator:
    """
    Generate career roadmaps with learning phases
    """
    
    def __init__(self):
        self.gemini_model = None
        self._init_gemini()
        
        # Skill complexity estimates (weeks to learn)
        self.skill_complexity = {
            'beginner': {'weeks': 2, 'description': 'Basic understanding'},
            'intermediate': {'weeks': 4, 'description': 'Working proficiency'},
            'advanced': {'weeks': 8, 'description': 'Expert level'}
        }
    
    def _init_gemini(self):
        """Initialize Gemini API"""
        try:
            import google.generativeai as genai
            
            api_key = os.environ.get('GEMINI_API_KEY', '')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            print(f"Failed to initialize Gemini: {e}")
    
    def generate(self, current_skills, missing_skills, target_role):
        """
        Generate a career roadmap
        """
        if self.gemini_model:
            try:
                return self._generate_with_llm(current_skills, missing_skills, target_role)
            except Exception as e:
                print(f"LLM roadmap generation failed: {e}")
        
        return self._generate_basic_roadmap(current_skills, missing_skills, target_role)
    
    def _generate_with_llm(self, current_skills, missing_skills, target_role):
        """Generate roadmap using Gemini LLM"""
        prompt = f"""
        Create a career roadmap for someone targeting the role of "{target_role}".
        
        Current Skills: {current_skills}
        Skills to Learn: {missing_skills}
        
        Generate a structured learning path with 3-4 phases. Each phase should have:
        1. Phase name
        2. Duration (in weeks)
        3. Skills to focus on
        4. Learning goals
        5. Milestones
        
        Return as JSON with this format:
        {{
            "target_role": "{target_role}",
            "total_duration_weeks": number,
            "phases": [
                {{
                    "phase_number": 1,
                    "name": "Foundation",
                    "duration_weeks": 4,
                    "skills": ["skill1", "skill2"],
                    "goals": ["goal1", "goal2"],
                    "milestones": ["milestone1"],
                    "resources": ["resource type"]
                }}
            ],
            "career_progression": [
                {{"stage": "Current", "role": "...", "timeline": "Now"}},
                {{"stage": "Milestone 1", "role": "...", "timeline": "3 months"}}
            ]
        }}
        
        Return ONLY the JSON, no other text.
        """
        
        response = self.gemini_model.generate_content(prompt)
        response_text = response.text
        
        # Extract JSON
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            roadmap = json.loads(json_match.group())
            return roadmap
        
        return self._generate_basic_roadmap(current_skills, missing_skills, target_role)
    
    def _generate_basic_roadmap(self, current_skills, missing_skills, target_role):
        """Generate a basic roadmap without LLM"""
        # Categorize missing skills by estimated complexity
        phases = []
        
        # Phase 1: Foundation (first 1/3 of skills)
        phase1_skills = missing_skills[:len(missing_skills)//3 + 1]
        phases.append({
            'phase_number': 1,
            'name': 'Foundation Building',
            'duration_weeks': max(4, len(phase1_skills) * 2),
            'skills': phase1_skills,
            'goals': [
                f'Learn fundamentals of {skill}' for skill in phase1_skills[:3]
            ],
            'milestones': [
                'Complete basic tutorials',
                'Build simple practice projects',
                'Understand core concepts'
            ],
            'resources': ['Online courses', 'Documentation', 'Tutorials']
        })
        
        # Phase 2: Intermediate (middle 1/3 of skills)
        start_idx = len(missing_skills)//3 + 1
        end_idx = 2 * len(missing_skills)//3 + 1
        phase2_skills = missing_skills[start_idx:end_idx]
        
        if phase2_skills:
            phases.append({
                'phase_number': 2,
                'name': 'Skill Development',
                'duration_weeks': max(6, len(phase2_skills) * 2),
                'skills': phase2_skills,
                'goals': [
                    f'Develop proficiency in {skill}' for skill in phase2_skills[:3]
                ],
                'milestones': [
                    'Complete intermediate projects',
                    'Contribute to open source',
                    'Build portfolio pieces'
                ],
                'resources': ['Advanced courses', 'Projects', 'Community']
            })
        
        # Phase 3: Advanced (remaining skills)
        phase3_skills = missing_skills[end_idx:]
        
        if phase3_skills:
            phases.append({
                'phase_number': 3,
                'name': 'Advanced Specialization',
                'duration_weeks': max(8, len(phase3_skills) * 3),
                'skills': phase3_skills,
                'goals': [
                    f'Master {skill}' for skill in phase3_skills[:3]
                ],
                'milestones': [
                    'Complete complex projects',
                    'Obtain certifications',
                    'Mentor others'
                ],
                'resources': ['Certifications', 'Real projects', 'Mentorship']
            })
        
        # Phase 4: Job Ready
        phases.append({
            'phase_number': len(phases) + 1,
            'name': 'Job Preparation',
            'duration_weeks': 4,
            'skills': ['Interview Skills', 'Resume Building', 'Networking'],
            'goals': [
                'Prepare for technical interviews',
                'Build professional network',
                'Apply for positions'
            ],
            'milestones': [
                'Complete mock interviews',
                'Update portfolio',
                'Start job applications'
            ],
            'resources': ['LeetCode', 'LinkedIn', 'Job boards']
        })
        
        total_weeks = sum(phase['duration_weeks'] for phase in phases)
        
        return {
            'target_role': target_role,
            'total_duration_weeks': total_weeks,
            'phases': phases,
            'career_progression': [
                {'stage': 'Current', 'role': 'Learning Phase', 'timeline': 'Now'},
                {'stage': 'Phase 1 Complete', 'role': 'Beginner Developer', 'timeline': f'{phases[0]["duration_weeks"]} weeks'},
                {'stage': 'Phase 2 Complete', 'role': 'Junior Developer', 'timeline': f'{total_weeks//2} weeks'},
                {'stage': 'Ready', 'role': target_role, 'timeline': f'{total_weeks} weeks'}
            ],
            'current_skills_count': len(current_skills),
            'skills_to_learn_count': len(missing_skills)
        }