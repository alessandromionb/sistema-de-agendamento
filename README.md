# AgendaPro — Sistema de Agendamentos

> Aplicação conteinerizada com Docker Compose: NGINX · FastAPI · MySQL

---

## Integrantes

| Nome | Matrícula |
|------|-----------|
| _(preencha)_ | _(preencha)_ |
| _(preencha)_ | _(preencha)_ |

## Tema

**Sistema de Agendamentos** — gerenciamento de clientes e seus agendamentos de serviços.

---

## Arquitetura

```
Host (porta 80/443)
        │
      NGINX  ──── /          → frontend estático (HTML/CSS/JS)
        │    ──── /api/*     → FastAPI (porta 8080, rede interna)
        │                           │
        │                       MySQL (rede interna, volume persistente)
```

### Rede e containers

| Container | Imagem | Porta interna | Exposta no host |
|-----------|--------|---------------|-----------------|
| `nginx_agendamentos` | nginx:1.25-alpine | 8080, 8443 | 80, 443 |
| `fastapi_agendamentos` | build local | 8080 | — |
| `mysql_agendamentos` | mysql:8.0 | 3306 | — |

Todos os serviços compartilham a rede `netatividade01`.

---

## Pré-requisitos

- Docker ≥ 24
- Docker Compose ≥ 2.20

---

## Como subir a aplicação

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/sistema-agendamentos.git
cd sistema-agendamentos

# 2. Edite o arquivo .env com a matrícula de um integrante como senha
#    MYSQL_PASSWORD=20241234567
nano .env

# 3. Suba toda a topologia com um único comando
docker compose up --build -d

# 4. Acesse no navegador
#    Frontend:      http://localhost
#    Docs FastAPI:  http://localhost/api/docs
```

Para derrubar:
```bash
docker compose down          # mantém o volume do banco
docker compose down -v       # destrói o volume também
```

---

## Estrutura do projeto

```
sistema-agendamentos/
├── docker-compose.yml
├── .env
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py          # ponto de entrada FastAPI
│       ├── database.py      # engine SQLAlchemy + settings
│       ├── models.py        # ORM: Cliente, Agendamento
│       ├── routes/
│       │   ├── __init__.py  # reexporta clientes_router, agendamentos_router
│       │   ├── clientes.py
│       │   └── agendamentos.py
│       └── schemas/
│           ├── __init__.py  # reexporta todos os schemas
│           ├── cliente.py
│           └── agendamento.py
└── nginx/
    ├── nginx.conf
    └── html/
        ├── index.html
        ├── style.css
        └── script.js
```

---

## Endpoints da API

### Clientes

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/clientes/` | Lista todos os clientes |
| GET | `/api/clientes/{id}` | Busca cliente por ID |
| POST | `/api/clientes/` | Cria novo cliente |
| PUT | `/api/clientes/{id}` | Atualiza cliente |
| DELETE | `/api/clientes/{id}` | Remove cliente |

### Agendamentos

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/agendamentos/` | Lista agendamentos (filtrável por `?status=`) |
| GET | `/api/agendamentos/{id}` | Busca agendamento por ID |
| POST | `/api/agendamentos/` | Cria novo agendamento |
| PUT | `/api/agendamentos/{id}` | Atualiza agendamento |
| DELETE | `/api/agendamentos/{id}` | Remove agendamento |

---

## Exemplos de uso (curl)

```bash
# Criar cliente
curl -X POST http://localhost/api/clientes/ \
  -H "Content-Type: application/json" \
  -d '{"nome":"João Silva","email":"joao@email.com","telefone":"(27) 99999-0001"}'

# Listar clientes
curl http://localhost/api/clientes/

# Criar agendamento
curl -X POST http://localhost/api/agendamentos/ \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": 1,
    "servico": "Corte de cabelo",
    "data_hora": "2025-06-15T14:00:00",
    "status": "pendente"
  }'

# Atualizar status do agendamento
curl -X PUT http://localhost/api/agendamentos/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "confirmado"}'

# Remover agendamento
curl -X DELETE http://localhost/api/agendamentos/1

# Documentação interativa (Swagger)
# Acesse: http://localhost/api/docs
```

---

## Variáveis de ambiente (`.env`)

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `MYSQL_USER` | Usuário do banco | `agendamento` |
| `MYSQL_PASSWORD` | Senha — usar matrícula de integrante | _(obrigatório)_ |
| `MYSQL_DATABASE` | Nome do banco | `agendamentos_db` |