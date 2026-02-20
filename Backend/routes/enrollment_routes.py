from flask import Blueprint, request, jsonify
from utils.db import enrollments_collection, courses_collection
from bson.objectid import ObjectId
from datetime import datetime

enrollment_bp = Blueprint('enrollment_routes', __name__)

@enrollment_bp.route('/enroll', methods=['POST'])
def enroll_course():
    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')

    # Check for duplicate
    if enrollments_collection.find_one({"user_id": user_id, "course_id": course_id}):
        return jsonify({"error": "You are already enrolled in this course"}), 400

    new_enrollment = {
        "user_id": user_id,
        "course_id": course_id,
        "enrolled_at": datetime.utcnow()
    }
    enrollments_collection.insert_one(new_enrollment)

    return jsonify({"message": "Successfully enrolled!"}), 201

@enrollment_bp.route('/my-courses/<user_id>', methods=['GET'])
def get_user_courses(user_id):
    # MongoDB aggregation to join enrollments with courses ($lookup)
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$addFields": {"course_obj_id": {"$toObjectId": "$course_id"}}},
        {"$lookup": {
            "from": "courses",
            "localField": "course_obj_id",
            "foreignField": "_id",
            "as": "course_details"
        }},
        {"$unwind": "$course_details"}
    ]
    
    enrollments = list(enrollments_collection.aggregate(pipeline))
    
    my_courses = []
    for enr in enrollments:
        course = enr['course_details']
        my_courses.append({
            "enrollment_id": str(enr['_id']),
            "course_id": str(course['_id']),
            "title": course['title'],
            "image": course['image'],
            "enrolled_at": enr['enrolled_at'].strftime("%Y-%m-%d")
        })

    return jsonify(my_courses), 200