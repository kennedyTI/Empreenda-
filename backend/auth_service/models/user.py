# backend/auth_service/models/user.py

from auth_service.db.mongo import db
from passlib.context import CryptContext

# Configura o contexto para hashear/verificar senhas com bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Nome da coleção de usuários no banco
COLLECTION_NAME = "users"

def buscar_usuario_por_email(email: str):
    """
    Busca um usuário real no MongoDB a partir do email.
    Retorna o dicionário do usuário ou None se não existir.
    """
    usuario = db[COLLECTION_NAME].find_one({"email": email})
    return usuario

