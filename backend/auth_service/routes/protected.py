# -*- coding: utf-8 -*-
"""
Rota protegida – acessível apenas com token JWT válido.
"""

from fastapi import APIRouter, Depends
from auth_service.utils.security import get_current_user

router = APIRouter()

@router.get("/protegido")
def rota_protegida(usuario: dict = Depends(get_current_user)):
    """
    Rota protegida por autenticação JWT.

    Parâmetros:
    - Authorization: Bearer <token>

    Retorno:
    {
        "mensagem": "Você acessou uma rota protegida!",
        "usuario": "email@dominio.com"
    }
    """
    return {
        "mensagem": "Você acessou uma rota protegida!",
        "usuario": usuario["email"]
    }
