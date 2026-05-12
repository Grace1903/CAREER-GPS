from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from app import db
from app.models import User, Resume, Analysis, JobRole, Course
from app.services.pdf_extractor import PDFExtractor
from app.services.nlp_processor import NLPProcessor
from app.services.skill_extractor import SkillExtractor
from app.services.skill_gap_analyzer import SkillGapAnalyzer
from app.services.course_recommender import CourseRecommender
from app.services.roadmap_generator import RoadmapGenerator
from app.services.stability_analyzer import StabilityAnalyzer
from app.utils.decorators import student_required
import os
import uuid
import json
import time

student_bp = Blueprint('student', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


@student_bp.route('/dashboard')
@jwt_required()
@student_required
def dashboard():
    user = get_current_user()
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.login'))
    
    recent_analyses = Analysis.query.filter_by(user_id=user.id)\
        .order_by(Analysis.created_at.desc())\
        .limit(5).all()
    
    total_analyses = Analysis.query.filter_by(user_id=user.id).count()
    total_resumes = Resume.query.filter_by(user_id=user.id).count()
    
    job_roles = JobRole.query.all()
    
    return render_template('student/dashboard.html',
                          user=user,
                          recent_analyses=recent_analyses,
                          total_analyses=total_analyses,
                          total_resumes=total_resumes,
                          job_roles=job_roles)


@student_bp.route('/upload', methods=['GET', 'POST'])
@jwt_required()
@student_required
def upload_resume():
    user = get_current_user()
    job_roles = JobRole.query.all()
    
    if request.method == 'GET':
        return render_template('student/upload.html', user=user, job_roles=job_roles)
    
    if 'resume' not in request.files:
        flash('No file uploaded', 'error')
        return render_template('student/upload.html', user=user, job_roles=job_roles)
    
    file = request.files['resume']
    target_job_role = request.form.get('job_role')
    
    if file.filename == '':
        flash('No file selected', 'error')
        return render_template('student/upload.html', user=user, job_roles=job_roles)
    
    if not allowed_file(file.filename):
        flash('Only PDF files are allowed', 'error')
        return render_template('student/upload.html', user=user, job_roles=job_roles)
    
    if not target_job_role:
        flash('Please select a target job role', 'error')
        return render_template('student/upload.html', user=user, job_roles=job_roles)
    
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{original_filename}"
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)
    
    resume = Resume(
        user_id=user.id,
        filename=unique_filename,
        original_filename=original_filename,
        file_path=file_path
    )
    db.session.add(resume)
    db.session.commit()
    
    return redirect(url_for('student.analyze_resume', resume_id=resume.id, job_role=target_job_role))


@student_bp.route('/analyze/<int:resume_id>')
@jwt_required()
@student_required
def analyze_resume(resume_id):
    user = get_current_user()
    
    resume = Resume.query.filter_by(id=resume_id, user_id=user.id).first()
    if not resume:
        flash('Resume not found', 'error')
        return redirect(url_for('student.dashboard'))
    
    job_role = request.args.get('job_role')
    if not job_role:
        flash('Job role not specified', 'error')
        return redirect(url_for('student.dashboard'))
    
    start_time = time.time()
    
    try:

        pdf_extractor = PDFExtractor()
        extracted_text = pdf_extractor.extract_text(resume.file_path)
        resume.extracted_text = extracted_text
        db.session.commit()
        
        nlp_processor = NLPProcessor()
        processed_text = nlp_processor.process(extracted_text)
        
        print("Step 3: Skill Extraction")
        skill_extractor = SkillExtractor()
        skills_result = skill_extractor.extract_skills(processed_text, extracted_text)
        print(skills_result)
        
        print("Step 4: Skill Gap Analysis")
        job_role_data = JobRole.query.filter_by(title=job_role).first()
        skill_gap_analyzer = SkillGapAnalyzer()
        gap_analysis = skill_gap_analyzer.analyze(
            skills_result['all_skills'],
            job_role_data.to_dict() if job_role_data else {'title': job_role, 'required_skills': [], 'preferred_skills': []}
        )
        
        course_recommender = CourseRecommender()
        recommended_courses = course_recommender.recommend(gap_analysis['missing_skills'])
        
        roadmap_generator = RoadmapGenerator()
        career_roadmap = roadmap_generator.generate(
            skills_result['all_skills'],
            gap_analysis['missing_skills'],
            job_role
        )
        
        stability_analyzer = StabilityAnalyzer()
        stability_result = stability_analyzer.analyze(job_role)
        
        processing_time = time.time() - start_time
        
        analysis = Analysis(
            user_id=user.id,
            resume_id=resume.id,
            target_job_role=job_role,
            extracted_skills=json.dumps(skills_result['all_skills']),
            technical_skills=json.dumps(skills_result['technical_skills']),
            soft_skills=json.dumps(skills_result['soft_skills']),
            matched_skills=json.dumps(gap_analysis['matched_skills']),
            missing_skills=json.dumps(gap_analysis['missing_skills']),
            skill_match_percentage=gap_analysis['match_percentage'],
            priority_skills=json.dumps(gap_analysis['priority_skills']),
            recommended_courses=json.dumps(recommended_courses),
            career_roadmap=json.dumps(career_roadmap),
            stability_score=stability_result['stability_score'],
            stability_analysis=json.dumps(stability_result),
            risk_classification=stability_result['risk_classification'],
            processing_time=processing_time
        )
        db.session.add(analysis)
        db.session.commit()
        
        return redirect(url_for('student.view_analysis', analysis_id=analysis.id))
        
    except Exception as e:
        flash(f'Error processing resume: {str(e)}', 'error')
        import traceback
        traceback.print_exc()
        return redirect(url_for('student.dashboard'))


@student_bp.route('/analysis/<int:analysis_id>')
@jwt_required()
@student_required
def view_analysis(analysis_id):
    user = get_current_user()
    
    analysis = Analysis.query.filter_by(id=analysis_id, user_id=user.id).first()
    if not analysis:
        flash('Analysis not found', 'error')
        return redirect(url_for('student.dashboard'))
    
    return render_template('student/analysis_result.html',
                          user=user,
                          analysis=analysis.to_dict(),
                          resume=analysis.resume)


@student_bp.route('/history')
@jwt_required()
@student_required
def history():
    user = get_current_user()
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    analyses = Analysis.query.filter_by(user_id=user.id)\
        .order_by(Analysis.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('student/history.html',
                          user=user,
                          analyses=analyses)


@student_bp.route('/profile', methods=['GET', 'POST'])
@jwt_required()
@student_required
def profile():
    user = get_current_user()
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        if full_name:
            user.full_name = full_name
            db.session.commit()
            flash('Profile updated successfully', 'success')
    
    return render_template('student/profile.html', user=user)