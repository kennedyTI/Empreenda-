# backend/auth_service/routes/protected.py

from fastapi import APIRouter, Depends
from auth_service.utils.security import get_current_user

# Cria um novo router para rotas protegidas
router = APIRouter()

# Rota protegida por token JWT
@router.get("/protected")
def rota_protegida(usuario=Depends(get_current_user)):
    """
    Rota protegida por autenticação JWT.
    Requer token válido no header Authorization: Bearer <token>
    """
    return {"mensagem": f"Acesso liberado para {usuario['email']}"}
