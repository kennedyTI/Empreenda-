# 🚀 Empreenda+ – Auth Service

Este projeto é o serviço de autenticação do sistema **Empreenda+**, construído com **FastAPI**, **JWT** e **MongoDB**.

---

## 📦 Estrutura do Projeto

```
backend/ 
├── auth_service/
│   ├── main.py ✅                         # Entrada principal do FastAPI
│   ├── db/ ✅
│   │   └── mongo.py ✅                    # Conexão com MongoDB usando .env
│   ├── models/ ✅
│   │   └── user.py ✅                     # Modelo e busca de usuário
│   ├── routes/ ✅
│   │   ├── login.py ✅                    # Rota de login
│   │   ├── protected.py ✅                # Rota protegida com JWT
│   │   └── signup.py ✅                  # Rota para cadastro de usuários
│   ├── schemas/ ✅
│   │   ├── token.py ✅                    # Schema de resposta de token
│   │   └── user.py ✅                     # Schemas de entrada/saída do usuário
│   ├── services/ ✅
│   │   ├── auth.py ✅                     # Lógica de autenticação e geração de token
│   │   └── user_service.py ✅            # Criação e busca de usuários no MongoDB
│   └── utils/
│       ├── criar_usuario_mock.py ✅      # Cria automaticamente usuário fake em dev
│       ├── email_service
│       ├── i18n
│       ├──limiter
│       ├── security.py ✅                # Segurança: hashing e JWT
│       ├── verificar_mongodb.py ✅      # Testa conexão com o MongoDB
│       └── update_requirements ✅ 
├── tests/✅
│   └── test_auth.py ✅
├── .env ✅                           # Variáveis de ambiente
├── docker-compose.yml ✅                 # Orquestração com Docker
├── dockerfile
├── requirements.txt ✅                   # Dependências Python
├── README.md ✅
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

✅ ETAPAS JÁ CONCLUÍDAS

✅ Etapa 1 – Estrutura Inicial do Projeto

Estrutura de pastas organizada (auth_service/, routes/, models/, services/, utils/, tests/)

Uso de Docker + Docker Compose

Configuração de ambiente com .env e reload automático com uvicorn

✅ Etapa 2 – Login com JWT

Rota /login funcional

Autenticação via OAuth2PasswordRequestForm

Senhas com hash bcrypt

Geração de tokens JWT com tempo de expiração

Schema de resposta TokenResponse

✅ Etapa 3 – Proteção de Rotas

Rota protegida /protegido

Autenticação via Bearer Token

Dependência de segurança get_current_user

Verificação do token e retorno do usuário

✅ Etapa 4 – Integração Real com MongoDB

Substituição de usuários fake por persistência real

MongoDB funcional com volume Docker (mongodb)

Criação automática de usuário de teste (criar_usuario_mock.py)

Conexão validada automaticamente no startup (verificar_conexao_mongodb)

Compass conectado com banco containerizado

✅ Etapa 5 – Cadastro Real de Usuários

Rota /signup funcional com persistência no MongoDB

Esquema SignupRequest validando os dados

Proteção contra e-mails duplicados

Testes automatizados para /signup:

Cadastro válido

E-mail duplicado

Proteção contra SPAM por IP

Controle de IP temporário (rate limit por IP)

Logs para facilitar debug

Observação registrada para uso de Redis no futuro em produção

Atualização automática do requirements.txt

Venv configurado com activate_hook

🎁 Extras

Logs informativos no terminal

requirements.txt atualizado automaticamente apenas no ambiente dev

Observação sobre @app.on_event("startup") marcada para futura migração para lifespan

README.md completo e comentado

Proteção mínima contra SPAM funcional

---

Testes automatizados em estrutura pronta (tests/)
## 👥 Sobre o projeto

**Empreenda+** é um sistema pensado para simplificar a vida do **MEI brasileiro**, com foco em automação, orientação inteligente e integração com parceiros.

- Abertura de CNPJ
- Emissão de NF
- Alertas fiscais
- Atendimento automatizado com IA

---

Feito com ❤️ e Python...
