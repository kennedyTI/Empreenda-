# backend/auth_service/utils/security.py

from passlib.context import CryptContext
from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuração do hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chave secreta e algoritmo (em produção, use .env)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
EXPIRES_MIN = 30

# Gera hash seguro da senha
def gerar_hash_senha(senha: str):
    return pwd_context.hash(senha)

# Verifica se senha fornecida bate com hash salvo
def verificar_senha(senha: str, hash_senha: str):
    return pwd_context.verify(senha, hash_senha)

# Cria token JWT com tempo de expiração
def criar_token_acesso(dados: dict):
    to_encode = dados.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRES_MIN)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Define o esquema OAuth2 que espera um token Bearer enviado na requisição
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Função que valida o token e extrai o usuário atual
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decodifica o token usando a SECRET_KEY e o ALGORITHM definido
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extrai o e-mail do payload (campo 'sub')
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        # Retorna o "usuário autenticado"
        return {"email": email}
    
    except JWTError:
        # Caso o token seja inválido ou expirado
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")