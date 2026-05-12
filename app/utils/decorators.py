"""
Custom Decorators - FIXED VERSION
"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt


def student_required(fn):
    """Decorator to ensure user is a student or admin"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get('role', 'student')
            
            if role not in ['student', 'admin']:
                flash('Access denied', 'error')
                return redirect(url_for('main.landing'))
            return fn(*args, **kwargs)
        except Exception as e:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
    return wrapper


def admin_required(fn):
    """Decorator to ensure user is an admin"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get('role', '')
            
            if role != 'admin':
                flash('Admin access required', 'error')
                return redirect(url_for('main.landing'))
            return fn(*args, **kwargs)
        except Exception as e:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
    return wrapper


def get_current_user_id():
    """Helper to get current user ID from JWT"""
    identity = get_jwt_identity()
    return int(identity) if identity else None


def get_current_user_role():
    """Helper to get current user role from JWT claims"""
    claims = get_jwt()
    return claims.get('role', 'student')