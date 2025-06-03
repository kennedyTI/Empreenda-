"""
Funções de segurança para autenticação e proteção:
- Hash de senha com bcrypt
- Geração e validação de tokens JWT
- Autenticação via OAuth2
"""

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os

# 🔐 Configuração de hashing seguro
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Leitura obrigatória de variáveis de ambiente (via container)
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
EXPIRES_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

if not SECRET_KEY:
    raise EnvironmentError("❌ JWT_SECRET não definido no ambiente.")

# 🔑 Gera um hash seguro da senha (bcrypt)
def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

# 🔎 Verifica se uma senha corresponde ao hash armazenado
def verificar_senha(senha: str, hash_senha: str):
    return pwd_context.verify(senha, hash_senha)

# 🪪 Gera token JWT com dados e expiração
def criar_token_acesso(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRES_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 🧩 FastAPI: espera token no header Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ✅ Extrai o usuário do token JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
