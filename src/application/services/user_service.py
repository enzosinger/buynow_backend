from werkzeug.security import generate_password_hash

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, username, password):
        if self.user_repository.find_by_username(username):
            return {'error': 'Usuário já cadastrado!'}

        hashed_password = generate_password_hash(password)
        user_id = self.user_repository.get_next_user_id()

        user = {
            '_id': user_id,
            'username': username,
            'password': hashed_password,
            'compras': 0  # Inicializa o campo "compras" com 0
        }

        self.user_repository.create(user)
        return {'message': 'Usuário criado com sucesso!'}

    def get_all_users(self):
        users = self.user_repository.get_all()
        return [{'id': user['_id'], 'username': user['username'], 'compras': user.get('compras', 0)} for user in users]

    def update_user(self, user_id, username=None, password=None, compras=None):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return {'error': 'Usuário não encontrado!'}

        updated_user = {}

        if username:
            updated_user['username'] = username
        if password:
            updated_user['password'] = generate_password_hash(password)
        if compras is not None:
            updated_user['compras'] = compras

        if updated_user:
            self.user_repository.update(user_id, updated_user)
            return {'message': 'Usuário atualizado com sucesso!'}
        else:
            return {'error': 'Nada para atualizar'}

    def delete_user(self, user_id):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            return {'error': 'Usuário não encontrado!'}

        self.user_repository.delete(user_id)
        return {'message': 'Usuário excluído com sucesso!'}

    def increment_user_purchases(self, user_id):
        user = self.user_repository.find_by_id(user_id)
        if not user:
            print(f"Usuário com ID {user_id} não encontrado.")
            return {"error": "Usuário não encontrado"}

        new_compras_count = user.get("compras", 0) + 1
        self.user_repository.update(user_id, {"compras": new_compras_count})

        print(f"Compras do usuário com ID {user_id} incrementadas para {new_compras_count}.")
        return {"message": "Compras incrementadas com sucesso"}