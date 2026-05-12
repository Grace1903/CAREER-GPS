"""
Database Models
"""
from datetime import datetime
from app import db
import json


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='student')  # 'student' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy=True)
    analyses = db.relationship('Analysis', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }


class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    analyses = db.relationship('Analysis', backref='resume', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.original_filename,
            'upload_date': self.upload_date.isoformat(),
            'has_text': bool(self.extracted_text)
        }


class Analysis(db.Model):
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    target_job_role = db.Column(db.String(100), nullable=False)
    
    # Extracted Skills
    extracted_skills = db.Column(db.Text, nullable=True)  # JSON
    technical_skills = db.Column(db.Text, nullable=True)  # JSON
    soft_skills = db.Column(db.Text, nullable=True)  # JSON
    
    # Skill Gap Analysis
    matched_skills = db.Column(db.Text, nullable=True)  # JSON
    missing_skills = db.Column(db.Text, nullable=True)  # JSON
    skill_match_percentage = db.Column(db.Float, nullable=True)
    priority_skills = db.Column(db.Text, nullable=True)  # JSON
    
    # Course Recommendations
    recommended_courses = db.Column(db.Text, nullable=True)  # JSON
    
    # Career Roadmap
    career_roadmap = db.Column(db.Text, nullable=True)  # JSON
    
    # Job Stability
    stability_score = db.Column(db.Float, nullable=True)
    stability_analysis = db.Column(db.Text, nullable=True)  # JSON
    risk_classification = db.Column(db.String(50), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processing_time = db.Column(db.Float, nullable=True)  # in seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'target_job_role': self.target_job_role,
            'extracted_skills': json.loads(self.extracted_skills) if self.extracted_skills else [],
            'technical_skills': json.loads(self.technical_skills) if self.technical_skills else [],
            'soft_skills': json.loads(self.soft_skills) if self.soft_skills else [],
            'matched_skills': json.loads(self.matched_skills) if self.matched_skills else [],
            'missing_skills': json.loads(self.missing_skills) if self.missing_skills else [],
            'skill_match_percentage': self.skill_match_percentage,
            'priority_skills': json.loads(self.priority_skills) if self.priority_skills else [],
            'recommended_courses': json.loads(self.recommended_courses) if self.recommended_courses else [],
            'career_roadmap': json.loads(self.career_roadmap) if self.career_roadmap else {},
            'stability_score': self.stability_score,
            'stability_analysis': json.loads(self.stability_analysis) if self.stability_analysis else {},
            'risk_classification': self.risk_classification,
            'created_at': self.created_at.isoformat(),
            'processing_time': self.processing_time
        }


class JobRole(db.Model):
    __tablename__ = 'job_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    required_skills = db.Column(db.Text, nullable=False)  # JSON
    preferred_skills = db.Column(db.Text, nullable=True)  # JSON
    experience_levels = db.Column(db.Text, nullable=True)  # JSON
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'industry': self.industry,
            'required_skills': json.loads(self.required_skills),
            'preferred_skills': json.loads(self.preferred_skills) if self.preferred_skills else [],
            'experience_levels': json.loads(self.experience_levels) if self.experience_levels else {},
            'description': self.description
        }


class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    skills_covered = db.Column(db.Text, nullable=False)  # JSON
    duration_hours = db.Column(db.Integer, nullable=True)
    difficulty = db.Column(db.String(50), nullable=True)  # beginner, intermediate, advanced
    rating = db.Column(db.Float, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    price = db.Column(db.String(50), nullable=True)
    has_certificate = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'skills_covered': json.loads(self.skills_covered),
            'duration_hours': self.duration_hours,
            'difficulty': self.difficulty,
            'rating': self.rating,
            'url': self.url,
            'price': self.price,
            'has_certificate': self.has_certificate
        }


class SkillTaxonomy(db.Model):
    __tablename__ = 'skill_taxonomy'
    
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    aliases = db.Column(db.Text, nullable=True)  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name,
            'category': self.category,
            'aliases': json.loads(self.aliases) if self.aliases else []
        }


class JobStabilityData(db.Model):
    __tablename__ = 'job_stability_data'
    
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    avg_salary_lpa = db.Column(db.Float, nullable=False)
    demand_growth_percent = db.Column(db.Float, nullable=False)
    automation_risk_percent = db.Column(db.Float, nullable=False)
    layoff_rate_percent = db.Column(db.Float, nullable=False)
    skill_obsolescence_rate = db.Column(db.Float, nullable=False)
    remote_work_possibility = db.Column(db.Integer, nullable=False)
    required_skill_level = db.Column(db.Integer, nullable=False)
    industry_growth_percent = db.Column(db.Float, nullable=False)
    economic_sensitivity = db.Column(db.Integer, nullable=False)
    experience_level = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_title': self.job_title,
            'industry': self.industry,
            'avg_salary_lpa': self.avg_salary_lpa,
            'demand_growth_percent': self.demand_growth_percent,
            'automation_risk_percent': self.automation_risk_percent,
            'layoff_rate_percent': self.layoff_rate_percent,
            'skill_obsolescence_rate': self.skill_obsolescence_rate,
            'remote_work_possibility': self.remote_work_possibility,
            'required_skill_level': self.required_skill_level,
            'industry_growth_percent': self.industry_growth_percent,
            'economic_sensitivity': self.economic_sensitivity,
            'experience_level': self.experience_level
        }