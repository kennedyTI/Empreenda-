# auth_service/utils/criar_usuario_mock.py

from pymongo import MongoClient
from passlib.context import CryptContext
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("DB_NAME", "empreendadb")
COLLECTION_NAME = "users"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_usuario_mock():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    users = db[COLLECTION_NAME]

    if users.find_one({"email": "usuario@exemplo.com"}):
        print("[i] Usuário de teste já existe.")
        return

    novo_usuario = {
        "nome": "Usuário Teste",
        "email": "usuario@exemplo.com",
        "senha": pwd_context.hash("senha123"),
        "ativo": True
    }

    users.insert_one(novo_usuario)
    print("[✓] Usuário de teste criado com sucesso.")
