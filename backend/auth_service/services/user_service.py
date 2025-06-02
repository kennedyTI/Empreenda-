# Serviço para manipulação de dados do usuário no MongoDB

from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException
from auth_service.schemas.user import SignupRequest
from auth_service.utils.security import gerar_hash_senha
import os

# Lê as configurações do MongoDB via .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "OliveiraDevelops")

# Conexão com o MongoDB e definição da coleção
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users = db["users"]

def criar_usuario(dados: SignupRequest) -> ObjectId:
    """
    Cria um novo usuário no MongoDB, se o e-mail ainda não existir.

    Parâmetros:
    - dados: SignupRequest com nome, email e senha

    Retorna:
    - ObjectId do novo usuário

    Lança:
    - HTTP 400 se o e-mail já estiver cadastrado
    """
    if users.find_one({"email": dados.email}):
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    novo_usuario = {
        "nome": dados.nome,
        "email": dados.email,
        "senha": gerar_hash_senha(dados.senha),
        "ativo": True
    }

    resultado = users.insert_one(novo_usuario)
    return resultado.inserted_id


def buscar_usuario_por_email(email: str):
    """
    Busca um usuário no MongoDB a partir do e-mail informado.

    Retorna:
    - Dicionário com dados do usuário (ou None se não encontrado)

    Lança:
    - HTTP 500 em caso de falha na consulta
    """
    try:
        return users.find_one({"email": email})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar usuário: {e}")
