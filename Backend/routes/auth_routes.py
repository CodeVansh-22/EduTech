from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.db import users_collection

auth_bp = Blueprint('auth_routes', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if users_collection.find_one({"email": data.get('email')}):
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(data.get('password'))
    
    # Grab the role from the frontend, default to 'student'
    role = data.get('role', 'student') 
    
    new_user = {
        "full_name": data.get('full_name'),
        "email": data.get('email'),
        "password_hash": hashed_password,
        "role": role  # Save the role to MongoDB
    }
    
    users_collection.insert_one(new_user)
    return jsonify({"message": f"{role.capitalize()} registered successfully!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data.get('email')})
    
    if user and check_password_hash(user['password_hash'], data.get('password')):
        
        # --- THE FIX: Save data to Flask Session ---
        session['user_id'] = str(user['_id'])
        session['role'] = user.get('role', 'student')
        
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": str(user['_id']),
                "full_name": user['full_name'],
                "email": user['email'],
                "role": user.get('role', 'student') 
            }
        }), 200
    
    return jsonify({"error": "Invalid email or password"}), 401

# --- ADDED LOGOUT ROUTE ---
@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() # Clears the Flask session
    return jsonify({"message": "Logged out successfully"}), 200