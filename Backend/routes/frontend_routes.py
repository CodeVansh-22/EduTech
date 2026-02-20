from flask import Blueprint, render_template, session, redirect

frontend_bp = Blueprint('frontend_routes', __name__)

@frontend_bp.route('/')
@frontend_bp.route('/index.html')
def index():
    return render_template('index.html')

@frontend_bp.route('/courses.html')
def courses():
    return render_template('courses.html')

@frontend_bp.route('/login.html')
def login():
    return render_template('login.html')

@frontend_bp.route('/register.html')
def register():
    return render_template('register.html')

@frontend_bp.route('/dashboard.html')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login.html')
    return render_template('dashboard.html')

@frontend_bp.route('/admin-dashboard.html')
def admin():
    if 'role' not in session or session['role'] != 'admin':
        return redirect('/login.html')
    return render_template('admin-dashboard.html')