from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import User, JobRole, Course, SkillTaxonomy, JobStabilityData, Analysis
from app.utils.decorators import admin_required
import json

admin_bp = Blueprint('admin', __name__)


def get_current_user():
    user_id = get_jwt_identity()
    return User.query.get(int(user_id))


@admin_bp.route('/dashboard')
@jwt_required()
@admin_required
def dashboard():
    user = get_current_user()
    
    # Statistics
    total_users = User.query.filter_by(role='student').count()
    total_analyses = Analysis.query.count()
    total_jobs = JobRole.query.count()
    total_courses = Course.query.count()
    total_skills = SkillTaxonomy.query.count()
    
    recent_analyses = Analysis.query.order_by(Analysis.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                          user=user,
                          total_users=total_users,
                          total_analyses=total_analyses,
                          total_jobs=total_jobs,
                          total_courses=total_courses,
                          total_skills=total_skills,
                          recent_analyses=recent_analyses)


@admin_bp.route('/jobs', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_jobs():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            title = request.form.get('title')
            industry = request.form.get('industry')
            required_skills = request.form.get('required_skills', '').split(',')
            preferred_skills = request.form.get('preferred_skills', '').split(',')
            description = request.form.get('description')
            
            job = JobRole(
                title=title.strip(),
                industry=industry.strip(),
                required_skills=json.dumps([s.strip() for s in required_skills if s.strip()]),
                preferred_skills=json.dumps([s.strip() for s in preferred_skills if s.strip()]),
                description=description
            )
            db.session.add(job)
            db.session.commit()
            flash('Job role added successfully', 'success')
            
        elif action == 'delete':
            job_id = request.form.get('job_id')
            job = JobRole.query.get(job_id)
            if job:
                db.session.delete(job)
                db.session.commit()
                flash('Job role deleted successfully', 'success')
                
        elif action == 'update':
            job_id = request.form.get('job_id')
            job = JobRole.query.get(job_id)
            if job:
                job.title = request.form.get('title', job.title)
                job.industry = request.form.get('industry', job.industry)
                required_skills = request.form.get('required_skills', '').split(',')
                preferred_skills = request.form.get('preferred_skills', '').split(',')
                job.required_skills = json.dumps([s.strip() for s in required_skills if s.strip()])
                job.preferred_skills = json.dumps([s.strip() for s in preferred_skills if s.strip()])
                job.description = request.form.get('description', job.description)
                db.session.commit()
                flash('Job role updated successfully', 'success')
    
    jobs = JobRole.query.all()
    return render_template('admin/manage_jobs.html', user=user, jobs=jobs)


@admin_bp.route('/courses', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_courses():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            name = request.form.get('name')
            provider = request.form.get('provider')
            skills_covered = request.form.get('skills_covered', '').split(',')
            duration_hours = request.form.get('duration_hours', type=int)
            difficulty = request.form.get('difficulty')
            rating = request.form.get('rating', type=float)
            url = request.form.get('url')
            price = request.form.get('price')
            has_certificate = request.form.get('has_certificate') == 'on'
            
            course = Course(
                name=name.strip(),
                provider=provider.strip(),
                skills_covered=json.dumps([s.strip() for s in skills_covered if s.strip()]),
                duration_hours=duration_hours,
                difficulty=difficulty,
                rating=rating,
                url=url,
                price=price,
                has_certificate=has_certificate
            )
            db.session.add(course)
            db.session.commit()
            flash('Course added successfully', 'success')
            
        elif action == 'delete':
            course_id = request.form.get('course_id')
            course = Course.query.get(course_id)
            if course:
                db.session.delete(course)
                db.session.commit()
                flash('Course deleted successfully', 'success')
    
    courses = Course.query.all()
    return render_template('admin/manage_courses.html', user=user, courses=courses)


@admin_bp.route('/skills', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_skills():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            skill_name = request.form.get('skill_name')
            category = request.form.get('category')
            aliases = request.form.get('aliases', '').split(',')
            
            skill = SkillTaxonomy(
                skill_name=skill_name.strip(),
                category=category.strip(),
                aliases=json.dumps([a.strip() for a in aliases if a.strip()])
            )
            db.session.add(skill)
            db.session.commit()
            flash('Skill added successfully', 'success')
            
        elif action == 'delete':
            skill_id = request.form.get('skill_id')
            skill = SkillTaxonomy.query.get(skill_id)
            if skill:
                db.session.delete(skill)
                db.session.commit()
                flash('Skill deleted successfully', 'success')
    
    skills = SkillTaxonomy.query.order_by(SkillTaxonomy.category).all()
    categories = db.session.query(SkillTaxonomy.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('admin/manage_skills.html', 
                          user=user, 
                          skills=skills,
                          categories=categories)


@admin_bp.route('/stability', methods=['GET', 'POST'])
@jwt_required()
@admin_required
def manage_stability():
    user = get_current_user()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'add':
            stability = JobStabilityData(
                job_title=request.form.get('job_title'),
                industry=request.form.get('industry'),
                avg_salary_lpa=float(request.form.get('avg_salary_lpa', 0)),
                demand_growth_percent=float(request.form.get('demand_growth_percent', 0)),
                automation_risk_percent=float(request.form.get('automation_risk_percent', 0)),
                layoff_rate_percent=float(request.form.get('layoff_rate_percent', 0)),
                skill_obsolescence_rate=float(request.form.get('skill_obsolescence_rate', 0)),
                remote_work_possibility=int(request.form.get('remote_work_possibility', 0)),
                required_skill_level=int(request.form.get('required_skill_level', 1)),
                industry_growth_percent=float(request.form.get('industry_growth_percent', 0)),
                economic_sensitivity=int(request.form.get('economic_sensitivity', 1)),
                experience_level=request.form.get('experience_level', 'mid')
            )
            db.session.add(stability)
            db.session.commit()
            flash('Job stability data added successfully', 'success')
            
        elif action == 'delete':
            stability_id = request.form.get('stability_id')
            stability = JobStabilityData.query.get(stability_id)
            if stability:
                db.session.delete(stability)
                db.session.commit()
                flash('Job stability data deleted successfully', 'success')
    
    stability_data = JobStabilityData.query.all()
    return render_template('admin/manage_stability.html', 
                          user=user, 
                          stability_data=stability_data)


@admin_bp.route('/users')
@jwt_required()
@admin_required
def manage_users():
    user = get_current_user()
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/manage_users.html', user=user, users=users)

@admin_bp.route('/refresh-vector-store', methods=['POST'])
@jwt_required()
@admin_required
def refresh_vector_store():
    try:
        from app.services.vector_store_initializer import refresh_vector_store as refresh_vs
        
        success = refresh_vs()
        
        if success:
            flash('Vector store refreshed successfully!', 'success')
        else:
            flash('Vector store refresh failed. Check server logs.', 'warning')
            
    except Exception as e:
        flash(f'Error refreshing vector store: {str(e)}', 'error')
    
    return redirect(url_for('admin.dashboard'))