from flask import Flask
from flask_cors import CORS
from config import Config

# Import API Blueprints
from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.enrollment_routes import enrollment_bp
from routes.admin_routes import admin_bp

# Import the Frontend Blueprint
from routes.frontend_routes import frontend_bp

# Import MongoDB collection
from utils.db import courses_collection

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'supersecretkey'
    # Enable CORS to allow your frontend HTML files to make requests to this backend API
    CORS(app)

    # Register the Blueprints (API endpoints)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(enrollment_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    # Register Frontend Routes (No URL prefix so it serves at the root domain)
    app.register_blueprint(frontend_bp)

    # Seed MongoDB with initial courses if the collection is empty
    # We do this inside the app context so the app is fully initialized
    with app.app_context():
        seed_courses()

    return app

def seed_courses():
    """Seeds the MongoDB Atlas database with your local image paths."""
    if courses_collection.count_documents({}) == 0:
        initial_courses = [
            {
                "title": "Full-Stack Web Development", 
                "description": "Master HTML, CSS, JavaScript, Node.js & Full Stack Projects.", 
                "price": 4999.0, 
                "image": "/static/images/Course Card1.jpg"
            },
            {
                "title": "Python & Data Science", 
                "description": "Learn Python, Pandas, Machine Learning Models, and more.", 
                "price": 6999.0, 
                "image": "/static/images/Course Card2.jpg"
            },
            {
                "title": "Linux System Administration", 
                "description": "Master TCP/IP networking, firewalls, and server management.", 
                "price": 3999.0, 
                "image": "/static/images/Course Card3.jpg"
            },
            {
                "title": "Android App Development", 
                "description": "Build robust Android applications using Java & Kotlin.", 
                "price": 5999.0, 
                "image": "/static/images/Course Card4.jpg"
            },
            {
                "title": "Digital Marketing Expert", 
                "description": "Master SEO, Social Media Marketing, and Ads Strategy.", 
                "price": 4499.0, 
                "image": "/static/images/Course Card5.jpg"
            },
            {
                "title": "Generative AI & ChatGPT", 
                "description": "Learn Prompt Engineering, AI Automation, and intelligent systems.", 
                "price": 7999.0, 
                "image": "/static/images/Course Card6.jpg"
            }
        ]
        courses_collection.insert_many(initial_courses)
        print("MongoDB Atlas Seeded with Local Image Paths!")

if __name__ == '__main__':
    app = create_app()
    # Run the server on port 5000 in debug mode
    app.run(debug=True, port=5000)