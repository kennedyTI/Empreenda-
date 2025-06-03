"""
Modelo de acesso à coleção de usuários no MongoDB.
"""

from auth_service.db.mongo import db

COLLECTION_NAME = "users"

def buscar_usuario_por_email(email: str):
    """
    Busca um usuário pelo e-mail.

    Args:
        email (str): e-mail a consultar

    Returns:
        dict | None: usuário encontrado
    """
    return db[COLLECTION_NAME].find_one({"email": email})
