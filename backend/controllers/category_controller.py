# Category Controller

from flask import Blueprint, request, jsonify
from backend.services.supabase_service import SupabaseService

category_controller = Blueprint('category_controller', __name__)
supabase_service = SupabaseService()

@category_controller.route('/categories', methods=['GET'])
def get_categories():
    categories = supabase_service.get_categories()
    return jsonify(categories), 200

@category_controller.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    category = supabase_service.create_category(data)
    return jsonify(category), 201

@category_controller.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.json
    updated_category = supabase_service.update_category(category_id, data)
    return jsonify(updated_category), 200

@category_controller.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    supabase_service.delete_category(category_id)
    return jsonify({'message': 'Category deleted successfully'}), 204