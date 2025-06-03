# 🚀 Empreenda+ – Plataforma Completa (Backend + Frontend)

Este projeto é a base da plataforma **Empreenda+**, voltada para MEIs e pequenos empreendedores, com funcionalidades como autenticação, painel administrativo, e integração inteligente entre serviços. 

Conta com:
- Backend em **FastAPI** com JWT e MongoDB
- Frontend em **Next.js + Tailwind + TypeScript**
- Totalmente **dockerizado**, preparado para produção em cloud

---

![Tests](https://github.com/kennedyTI/Empreenda-Plus/actions/workflows/backend-tests.yml/badge.svg)

---

## 📦 Estrutura do Projeto

A seguir, a estrutura completa do repositório Empreenda+, com comentários por etapa:

```
Empreenda+/                      # Raiz do projeto fullstack (frontend + backend)
├── frontend/                         # Aplicação web Next.js (institucional + dashboard)
│   ├── Dockerfile                    # Dockerfile para build e execução do frontend
│   ├── public/                       # Arquivos públicos, imagens, favicon, etc.
│   ├── src/                          # Código fonte
│   │   ├── pages/                   # Rotas e páginas (Next.js)
│   │   ├── components/              # Componentes reutilizáveis
│   │   ├── styles/                  # TailwindCSS e estilos globais
│   │   └── ...                      # Outros utilitários e hooks
│   ├── package.json                 # Dependências e scripts do frontend
│   └── tsconfig.json                # Configuração TypeScript
│
├── backend/                          # Backend FastAPI com autenticação e MongoDB
│   ├── __init__.py                   # Torna o diretório backend um pacote Python
│   ├── .env                          # Variáveis de ambiente (nunca commitar)
│   ├── .env.example                  # Exemplo seguro para uso no repositório
│   ├── .gitignore                    # Ignora arquivos sensíveis e temporários
│   ├── Dockerfile                    # Dockerfile com multi-stage para backend
│   ├── docker-compose.yml           # Orquestra backend, frontend e MongoDB
│   ├── requirements.txt             # Dependências fixadas do backend
│   ├── tests/                        # Testes automatizados com pytest
│   │   └── test_auth.py             # Testes de login, signup e JWT
│   ├── .github/
│   │   └── workflows/
│   │       └── backend-tests.yml    # GitHub Actions (CI para backend)
│   └── auth_service/                # Código principal do FastAPI
│       ├── __init__.py
│       ├── main.py                  # Entrada FastAPI
│       ├── db/
│       │   └── mongo.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── login.py
│       │   ├── protected.py
│       │   └── signup.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── token.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── user_service.py
│       └── utils/
│           ├── __init__.py
│           ├── email_service.py
│           ├── i18n.py
│           ├── limiter.py
│           ├── criar_usuario_mock.py
│           ├── security.py
│           ├── verificar_mongodb.py
│           └── update_requirements.py
```

---

## ▶️ Como rodar com Docker

```bash
docker-compose up --build
```

Acesse:
- Frontend: http://localhost:3000
- API Swagger: http://localhost:8000/docs

---

## ✅ Funcionalidades principais (backend)
- Autenticação JWT (login, signup)
- Proteção de rotas via token Bearer
- Integração real com MongoDB
- Criação automática de usuário em dev
- Validações com Pydantic e email-validator
- Internacionalização de mensagens (i18n pt/en)
- Envio de e-mail via SMTP (Gmail/Outlook)
- Rate limiting básico (por IP)
- Testes automatizados com `pytest`

---

## 🧪 Testes

Executar os testes:
```bash
docker-compose exec auth_service pytest
```

Os testes cobrem:
- Login válido e inválido
- Cadastro com e sem falhas
- Proteção contra spam (rate limit)
- Acesso a rota protegida com JWT

---

## 🔒 Segurança e produção

Antes de subir para produção, lembre-se de:

- Proteger suas chaves `.env`, como `JWT_SECRET`, `EMAIL_PASSWORD`, `MONGO_URI`
- Nunca subir `.env` ao GitHub (garantido via `.gitignore`)
- Usar **Docker Secrets**, **AWS Secrets Manager** ou **Vault** para variáveis sensíveis em ambiente cloud
- Ativar HTTPS e autenticação segura em endpoints críticos


- Variáveis de ambiente devem ser protegidas com `Docker Secrets` ou `.env.production`
- Recomendado usar Redis em produção para rate limiting
- MongoDB em nuvem (MongoDB Atlas)

---

## ⚙️ Pré-requisitos

Antes de rodar o projeto, é necessário ter:

- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) [MongoDB Compass](https://www.mongodb.com/products/compass) para visualizar dados
- Acesso ao `.env` local (baseado em `.env.example`)

---

## 📂 MongoDB + Compass (dev)

URI:
```
mongodb://localhost:27018
```
Banco: `OliveiraDevelops`
Coleção: `users`

---

## ⚙️ Variáveis de ambiente (.env exemplo)
```env
ENV=dev
JWT_SECRET=sua_chave_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGO_URI=mongodb://mongodb:27017
MONGO_DB_NAME=OliveiraDevelops
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_de_app
EMAIL_FROM=Empreenda+ <seu_email@gmail.com>
```

---

## 🔁 Atualização automática de dependências
Em ambiente `dev`, o arquivo `requirements.txt` é atualizado automaticamente com `pip freeze` via `update_requirements.py`.

---

## 👥 Sobre o projeto

**Empreenda+** é uma plataforma digital para **MEIs** e microempresários:

- Abertura de CNPJ
- Emissão de notas fiscais
- Alertas de obrigações fiscais
- Integração com parceiros
- IA para atendimento e automação

Desenvolvido com ❤️ em Python e TypeScript, com foco em escalabilidade, segurança e UX.

---

> Para dúvidas técnicas ou sugestões, abra uma issue no repositório ou entre em contato via e-mail profissional.
