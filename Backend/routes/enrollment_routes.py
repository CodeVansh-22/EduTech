from flask import Blueprint, request, jsonify, current_app
from ..utils.db import enrollments_collection, courses_collection
from bson.objectid import ObjectId
from datetime import datetime
import razorpay

enrollment_bp = Blueprint('enrollment_routes', __name__)

# ==========================================
# 1. CREATE RAZORPAY ORDER
# ==========================================
@enrollment_bp.route('/create-order', methods=['POST'])
def create_order():
    data = request.get_json()
    course_id = data.get('course_id')

    # 1. Find the course in the database to get the real price (Security!)
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        return jsonify({"error": "Course not found"}), 404

    # 2. Razorpay requires the amount in "paise" (multiply INR by 100)
    amount_in_paise = int(course['price'] * 100)

    # 3. Initialize Razorpay Client using keys from config
    client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))

    # 4. Create the order
    order_data = {
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": f"receipt_course_{course_id}"
    }
    
    try:
        order = client.order.create(data=order_data)
        return jsonify({
            "order_id": order['id'],
            "amount": order['amount'],
            "currency": order['currency'],
            "key": current_app.config['RAZORPAY_KEY_ID'],
            "course_name": course['title'],
            "course_desc": course['description']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ==========================================
# 2. VERIFY PAYMENT AND ENROLL
# ==========================================
@enrollment_bp.route('/enroll', methods=['POST'])
def enroll_course():
    data = request.get_json()
    user_id = data.get('user_id')
    course_id = data.get('course_id')
    
    # Payment details sent from frontend after Razorpay popup closes
    razorpay_payment_id = data.get('razorpay_payment_id')
    razorpay_order_id = data.get('razorpay_order_id')
    razorpay_signature = data.get('razorpay_signature')

    # 1. Verify Payment Signature
    client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
    
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except razorpay.errors.SignatureVerificationError:
        return jsonify({"error": "Payment verification failed. Invalid signature."}), 400

    # 2. Prevent duplicate enrollments
    if enrollments_collection.find_one({"user_id": user_id, "course_id": course_id}):
        return jsonify({"error": "You are already enrolled in this course"}), 400

    # 3. Save successful enrollment to database
    new_enrollment = {
        "user_id": user_id,
        "course_id": course_id,
        "payment_id": razorpay_payment_id, # Keep track of the transaction
        "enrolled_at": datetime.utcnow()
    }
    enrollments_collection.insert_one(new_enrollment)

    return jsonify({"message": "Payment successful! Welcome to the course."}), 201

# ==========================================
# 3. GET USER COURSES
# ==========================================
@enrollment_bp.route('/my-courses/<user_id>', methods=['GET'])
def get_user_courses(user_id):
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