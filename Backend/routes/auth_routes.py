from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import users_collection

auth_bp = Blueprint('auth_routes', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if users_collection.find_one({"email": data.get('email')}):
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data.get('password'))
    
    new_user = {
        "full_name": data.get('full_name'),
        "email": data.get('email'),
        "password_hash": hashed_password,
        "role": "student"
    }
    
    users_collection.insert_one(new_user)
    return jsonify({"message": "User registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data.get('email')})
    
    if user and check_password_hash(user['password_hash'], data.get('password')):
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": str(user['_id']),
                "full_name": user['full_name'],
                "email": user['email'],
                "role": user['role']
            }
        }), 200
    
    return jsonify({"error": "Invalid email or password"}), 401