import os
from pymongo import MongoClient
from src.core.interfaces import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://buynowadmin:Enzosinger123!@buynow.fddwc.mongodb.net/?retryWrites=true&w=majority&appName=buynow')
        client = MongoClient(mongo_uri)
        self.db = client.get_database('buynow')  # Nome do banco de dados no Atlas

        # Inicializar o contador, se necessário
        if self.db.counters.find_one({'_id': 'usuarios'}) is None:
            self.db.counters.insert_one({'_id': 'usuarios', 'seq': 0})

    def get_next_user_id(self):
        counter = self.db.counters.find_one_and_update(
            {'_id': 'usuarios'},
            {'$inc': {'seq': 1}},
            return_document=True
        )
        return counter['seq']

    def create(self, user):
        self.db.usuarios.insert_one(user)

    def find_by_id(self, user_id):
        return self.db.usuarios.find_one({'_id': user_id})

    def find_by_username(self, username):
        return self.db.usuarios.find_one({'username': username})

    def get_all(self):
        return self.db.usuarios.find()

    def update(self, user_id, updated_user):
        self.db.usuarios.update_one({'_id': user_id}, {'$set': updated_user})

    def delete(self, user_id):
        self.db.usuarios.delete_one({'_id': user_id})
