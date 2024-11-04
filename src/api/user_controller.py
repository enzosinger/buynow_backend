from flask import Blueprint, request, jsonify
from src.application.services import user_service

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    result = user_service.create_user(username, password)
    return jsonify(result), (201 if 'message' in result else 400)

@user_controller.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_all_users()
    return jsonify(users), 200

@user_controller.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    result = user_service.update_user(user_id, username, password)
    return jsonify(result), (200 if 'message' in result else 404)

@user_controller.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_service.delete_user(user_id)
    return jsonify(result), (200 if 'message' in result else 404)
