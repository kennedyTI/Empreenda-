# Funções de segurança: hash de senha, geração e validação de tokens JWT

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# Configura o algoritmo de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Lê configurações do .env
SECRET_KEY = os.getenv("JWT_SECRET", "chave_padrao_insegura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Gera hash seguro da senha
def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

# Verifica se a senha fornecida corresponde ao hash armazenado
def verificar_senha(senha: str, hash_senha: str):
    return pwd_context.verify(senha, hash_senha)

# Cria um token JWT com tempo de expiração
def criar_token_acesso(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRES_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# OAuth2 espera o token no header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Extrai e valida o token, retornando o "usuário atual"
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
