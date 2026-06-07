<div align="center">
  <img width="200" height="200" alt="logo" src="https://github.com/user-attachments/assets/9675e185-d7fb-44b8-9db8-17cb40a42846" />
</div>

# 👋 Introduction
**NaiveAPI** is an API Gateway for NaiveProxy based on FastAPI.

# ☄️ How To Install

## Docker Compose

Clone the repository and place it next to your `naive/` folder:

```
.
├── naive/
│   └── users.conf
└── NaiveAPI/
    ├── docker-compose.yml
    └── ...
```

Generate the `.env` file:

```bash
chmod +x env_generator.sh
./env_generator.sh
```

The script generates:
- `CRYPTOGRAPHY_KEY` — Fernet key for encrypting user passwords
- `AUTH_INIT_ENDPOINT_RATELIMIT_TPM` — rate limit for `/auth/init` (requests per minute)
- `AUTH_ENDPOINT_RATELIMIT_TPM` — rate limit for all other auth endpoints (requests per minute)

> [!IMPORTANT]
> Keep your `.env` file safe. If `CRYPTOGRAPHY_KEY` is lost, all stored passwords become unrecoverable.

Start the container:

```bash
docker compose up -d
```

API will be available at `http://localhost:8000`.

## Database

| Database | `DATABASE_URL` | Driver | Notes |
|----------|----------------|--------|-------|
| SQLite | `sqlite:///data.db` | built-in | default, no setup required |
| PostgreSQL | `postgresql://user:pass@host/db` | `psycopg2-binary` | recommended for production |
| MySQL | `mysql+pymysql://user:pass@host/db` | `pymysql` | |
| MariaDB | `mariadb+pymysql://user:pass@host/db` | `pymysql` | |

# 🔐 Authentication

NaiveAPI uses API keys passed via the `X-API-Key` header.

There are two key types:

| Type | Capabilities |
|------|-------------|
| Master key | Manage API keys (create, deactivate, delete, rotate) |
| Regular key | Access all other endpoints (users, config) |

## Initial Setup

On a fresh install, no keys exist. Generate the master key once:

```http
POST /auth/init
```

Returns the master key — **save it**, it won't be shown again.

Then use the master key to generate regular keys for day-to-day use:

```http
POST /auth/keys
X-API-Key: <master_key>

{"name": "my-key"}
```

Include the key in every subsequent request:

```http
X-API-Key: <your_key>
```

# 🎯 Endpoints

## Auth

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/init` | — | Generate master key (once) |
| POST | `/auth/keys` | Master | Generate a new API key |
| GET | `/auth/keys` | Master | List all API keys |
| PATCH | `/auth/keys/{id}/deactivate` | Master | Deactivate an API key |
| DELETE | `/auth/keys` | Master | Delete deactivated API keys |
| POST | `/auth/rotate-master-key` | Master | Rotate the master key |

## User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List all users |
| POST | `/users/` | Create a user |
| PATCH | `/users/` | Update user password |
| DELETE | `/users/{login}` | Delete a user |
| GET | `/users/{login}` | Get login and decrypted password |

## Naive Service

> [!WARNING]
> To modify site domains and ports use `/service/config/site-header` endpoints, not `/service/config`.

> [!NOTE]
> Available `block` values for `/service/config`: `global_parameter`, `site_parameter`, `forward_proxy_parameter`, `reverse_proxy_header`, `reverse_proxy_parameter`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/service/config` | List all config parameters |
| POST | `/service/config` | Create config parameters |
| PATCH | `/service/config` | Update config parameters |
| GET | `/service/config/site-header` | List site domains |
| POST | `/service/config/site-header` | Add site domain |
| PATCH | `/service/config/site-header` | Update site domain |
| GET | `/service/config/raw` | Get generated Caddyfile as plain text |
