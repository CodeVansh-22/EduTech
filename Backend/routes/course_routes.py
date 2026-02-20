from flask import Blueprint, jsonify
from utils.db import courses_collection

course_bp = Blueprint('course_routes', __name__)

@course_bp.route('/courses', methods=['GET'])
def get_courses():
    courses = list(courses_collection.find({}))
    course_list = []
    
    for course in courses:
        course_list.append({
            "id": str(course['_id']), # Convert MongoDB ObjectId to string
            "title": course['title'],
            "description": course['description'],
            "price": course['price'],
            "image": course['image']
        })
        
    return jsonify(course_list), 200