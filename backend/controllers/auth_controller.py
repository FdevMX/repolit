from flask import Blueprint, request, jsonify
from backend.services.supabase_service import SupabaseService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Logic for authenticating user
    user = SupabaseService.authenticate_user(email, password)
    
    if user:
        return jsonify({"message": "Login successful", "user": user}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    # Logic for registering user
    new_user = SupabaseService.register_user(email, password)
    
    if new_user:
        return jsonify({"message": "Registration successful", "user": new_user}), 201
    else:
        return jsonify({"message": "Registration failed"}), 400