from flask import Blueprint, request, jsonify, session
from ..utils.db import users_collection, courses_collection, enrollments_collection
from bson.objectid import ObjectId

admin_bp = Blueprint('admin_routes', __name__)

# ------------------------------
# ADMIN ROLE PROTECTION FUNCTION
# ------------------------------
def admin_required():
    if 'role' not in session or session['role'] != 'admin':
        return False
    return True


# ------------------------------
# ADD COURSE
# ------------------------------
@admin_bp.route('/courses', methods=['POST'])
def add_course():
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()

    new_course = {
        "title": data.get('title'),
        "description": data.get('description'),
        "price": float(data.get('price')),
        "image": data.get('image')
    }

    result = courses_collection.insert_one(new_course)

    return jsonify({
        "message": "Course added successfully!",
        "course_id": str(result.inserted_id)
    }), 201


# ------------------------------
# DELETE COURSE
# ------------------------------
@admin_bp.route('/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    courses_collection.delete_one({"_id": ObjectId(course_id)})
    enrollments_collection.delete_many({"course_id": course_id})

    return jsonify({"message": "Course deleted successfully!"}), 200


# ------------------------------
# ANALYTICS
# ------------------------------
@admin_bp.route('/analytics', methods=['GET'])
def get_analytics():
    if not admin_required():
        return jsonify({"error": "Unauthorized"}), 403

    # Daily Aggregation
    daily_pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d",
                        "date": "$enrolled_at"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}},
        {"$limit": 7}
    ]

    daily_data = list(enrollments_collection.aggregate(daily_pipeline))

    # Monthly Aggregation
    monthly_pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m",
                        "date": "$enrolled_at"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": 1}},
        {"$limit": 6}
    ]

    monthly_data = list(enrollments_collection.aggregate(monthly_pipeline))

    return jsonify({
        "totals": {
            "users": users_collection.count_documents({}),
            "courses": courses_collection.count_documents({}),
            "enrollments": enrollments_collection.count_documents({})
        },
        "chart_data": {
            "daily_labels": [item['_id'] for item in daily_data] if daily_data else ['No Data'],
            "daily_data": [item['count'] for item in daily_data] if daily_data else [0],
            "monthly_labels": [item['_id'] for item in monthly_data] if monthly_data else ['No Data'],
            "monthly_data": [item['count'] for item in monthly_data] if monthly_data else [0],
            "yearly_labels": [item['_id'][:4] for item in monthly_data] if monthly_data else ['No Data'],
            "yearly_data": [item['count'] for item in monthly_data] if monthly_data else [0]
        }
    }), 200