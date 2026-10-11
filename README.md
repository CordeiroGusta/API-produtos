# 🚀 API-produtos *(Branch: sandbox/database)*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/FastAPI-0.141.1-009688?style=for-the-badge&logo=fastapi&logoColor=white">
  <img src="https://img.shields.io/badge/MariaDB-003545?style=for-the-badge&logo=mariadb&logoColor=white">
  <img src="https://img.shields.io/badge/Docker Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white">
  <img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white">
</p>

---

## 📌 Sobre esta Branch (Sandbox)

Esta branch faz parte de um estudo prático de evolução arquitetural. O projeto original (que utilizava armazenamento em memória/local) foi refatorado para integrar uma **base de dados relacional real (MariaDB)** executada em um container isolado via **Docker Compose**.

O objetivo desta etapa é validar:
- A configuração de containers para o ambiente de desenvolvimento local;
- A conexão da aplicação FastAPI com o banco de dados;
- A adaptação da camada de **Repositories** para persistência relacional.

---

## 🏗️ Arquitetura da aplicação

A aplicação mantém sua divisão estrita de responsabilidades, agora conectando a camada de persistência a um banco relacional externo.

```text
                         ┌──────────────────┐
                         │     CLIENTE      │
                         │ Postman / HTTP   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     ROUTERS      │
                         │ Endpoints / HTTP │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     SCHEMAS      │
                         │ Pydantic / Dados │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     SERVICES     │
                         │ Regras de negócio│
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   REPOSITORIES   │
                         │ Consultas / SQL  │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     MARIADB      │
                         │ (Docker Compose) │
                         └──────────────────┘
```

---

# 🛠️ Tecnologias utilizadas (Atualizada)

| Tecnologia | Utilização |
|---|---|
| 🐍 **Python** | Linguagem principal |
| ⚡ **FastAPI** | Desenvolvimento da API REST |
| 🦭 **MariaDB (v10.11)** | Banco de dados relacional |
| 🐳 **Docker / Compose** | Orquestração do ambiente de banco de dados |
| 📋 **Pydantic** | Validação e serialização dos dados |
| 🧪 **Pytest** | Execução dos testes automatizados |
| 📮 **Postman** | Testes funcionais e consumo manual da API |

---

# 🐳 Infraestrutura de Banco de Dados (`docker-compose.yml`)

O ambiente de banco de dados utiliza a seguinte configuração isolada e segura para desenvolvimento:

```yaml
services:
  mariadb-dev:
    image: mariadb:10.11
    container_name: mariadb-dev
    restart: always
    ports:
      - "127.0.0.1:${DB_PORT}:${DB_PORT}"
    environment:
      MARIADB_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MARIADB_DATABASE: ${DB_NAME}
      MARIADB_USER: ${DB_USER}
      MARIADB_PASSWORD: ${DB_PASSWORD}
    volumes:
      - db_data:/var/lib/mysql
    healthcheck:
      test: ["CMD-SHELL", "mariadb-admin ping -h 127.0.0.1 -u root -p\"$$MARIADB_ROOT_PASSWORD\" --silent || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 3
      start_period: 30s

volumes:
  db_data:
```

---

# 🚀 Como executar o projeto (Com Docker & MariaDB)

## 1. Clone o repositório e mude para esta branch
```bash
git clone https://github.com/CordeiroGusta/API-produtos.git
cd API-produtos
git checkout sandbox/database
```

## 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto mapeando as variáveis utilizadas no Compose:
```env
DB_PORT=3306
DB_ROOT_PASSWORD=sua_senha_root
DB_NAME=produtos_db
DB_USER=seu_usuario
DB_PASSWORD=sua_senha_usuario
```

## 3. Suba o banco de dados com Docker Compose
Certifique-se de que o Docker está rodando na sua máquina e execute:
```bash
docker compose up -d
```

## 4. Crie e ative o ambiente virtual
```bash
python -m venv .venv
```

### 🪟 Windows — PowerShell
```powershell
.venv\Scripts\Activate.ps1
```

### 🐧 Linux / 🍎 macOS
```bash
source .venv/bin/activate
```

## 5. Instale as dependências
```bash
pip install -r requirements.txt
```

## 6. Inicie a API
```bash
python -m uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.