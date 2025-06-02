# tests/test_auth.py

import sys
import os
import uuid
from fastapi.testclient import TestClient

# Garante que a raiz do projeto esteja no sys.path (necessário dentro do container Docker)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa a aplicação principal do FastAPI
from auth_service.main import app

# Importa o controle temporário de SPAM por IP (usado nos testes)
from auth_service.utils.limiter import tentativas_por_ip

# Cliente de teste para simular requisições HTTP
client = TestClient(app)

def reset_spam_control():
    """
    Reseta o controle de tentativas por IP (proteção contra spam).
    Necessário antes de cada teste para garantir independência entre eles.
    """
    tentativas_por_ip.clear()

def test_login_com_dados_invalidos():
    """
    Testa a rota /login com credenciais incorretas.
    Esperado: HTTP 401 (não autorizado).
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
            "senha": "senhaSegura123",
            "confirmar_senha": "senhaSegura123"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "id" in body
    assert body["mensagem"].lower().startswith("usuário") or body["mensagem"].lower().startswith("user")

def test_signup_email_duplicado():
    """
    Testa o endpoint /signup com um e-mail que já foi cadastrado.
    Esperado: HTTP 400 com mensagem de erro.
    """
    reset_spam_control()
    email = f"duplicado_{uuid.uuid4().hex[:6]}@teste.com"

    # Primeiro cadastro
    response1 = client.post("/signup", json={
        "nome": "Usuário Original",
        "email": email,
        "senha": "senha123",
        "confirmar_senha": "senha123"
    })
    assert response1.status_code == 200

    reset_spam_control()

    # Segundo cadastro com o mesmo e-mail
    response2 = client.post("/signup", json={
        "nome": "Outro Usuário",
        "email": email,
        "senha": "outrasenha456",
        "confirmar_senha": "outrasenha456"
    })
    assert response2.status_code == 400
    assert "email" in str(response2.json()).lower()

def test_protecao_contra_spam():
    """
    Testa a proteção contra múltiplos cadastros consecutivos por IP.
    Esperado: HTTP 429 após exceder o limite.
    """
    reset_spam_control()

    for i in range(5):
        response = client.post("/signup", json={
            "nome": f"Usuário{i}",
            "email": f"spam{i}_{uuid.uuid4().hex[:4]}@teste.com",
            "senha": "senhaForte123",
            "confirmar_senha": "senhaForte123"
        })
        if i < 3:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
            assert "muitas tentativas" in str(response.json()).lower()

def test_signup_email_invalido():
    """
    Testa o cadastro com e-mail inválido.
    Esperado: HTTP 422 (Unprocessable Entity) ou 400 com mensagem de erro.
    """
    reset_spam_control()
    response = client.post("/signup", json={
        "nome": "Usuário Inválido",
        "email": "email_invalido",
        "senha": "senhaValida123",
        "confirmar_senha": "senhaValida123"
    })
    assert response.status_code in [400, 422]
    assert "email" in str(response.json()).lower()

def test_signup_senhas_diferentes():
    """
    Testa o cadastro com senhas diferentes.
    Esperado: HTTP 422 ou 400 com mensagem de erro indicando senhas divergentes.
    """
    reset_spam_control()
    response = client.post("/signup", json={
        "nome": "Usuário Inconsistente",
        "email": "teste_senha_diferente@exemplo.com",
        "senha": "senha123",
        "confirmar_senha": "outraSenha"
    })
    assert response.status_code in [400, 422]
    assert "senhas" in str(response.json()).lower()

def test_rota_protegida_sem_token():
    """
    Testa o acesso à rota /protegido sem fornecer um token JWT.
    Esperado: HTTP 401 (Unauthorized)
    """
    response = client.get("/protegido")
    assert response.status_code == 401
    assert "token" in str(response.json()).lower()

def test_rota_protegida_com_token_valido():
    """
    Testa o acesso à rota /protegido com um token JWT válido.
    Esperado: HTTP 200 e retorno com email do usuário.
    """
    reset_spam_control()

    # Cria usuário para obter token
    email = f"token_{uuid.uuid4().hex[:6]}@exemplo.com"
    senha = "senhaForte123"

    client.post("/signup", json={
        "nome": "Usuário Token",
        "email": email,
        "senha": senha,
        "confirmar_senha": senha
    })

    # Login
    response_login = client.post(
        "/login",
        data={"username": email, "password": senha},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response_login.status_code == 200
    token = response_login.json()["access_token"]

    # Acessa rota protegida
    response_protegido = client.get("/protegido", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response_protegido.status_code == 200
    assert "mensagem" in response_protegido.json()
    assert "usuario" in response_protegido.json()
