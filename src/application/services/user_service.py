from werkzeug.security import generate_password_hash, check_password_hash
from src.infrastructure.database import user_repository


# Função para criar um usuário
def create_user(username, password):
    if user_repository.find_by_username(username):
        return {'error': 'Usuário já cadastrado!'}

    hashed_password = generate_password_hash(password)
    user_id = user_repository.get_next_user_id()

    user = {
        '_id': user_id,
        'username': username,
        'password': hashed_password
    }

    user_repository.create(user)
    return {'message': 'Usuário criado com sucesso!'}


# Função para listar todos os usuários
def get_all_users():
    users = user_repository.get_all()
    return [{'id': user['_id'], 'username': user['username']} for user in users]


# Função para atualizar um usuário
def update_user(user_id, username, password):
    user = user_repository.find_by_id(user_id)
    if not user:
        return {'error': 'Usuário não encontrado!'}

    hashed_password = generate_password_hash(password)
    updated_user = {
        'username': username,
        'password': hashed_password
    }

    user_repository.update(user_id, updated_user)
    return {'message': 'Usuário atualizado com sucesso!'}


# Função para deletar um usuário
def delete_user(user_id):
    user = user_repository.find_by_id(user_id)
    if not user:
        return {'error': 'Usuário não encontrado!'}

    user_repository.delete(user_id)
    return {'message': 'Usuário excluído com sucesso!'}
