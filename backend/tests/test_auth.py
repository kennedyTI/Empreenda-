# tests/test_auth.py

import sys
import os
import time
import uuid
from fastapi.testclient import TestClient

# Adiciona o caminho da raiz ao sys.path (necessário dentro do container Docker)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a aplicação FastAPI
from auth_service.main import app

# Importa o dicionário de controle de SPAM (apenas em dev)
from auth_service.utils.limiter import tentativas_por_ip

# Cria um cliente de teste para simular requisições HTTP
client = TestClient(app)


def reset_spam_control():
    """
    Limpa o controle de SPAM por IP antes de cada teste.
    Necessário para garantir que os testes sejam independentes.
    """
    tentativas_por_ip.clear()


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


def test_signup_com_dados_validos():
    """
    Testa o endpoint /signup com dados válidos.
    Esperado: HTTP 200 e retorno com ID do novo usuário.
    """
    reset_spam_control()
    email_unico = f"teste_{uuid.uuid4().hex[:6]}@exemplo.com"
    response = client.post(
        "/signup",
        json={
            "nome": "Teste Automático",
            "email": email_unico,
            "senha": "senhaSegura123"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["mensagem"] == "Usuário criado com sucesso"


def test_signup_email_duplicado():
    """
    Testa o endpoint /signup com um e-mail que já foi cadastrado.
    Esperado: HTTP 400 com mensagem de erro.
    """
    reset_spam_control()
    email = "duplicado@teste.com"

    # Primeiro cadastro
    response1 = client.post("/signup", json={
        "nome": "Usuário Original",
        "email": email,
        "senha": "senha123"
    })
    assert response1.status_code == 200

    reset_spam_control()  # Limpa antes de novo envio

    # Segundo cadastro com o mesmo e-mail
    response2 = client.post("/signup", json={
        "nome": "Outro Usuário",
        "email": email,
        "senha": "outrasenha456"
    })

    assert response2.status_code == 400
    assert response2.json()["detail"] == "E-mail já cadastrado"


def test_protecao_contra_spam():
    """
    Testa o rate limiting de cadastros consecutivos por IP.
    Esperado: HTTP 429 após exceder o limite.
    """
    reset_spam_control()

    for i in range(5):
        response = client.post("/signup", json={
            "nome": f"Usuário{i}",
            "email": f"spam{i}@teste.com",
            "senha": "senhaForte123"
        })

        if i < 3:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            assert "muitas tentativas" in response.json()["detail"].lower()
