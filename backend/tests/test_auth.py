# tests/test_auth.py

import sys
import os
from fastapi.testclient import TestClient

# Adiciona o caminho da raiz ao sys.path (necessário dentro do container Docker)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a aplicação FastAPI
from auth_service.main import app

# Cria um cliente de teste para fazer requisições HTTP simuladas
client = TestClient(app)


def test_login_com_dados_invalidos():
    """
    Testa a rota /login com e-mail e senha incorretos.
    Esperado: HTTP 401 (Unauthorized)
    """
    response = client.post(
        "/login",
        data={"username": "usuario@exemplo.com", "password": "senha_errada"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_login_com_dados_validos():
    """
    Testa a rota /login com credenciais válidas.
    Esperado: HTTP 200 e retorno de um token JWT.
    
    ⚠️ Este teste só passará se existir um usuário com:
        username: usuario@exemplo.com
        password: senha123
    """
    response = client.post(
        "/login",
        data={"username": "usuario@exemplo.com", "password": "senha123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
