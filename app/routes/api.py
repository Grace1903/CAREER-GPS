from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import JobRole, Course, SkillTaxonomy, Analysis, JobStabilityData

api_bp = Blueprint('api', __name__)


@api_bp.route('/job-roles')
@jwt_required()
def get_job_roles():
    jobs = JobRole.query.all()
    return jsonify([job.to_dict() for job in jobs])


@api_bp.route('/job-roles/<int:job_id>')
@jwt_required()
def get_job_role(job_id):
    job = JobRole.query.get_or_404(job_id)
    return jsonify(job.to_dict())


@api_bp.route('/courses')
@jwt_required()
def get_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])


@api_bp.route('/skills')
@jwt_required()
def get_skills():
    skills = SkillTaxonomy.query.all()
    return jsonify([skill.to_dict() for skill in skills])


@api_bp.route('/analysis/<int:analysis_id>')
@jwt_required()
def get_analysis(analysis_id):
    user_id = get_jwt_identity()
    claims = get_jwt()
    role = claims.get('role', 'student')
    
    analysis = Analysis.query.filter_by(id=analysis_id).first()
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    if str(analysis.user_id) != str(user_id) and role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify(analysis.to_dict())


@api_bp.route('/stability/<job_title>')
@jwt_required()
def get_stability(job_title):
    stability = JobStabilityData.query.filter_by(job_title=job_title).first()
    if not stability:
        return jsonify({'error': 'Stability data not found'}), 404
    return jsonify(stability.to_dict())