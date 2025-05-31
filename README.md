# 🚀 Empreenda+ – Auth Service

Este projeto é o serviço de autenticação do sistema Empreenda+, utilizando **FastAPI**, **JWT** e **MongoDB**.

---

## 📦 Estrutura

```
backend/
├── auth_service/
│   ├── main.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   └── user_mock.py
├── docker-compose.yml
└── requirements.txt
```

---

## ⚙️ Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (somente para testes locais fora do Docker)
- MongoDB Compass (opcional, para inspeção visual do banco)

---

## ▶️ Executar o projeto

```bash
docker-compose up --build
```

A API estará disponível em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Criar usuário de teste no MongoDB

```bash
docker-compose exec auth_service python tests/user_mock.py
```

---

## 🔐 Testar a rota de login (/login)

### Acesse a documentação Swagger:
[http://localhost:8000/docs](http://localhost:8000/docs)

### Faça login com:

```
username: usuario@exemplo.com
password: senha123
```

Se tudo estiver correto, a resposta será:

```json
{
  "access_token": "<token.jwt.aqui>",
  "token_type": "bearer"
}
```

---

## 🔒 Testar rotas protegidas com JWT

1. Copie o token da resposta do `/login`
2. Acesse a rota `/protegido` na mesma interface `/docs`
3. Clique em "Authorize", cole o token como:

```
Bearer <seu_token>
```

4. Envie a requisição. A resposta será:

```json
{ "mensagem": "Você acessou uma rota protegida!", "usuario": "usuario@exemplo.com" }
```

---

## 🧪 Rodar testes automatizados (em construção)

```bash
docker-compose exec auth_service pytest
```

---

## 📂 Conectar o MongoDB ao Compass

### String de conexão:
```
mongodb://localhost:27017
```

Banco: `empreendadb`  
Coleção: `users`

---

## 📌 Variáveis de ambiente

No momento, apenas a variável `ENV` é utilizada para ativar a atualização automática do `requirements.txt`:

```env
ENV=dev
```

---

## 🛠️ Requisitos do projeto (`requirements.txt`)

Atualizado automaticamente a cada execução em ambiente de desenvolvimento.

---

## 👥 Contribuição

Este projeto é parte do ecossistema **Empreenda+**, voltado para facilitar a vida do MEI no Brasil.