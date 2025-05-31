# 🚀 Empreenda+ – Auth Service

Este projeto é o serviço de autenticação do sistema **Empreenda+**, construído com **FastAPI**, **JWT** e **MongoDB**.

---

## 📦 Estrutura do Projeto

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

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) [MongoDB Compass](https://www.mongodb.com/products/compass) para visualizar os dados
- Python 3.11+ (caso queira rodar fora do container, para desenvolvimento e testes)

---

## ▶️ Como rodar o projeto

```bash
docker-compose up --build
```

Acesse a API em:  
📎 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## ✅ Verificação automática de conexão com MongoDB

Ao iniciar o `auth_service`, a conexão com o MongoDB é automaticamente validada.

Você verá no terminal algo como:

```
INFO:root:✅ Conexão com o MongoDB estabelecida com sucesso.
```

---

## 🧪 Criar usuário de teste no MongoDB

```bash
docker-compose exec auth_service python tests/user_mock.py
```

Isso cria um usuário com:

- **Email**: `usuario@exemplo.com`  
- **Senha**: `senha123`

---

## 🔐 Testar rota de login `/login`

### Acesse o Swagger:

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

1. Copie o token retornado do `/login`
2. Vá até `/docs` e clique em **Authorize**
3. Insira o token no formato:

```
Bearer <seu_token>
```

4. Acesse a rota `/protegido`. Resposta esperada:

```json
{
  "mensagem": "Você acessou uma rota protegida!",
  "usuario": "usuario@exemplo.com"
}
```

---

## 🧪 Rodar testes automatizados (em construção)

```bash
docker-compose exec auth_service pytest
```

---

## 📂 Conectar ao MongoDB pelo Compass

```
mongodb://localhost:27017
```

Banco: `empreendadb`  
Coleção: `users`

---

## ⚙️ Variáveis de Ambiente (.env)

Atualmente em desenvolvimento é usada:

```env
ENV=dev
```

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

## 👥 Sobre o projeto

**Empreenda+** é um sistema pensado para simplificar a vida do **MEI brasileiro**, com foco em automação, orientação inteligente e integração com parceiros.

---