# 🚀 Empreenda+ – Auth Service

Este projeto é o serviço de autenticação do sistema **Empreenda+**, construído com **FastAPI**, **JWT** e **MongoDB**.

---

## 📦 Estrutura do Projeto

```
backend/ 
├── auth_service/
│   ├── main.py                        # Entrada principal do FastAPI
│   ├── db/ 
│   │   └── mongo.py                   # Conexão com MongoDB usando .env
│   ├── models/ 
│   │   └── user.py                    # Modelo e busca de usuário
│   ├── routes/ 
│   │   ├── login.py                   # Rota de login
│   │   ├── protected.py               # Rota protegida com JWT
│   │   └── signup.py                  # Rota para cadastro de usuários
│   ├── schemas/
│   │   ├── token.py                   # Schema de resposta de token
│   │   └── user.py                    # Schemas de entrada/saída do usuário
│   ├── services/
│   │   ├── auth.py                    # Lógica de autenticação e geração de token
│   │   └── user_service.py            # Criação e busca de usuários no MongoDB
│   └── utils/
│       ├── criar_usuario_mock.py      # Cria automaticamente usuário fake em dev
│       ├── security.py                # Segurança: hashing e JWT
│       ├── verificar_mongodb.py       # Testa conexão com o MongoDB
│       └── update_requirements 
├── tests/
│   └── test_auth.py
├── .env                               # Variáveis de ambiente
├── docker-compose.yml                 # Orquestração com Docker
├── requirements.txt                   # Dependências Python
├── README.md
```

---

## ⚙️ Pré-requisitos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) [MongoDB Compass](https://www.mongodb.com/products/compass) para visualizar os dados
- Python 3.11+ (para desenvolvimento local com venv)

---

## ▶️ Como rodar o projeto

```bash
docker-compose up --build
```

Acesse a API em:  
📎 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Verificação automática de conexão com MongoDB

A aplicação realiza uma checagem automática ao subir. Se estiver tudo ok:

```
INFO:root:✅ Conexão com o MongoDB estabelecida com sucesso.
```

---

## 🧪 Criar usuário de teste no MongoDB

Ao iniciar em ambiente `dev`, é criado um usuário automaticamente:

- **Email**: `usuario@exemplo.com`  
- **Senha**: `senha123`

---

## 🔐 Testar rota de login `/login`

### Acesse:

📎 [http://localhost:8000/docs](http://localhost:8000/docs)

### Faça login com:

```
username: usuario@exemplo.com
password: senha123
```

Resposta esperada:

```json
{
  "access_token": "<token.jwt.aqui>",
  "token_type": "bearer"
}
```

---

## 🔒 Acessar rota protegida `/protegido`

1. Copie o token JWT obtido no `/login`
2. Vá até `/docs`, clique em **Authorize**
3. Cole:

```
Bearer <seu_token>
```

4. Teste a rota `/protegido`. A resposta será:

```json
{
  "mensagem": "Você acessou uma rota protegida!",
  "usuario": "usuario@exemplo.com"
}
```

---

## 🧪 Rodar testes automatizados (em construção)

Execute os testes com:

```bash
docker-compose exec auth_service pytest
```

Os testes estão em `tests/test_auth.py`, incluindo:

- Login com credenciais inválidas
- Login com credenciais válidas (usuário mock)

---

## 📂 Conectar ao MongoDB pelo Compass

Acesse:

```
mongodb://localhost:28000
```

Banco: `OliveiraDevelops`  
Coleção: `users`

---

## ⚙️ Variáveis de Ambiente (.env)

```env
# Ambiente
ENV=dev

# JWT
JWT_SECRET=minha_chave_secreta_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MongoDB
MONGO_URI=mongodb://mongodb:27017
MONGO_DB_NAME=OliveiraDevelops
```

---

Essa flag ativa a **atualização automática** do `requirements.txt`.

---

## 🛠️ Atualização do requirements.txt

O arquivo `requirements.txt` é atualizado automaticamente em ambiente de desenvolvimento toda vez que o container sobe.

---

## 📌 Notas de segurança

Antes de subir para produção, lembre-se de:

- Proteger suas chaves `.env` e JWT_SECRET
- Usar **Docker Secrets** ou **Vault** para credenciais sensíveis

---
Aqui está um resumo do que foi conquistado:

✅ Etapa 1 – Estrutura inicial do projeto
Criada a estrutura de diretórios: auth_service/, routes/, models/, services/, utils/, tests/

Criado o Dockerfile e docker-compose.yml

Definido o padrão de projeto baseado em FastAPI

Comando de inicialização via uvicorn

Ambiente com reload para desenvolvimento

✅ Etapa 2 – Rota de login com JWT
Implementada a rota POST /login

Utilizado OAuth2PasswordRequestForm para receber username e password

Criado o esquema TokenResponse

Implementada a função autenticar_usuario com validação de senha

Criado utils/security.py com:

verificar_senha

criar_token_acesso

gerar_hash_senha

JWT gerado com python-jose

✅ Etapa 3 – Proteção de rotas com JWT
Criada a rota /protegido acessível apenas com token válido

Implementado Depends(get_current_user) para validar o JWT

Testes via Swagger UI (/docs) com Bearer <token>

Autenticação funcionando fim a fim: MongoDB → Validação → JWT

✅ Etapa 4 – Integração real com MongoDB
Substituição do usuário fake por consulta real no banco

Banco MongoDB containerizado e persistente

Script `criar_usuario_mock.py` executado automaticamente

Acesso funcional via MongoDB Compass

Implementado verificador automático de conexão:

Executado no startup_event do FastAPI

Lê variáveis de ambiente

Usa pymongo com timeout controlado

requirements.txt atualizado dinamicamente

Organização e importações corrigidas e comentadas

Conexão com MongoDB real

Conexão validada na inicialização do serviço

Compass acessando MongoDB containerizado

### 👤 Etapa 5 – Registro real de usuários

- Rota `/signup` funcional
- Dados persistidos no MongoDB
- Login usando credenciais reais


🎁 Extras
README.md completo e formatado com instruções de uso

Projeto inteiramente funcional via Docker Compose

Código totalmente comentado

Preparação para boas práticas futuras:

Uso de .env para variáveis sensíveis

Planejamento para Docker Secrets na produção

---

Testes automatizados em estrutura pronta (tests/)
## 👥 Sobre o projeto

**Empreenda+** é um sistema pensado para simplificar a vida do **MEI brasileiro**, com foco em automação, orientação inteligente e integração com parceiros.

- Abertura de CNPJ
- Emissão de NF
- Alertas fiscais
- Atendimento automatizado com IA

---

Feito com ❤️ e Python.