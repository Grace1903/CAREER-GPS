"""
Course Recommendation Service
Map skill gaps to relevant learning resources
"""
import json
from app.models import Course


class CourseRecommender:
    """
    Recommend courses based on skill gaps
    """
    
    def __init__(self):
        self.courses = []
        self._load_courses()
    
    def _load_courses(self):
        """Load courses from database"""
        try:
            from flask import current_app
            with current_app.app_context():
                courses = Course.query.all()
                self.courses = [course.to_dict() for course in courses]
        except Exception as e:
            print(f"Error loading courses: {e}")
            self.courses = []
    
    def recommend(self, missing_skills, max_courses_per_skill=3):
        """
        Recommend courses for missing skills
        """
        recommendations = {}
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            matching_courses = []
            
            for course in self.courses:
                skills_covered = course.get('skills_covered', [])
                if isinstance(skills_covered, str):
                    skills_covered = json.loads(skills_covered)
                
                # Check if course covers this skill
                for covered_skill in skills_covered:
                    if skill_lower in covered_skill.lower() or covered_skill.lower() in skill_lower:
                        # Calculate relevance score
                        score = self._calculate_relevance(course, skill)
                        matching_courses.append({
                            **course,
                            'relevance_score': score
                        })
                        break
            
            # Sort by relevance and rating
            matching_courses.sort(key=lambda x: (x['relevance_score'], x.get('rating', 0)), reverse=True)
            
            # Take top courses
            recommendations[skill] = matching_courses[:max_courses_per_skill]
        
        # Flatten and deduplicate for overall recommendations
        all_courses = []
        seen_ids = set()
        
        for skill, courses in recommendations.items():
            for course in courses:
                if course['id'] not in seen_ids:
                    course['target_skill'] = skill
                    all_courses.append(course)
                    seen_ids.add(course['id'])
        
        # Sort by relevance
        all_courses.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return {
            'by_skill': recommendations,
            'top_courses': all_courses[:10],
            'total_recommendations': len(all_courses)
        }
    
    def _calculate_relevance(self, course, skill):
        """Calculate relevance score for a course"""
        score = 0
        
        # Base score for skill match
        score += 50
        
        # Rating bonus
        rating = course.get('rating', 0)
        score += rating * 5
        
        # Certificate bonus
        if course.get('has_certificate'):
            score += 10
        
        # Difficulty matching (prefer intermediate)
        difficulty = course.get('difficulty', 'intermediate')
        if difficulty == 'intermediate':
            score += 10
        elif difficulty == 'beginner':
            score += 5
        
        # Shorter courses slightly preferred (assuming more focused)
        duration = course.get('duration_hours', 50)
        if duration < 30:
            score += 5
        
        return score