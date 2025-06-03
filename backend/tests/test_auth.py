"""
Testes automatizados para autenticação da API Empreenda+.
Inclui testes para login, cadastro, proteção contra spam e acesso com JWT.
Executado automaticamente via GitHub Actions e localmente via pytest.
"""

import sys
import os
import uuid
from fastapi.testclient import TestClient

# ✅ Garante que o path funcione dentro do container
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ✅ Importa a aplicação principal e os utilitários
from auth_service.main import app
from auth_service.utils.limiter import tentativas_por_ip

# 🧪 Cliente de teste para simular chamadas HTTP REST
client = TestClient(app)

def reset_spam_control():
    """
    Limpa o controle de rate limit por IP para evitar interferência entre testes.
    """
    tentativas_por_ip.clear()

def test_login_com_dados_invalidos():
    response = client.post(
        "/login",
        data={"username": "usuario@exemplo.com", "password": "senha_errada"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert "access_token" not in response.json()

def test_signup_com_dados_validos():
    reset_spam_control()
    email = f"teste_{uuid.uuid4().hex[:6]}@exemplo.com"
    response = client.post("/signup", json={
        "nome": "Teste Automático",
        "email": email,
        "senha": "senhaSegura123",
        "confirmar_senha": "senhaSegura123"
    })
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert "usuário" in body["mensagem"].lower() or "user" in body["mensagem"].lower()

def test_signup_email_duplicado():
    reset_spam_control()
    email = f"duplicado_{uuid.uuid4().hex[:6]}@teste.com"
    client.post("/signup", json={
        "nome": "Usuário Original",
        "email": email,
        "senha": "senha123",
        "confirmar_senha": "senha123"
    })
    reset_spam_control()
    response = client.post("/signup", json={
        "nome": "Outro",
        "email": email,
        "senha": "outrasenha456",
        "confirmar_senha": "outrasenha456"
    })
    assert response.status_code == 400
    assert "email" in str(response.json()).lower()

def test_protecao_contra_spam():
    reset_spam_control()
    for i in range(5):
        response = client.post("/signup", json={
            "nome": f"SpamUser{i}",
            "email": f"spam_{uuid.uuid4().hex[:5]}@teste.com",
            "senha": "senha123456",
            "confirmar_senha": "senha123456"
        })
        if i < 3:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            assert "muitas tentativas" in str(response.json()).lower()

def test_signup_email_invalido():
    reset_spam_control()
    response = client.post("/signup", json={
        "nome": "Invalido",
        "email": "email_invalido",
        "senha": "senhaValida123",
        "confirmar_senha": "senhaValida123"
    })
    assert response.status_code in [400, 422]
    assert "email" in str(response.json()).lower()

def test_signup_senhas_diferentes():
    reset_spam_control()
    response = client.post("/signup", json={
        "nome": "Senhas Divergentes",
        "email": "senhas_dif@exemplo.com",
        "senha": "senha123",
        "confirmar_senha": "outraSenha"
    })
    assert response.status_code in [400, 422]
    assert "senhas" in str(response.json()).lower()

def test_rota_protegida_sem_token():
    response = client.get("/protegido")
    assert response.status_code == 401
    assert "token" in str(response.json()).lower()

def test_rota_protegida_com_token_valido():
    reset_spam_control()
    email = f"token_{uuid.uuid4().hex[:6]}@exemplo.com"
    senha = "senhaForte123"

    client.post("/signup", json={
        "nome": "Token",
        "email": email,
        "senha": senha,
        "confirmar_senha": senha
    })

    login_response = client.post("/login", data={
        "username": email,
        "password": senha
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    protegido_response = client.get("/protegido", headers={
        "Authorization": f"Bearer {token}"
    })
    assert protegido_response.status_code == 200
    assert "mensagem" in protegido_response.json()
    assert "usuario" in protegido_response.json()
