from flask import Blueprint, request, jsonify
from src.application.services.user_service import UserService
from src.infrastructure.database.user_repository import UserRepository
from src.infrastructure.messaging.service_bus_client import send_product_purchase_event

user_controller = Blueprint('user_controller', __name__)
user_service = UserService(UserRepository())

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
    compras = data.get('compras')

    # Verificar se pelo menos um dos campos foi fornecido
    if not username and not password and compras is None:
        return jsonify({'error': 'Username, password, or compras must be provided'}), 400

    # Chamar o serviço para atualização
    result = user_service.update_user(user_id, username, password, compras)
    if 'error' in result:
        return jsonify(result), 404

    return jsonify(result), 200

@user_controller.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = user_service.delete_user(user_id)
    return jsonify(result), (200 if 'message' in result else 404)


@user_controller.route('/users/<int:user_id>/comprar', methods=['POST'])
def process_purchase(user_id):
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'O campo product_id é obrigatório'}), 400

    # Chamar o envio do evento para o Service Bus com o user_id e product_id
    send_product_purchase_event(product_id, user_id)

    return jsonify({"message": f"Evento de compra do produto {product_id} enviado com sucesso e compras do usuário incrementadas."}), 200