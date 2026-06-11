# TechSolutions CRM

API e interface web para gerenciamento de clientes da TechSolutions, desenvolvida com FastAPI.

## Tecnologias

- **Python 3.14**
- **FastAPI** — framework web
- **SQLite** — banco de dados local
- **Jinja2** — templates HTML
- **Pydantic** — validação de dados
- **Docker** — containerização

## Estrutura do projeto

```
projeto_fastapi/
├── app/
│   ├── db/
│   │   ├── local.py                  # Conexão com o banco SQLite
│   │   ├── cliente_repository.py     # Operações de clientes no banco
│   │   └── usuario_repository.py     # Operações de usuários no banco
│   ├── models/
│   │   ├── cliente.py                # Models Pydantic de Cliente
│   │   └── usuario.py                # Models Pydantic de Usuário
│   ├── routes/
│   │   ├── cliente.py                # Rotas de clientes (API + front)
│   │   ├── login.py                  # Rota de login
│   │   └── registro.py               # Rota de registro
│   ├── auth_middleware.py            # Middleware de autenticação por cookie
│   ├── dependencies.py               # Injeção de dependências
│   └── main.py                       # Entrada da aplicação
├── templates/                        # HTML com Jinja2
├── static/                           # CSS, JS e assets
├── test/                             # Testes automatizados
├── Dockerfile
├── requirements.txt
└── techlog.db                        # Banco de dados SQLite
```

## Rotas

### Interface web

| Método | Rota            | Descrição                  |
|--------|-----------------|----------------------------|
| GET    | `/`             | Página inicial             |
| GET    | `/login`        | Página de login            |
| POST   | `/login`        | Autenticar usuário         |
| GET    | `/logout`       | Encerrar sessão            |
| GET    | `/registro`     | Página de registro         |
| POST   | `/registro`     | Criar novo usuário         |
| GET    | `/clientes`     | Listar clientes            |
| GET    | `/clientes/novo`| Formulário novo cliente    |
| GET    | `/clientes/{id}`| Formulário editar cliente  |

### API REST

| Método | Rota                   | Descrição              |
|--------|------------------------|------------------------|
| GET    | `/api/clientes`        | Listar clientes        |
| GET    | `/api/clientes/{id}`   | Obter cliente por ID   |
| POST   | `/api/clientes`        | Criar cliente          |
| PUT    | `/api/clientes/{id}`   | Atualizar cliente      |
| DELETE | `/api/clientes/{id}`   | Deletar cliente        |
| GET    | `/health`              | Status da aplicação    |

## Como rodar

### Localmente

```bash
# Criar e ativar o ambiente virtual
python -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn app.main:app --reload
```

Acesse em: `http://localhost:8000`

Documentação automática: `http://localhost:8000/docs`

### Com Docker

```bash
# Build da imagem
docker build -t techsolutions-api .

# Rodar o container
docker run --rm -p 8000:8000 techsolutions-api
```

## Autenticação

O sistema usa **cookie de sessão**. Após o login bem-sucedido, um cookie `session_token` é definido e validado pelo `AuthMiddleware` em todas as rotas protegidas.
