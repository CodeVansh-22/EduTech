from flask import Blueprint, render_template

# Create a blueprint for frontend views
frontend_bp = Blueprint('frontend_routes', __name__)

# Map the root URL to index.html
@frontend_bp.route('/')
@frontend_bp.route('/index.html')
def index():
    return render_template('index.html')

# Map the courses page
@frontend_bp.route('/courses.html')
def courses():
    return render_template('courses.html')

# Map the login page
@frontend_bp.route('/login.html')
def login():
    return render_template('login.html')

# Map the register page
@frontend_bp.route('/register.html')
def register():
    return render_template('register.html')

# Map the student dashboard
@frontend_bp.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

# Map the admin dashboard
@frontend_bp.route('/admin-dashboard.html')
def admin():
    return render_template('admin-dashboard.html')