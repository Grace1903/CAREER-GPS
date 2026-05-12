from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, get_jwt
)
from app import db, bcrypt
from app.models import User
from datetime import datetime, timedelta
import secrets
import json

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        flash('Please provide email and password', 'error')
        return render_template('auth/login.html')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not bcrypt.check_password_hash(user.password, password):
        flash('Invalid email or password', 'error')
        return render_template('auth/login.html')
    
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={'role': user.role, 'email': user.email}
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        additional_claims={'role': user.role}
    )
    
    if user.role == 'admin':
        response = make_response(redirect(url_for('admin.dashboard')))
    else:
        response = make_response(redirect(url_for('student.dashboard')))
    
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    
    flash(f'Welcome back, {user.full_name}!', 'success')
    return response


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    data = request.form
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    full_name = data.get('full_name')
    
    if not all([email, password, confirm_password, full_name]):
        flash('All fields are required', 'error')
        return render_template('auth/register.html')
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return render_template('auth/register.html')
    
    if User.query.filter_by(email=email).first():
        flash('Email already registered', 'error')
        return render_template('auth/register.html')
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        role='student'
    )
    
    db.session.add(user)
    db.session.commit()
    
    flash('Registration successful! Please login.', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('main.landing')))
    unset_jwt_cookies(response)
    flash('You have been logged out', 'info')
    return response


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    
    if user:
        token = secrets.token_urlsafe(32)
        user.reset_token = token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        
        reset_link = url_for('auth.reset_password', token=token, _external=True)
        flash(f'Password reset link (DEV MODE): {reset_link}', 'info')
    else:
        flash('If the email exists, a reset link has been sent.', 'info')
    
    return render_template('auth/forgot_password.html')


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        flash('Invalid or expired reset token', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'GET':
        return render_template('auth/reset_password.html', token=token)
    
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return render_template('auth/reset_password.html', token=token)
    
    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    
    flash('Password reset successful! Please login.', 'success')
    return redirect(url_for('auth.login'))