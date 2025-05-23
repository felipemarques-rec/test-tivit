# Teste Tivit API

API desenvolvida para o teste técnico da Tivit com autenticação JWT segura e integração com serviços externos, seguindo princípios de Clean Architecture e SOLID.

## 🚀 Características Principais

- **🔐 Autenticação JWT Segura**: Proteção contra ataques de timing e role tampering
- **👥 Controle de Acesso**: Rotas protegidas com diferentes níveis de permissão (user/admin)
- **🌐 Integração Externa**: Consumo de APIs externas com armazenamento em banco de dados
- **🏗️ Arquitetura Limpa**: Implementação seguindo princípios SOLID e Clean Architecture
- **🐳 Docker**: Containerização completa com PostgreSQL
- **🧪 Testes**: Suite de testes automatizados
- **✅ Validações**: Validação de entrada de dados com Pydantic

## 🛡️ Melhorias de Segurança Implementadas

### Proteção contra Role Tampering
- Hash de integridade para roles no JWT
- Validação de roles usando comparação segura com `secrets.compare_digest()`
- Verificação de integridade a cada validação de token

### Proteção contra Timing Attacks
- Operação de hash sempre executada mesmo para usuários inexistentes
- Tempo de resposta consistente independente da existência do usuário

### JWT Seguro
- Claims padrão: `iss` (issuer), `aud` (audience), `jti` (JWT ID)
- Tokens com expiração configurável
- Validação rigorosa de audience e issuer

### Senhas Seguras
- Hash usando o bcrypt
- A senha não está armazenadas em texto plano

## 🏗️ Arquitetura

O projeto segue **Clean Architecture** com separação clara de responsabilidades:

```
app/
├── domain/                    # Camada de Domínio
│   ├── entities/             # Entidades de negócio
│   ├── repositories/         # Interfaces dos repositórios
│   └── use_cases/           # Casos de uso
├── infrastructure/           # Camada de Infraestrutura
│   └── repositories/        # Implementações dos repositórios
├── core/                    # Configurações e segurança
├── schemas/                 # DTOs e validações
├── services/               # Serviços externos
├── dependencies/           # Injeção de dependências
├── routers/               # Controllers/Endpoints
└── models/               # Modelos do banco de dados
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**: Framework web moderno e rápido
- **PostgreSQL**: Banco de dados relacional
- **SQLAlchemy**: ORM para Python
- **JWT**: Autenticação baseada em tokens
- **Pydantic**: Validação de dados
- **Docker & Docker Compose**: Containerização
- **Pytest**: Framework de testes
- **Bcrypt**: Hash seguro de senhas

## 📋 Usuários Fictícios

Conforme especificado no teste:

```python
{
    "usuario": {
        "username": "usuario",
        "role": "user",
        "password": "L0XuwPOdS5U"
    },
    "admin": {
        "username": "admin",
        "role": "admin", 
        "password": "JKSipm0YH"
    }
}
```

## 🌐 Endpoints da API

### Autenticação
- `POST /auth/token` - Autenticação com form data (OAuth2)
- `POST /auth/token-json` - Autenticação com JSON
- `POST /auth/login` - Login com resposta detalhada

### Rotas Protegidas
- `GET /user` - Acessível apenas para usuários com role "user"
- `GET /admin` - Acessível apenas para usuários com role "admin"
- `GET /health` - Health check (requer autenticação)
- `GET /profile` - Perfil do usuário atual

### Endpoints Públicos
- `GET /` - Informações da API
- `GET /health` - Health check público
- `GET /info` - Informações detalhadas da API

## 🚀 Instalação e Execução

### Pré-requisitos

- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)

### Execução Rápida com Script

```bash
# Tornar o script executável
chmod +x run.sh

# Ver comandos disponíveis
./run.sh help

# Executar com Docker (Recomendado)
./run.sh docker

# Ou configurar ambiente local
./run.sh setup
./run.sh dev
```

A API estará disponível em `http://localhost:8000`

## 📖 Uso da API

### 1. Obter Token de Autenticação

```bash
curl -X POST "http://localhost:8000/auth/token-json" \
     -H "Content-Type: application/json" \
     -d '{"username": "usuario", "password": "L0XuwPOdS5U"}'
```

### 2. Acessar Rota Protegida

```bash
curl -X GET "http://localhost:8000/user" \
     -H "Authorization: Bearer <seu-token-aqui>"
```

### 3. Acessar Rota Admin

```bash
curl -X GET "http://localhost:8000/admin" \
     -H "Authorization: Bearer <token-admin-aqui>"
```

### 4. Ver Perfil do Usuário

```bash
curl -X GET "http://localhost:8000/profile" \
     -H "Authorization: Bearer <seu-token-aqui>"
```

## 📚 Documentação da API

Após executar a aplicação, acesse:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testes

### Executar Testes

```bash
# Com script
./run.sh test

# Com Docker
docker-compose exec api pytest

# Localmente
pytest -v
```

### Cobertura de Testes

```bash
pytest --cov=app tests/
```

## 🔗 Integração com APIs Externas

A aplicação consome os seguintes endpoints externos:

- `GET https://api-onecloud.multicloud.tivit.com/fake/health`
- `GET https://api-onecloud.multicloud.tivit.com/fake/user`
- `GET https://api-onecloud.multicloud.tivit.com/fake/admin`
- `POST https://api-onecloud.multicloud.tivit.com/fake/token`

Todos os dados consumidos são armazenados no banco de dados PostgreSQL.

## 🔒 Segurança

### Recursos de Segurança Implementados

- **JWT Seguro**: Tokens com claims padrão e validação rigorosa
- **Hash de Senhas**: Bcrypt com salt automático
- **Proteção contra Timing Attacks**: Tempo de resposta consistente
- **Validação de Integridade**: Hash de roles para prevenir tampering
- **Validação de Entrada**: Pydantic com validadores customizados
- **CORS Configurável**: Configurado para desenvolvimento
- **Logs de Segurança**: Logging de tentativas de acesso

## 🌍 Variáveis de Ambiente

```env
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/teste_tivit
EXTERNAL_API_BASE_URL=https://api-onecloud.multicloud.tivit.com/fake
```

## 🐳 Docker

### Estrutura dos Containers

- **API**: Aplicação FastAPI
- **PostgreSQL**: Banco de dados
- **Volumes**: Persistência de dados

### Comandos Docker Úteis

```bash
# Ver logs da API
docker-compose logs teste_tivit_api

# Ver logs do banco
docker-compose logs postgres

# Executar comando no container da API
docker-compose exec teste_tivit_api bash

# Parar todos os containers
docker-compose down

# Limpar volumes
docker-compose down -v
```