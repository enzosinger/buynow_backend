import os
from pymongo import MongoClient
from bson.objectid import ObjectId

# Conectar ao MongoDB usando a variável de ambiente MONGO_URI
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/buynow_usuarios')
client = MongoClient(mongo_uri)
db = client.get_database()

# Inicializar o contador, se necessário
if db.counters.find_one({'_id': 'usuarios'}) is None:
    db.counters.insert_one({'_id': 'usuarios', 'seq': 0})

# Função para obter o próximo número sequencial
def get_next_user_id():
    counter = db.counters.find_one_and_update(
        {'_id': 'usuarios'},
        {'$inc': {'seq': 1}},
        return_document=True
    )
    return counter['seq']

# Função para criar um novo usuário
def create(user):
    db.usuarios.insert_one(user)

# Função para encontrar um usuário pelo ID
def find_by_id(user_id):
    return db.usuarios.find_one({'_id': user_id})

# Função para encontrar um usuário pelo nome de usuário
def find_by_username(username):
    return db.usuarios.find_one({'username': username})

# Função para obter todos os usuários
def get_all():
    return db.usuarios.find()

# Função para atualizar um usuário pelo ID
def update(user_id, updated_user):
    db.usuarios.update_one({'_id': user_id}, {'$set': updated_user})

# Função para deletar um usuário pelo ID
def delete(user_id):
    db.usuarios.delete_one({'_id': user_id})
