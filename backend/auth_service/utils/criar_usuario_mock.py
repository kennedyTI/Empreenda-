"""
Cria automaticamente um usuário fake para testes locais.
⚠️ Usado apenas em ambiente de desenvolvimento (ENV=dev).
"""

from pymongo import MongoClient
from passlib.context import CryptContext
import os

# ⚙️ Configurações lidas do ambiente do container
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = "users"

if not MONGO_URI or not DB_NAME:
    raise EnvironmentError("❌ Variáveis de ambiente MONGO_URI ou MONGO_DB_NAME não definidas.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_usuario_mock():
    """
    Cria um usuário de teste se ainda não existir no banco.
    Email: usuario@exemplo.com
    Senha: senha123
    """
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
