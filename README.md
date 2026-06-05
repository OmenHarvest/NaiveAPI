<div align="center">
  <img width="200" height="200" alt="logo" src="https://github.com/user-attachments/assets/9675e185-d7fb-44b8-9db8-17cb40a42846" />
</div>



# 👋Introduction
**NaiveAPI** is API Gateway for NaiveProxy based on FastAPI.

# ☄️How To Install

## Docker Compose

Clone the repository and place it next to your `naive/` folder

Generate the `.env` file:

```bash
chmod +x env_generator.sh
./env_generator.sh
```

The script automatically generates:
- `CRYPTOGRAPHY_KEY` — Fernet encryption key for storing user passwords
- `JWT_SECRET` — secret key for signing JWT tokens
- `DEFAULT_SITE_PORT` — default port for site headers (443)
- `NAIVE_PROXY` — Caddy Admin API URL (http://localhost:2019)
- `JWT_ALGORITHM`, `JWT_EXPIRE_MINUTES`, `JWT_REFRESH_EXPIRE_DAYS` — JWT settings

> [!IMPORTANT]
> Keep your `.env` file safe. If `CRYPTOGRAPHY_KEY` is lost, all stored passwords become unrecoverable.

Then start the container:

```bash
docker compose up -d
```

API will be available at `http://localhost:8000`.

## Database

| Database | URL prefix | Driver | Notes |
|----------|------------|--------|-------|
| SQLite | `sqlite:///./data.db` | built-in | default, no setup required |
| PostgreSQL | `postgresql://user:pass@host/db` | `psycopg2-binary` | recommended for production |
| MySQL | `mysql+pymysql://user:pass@host/db` | `pymysql` | |
| MariaDB | `mariadb+pymysql://user:pass@host/db` | `pymysql` | |


# 🔐Authentication

NaiveAPI uses JWT for authentication. All endpoints except `/auth/login` require a valid access token.

Include the token in every request:

```http
Authorization: Bearer eyJ...
```

| Token | Lifetime |
|-------|----------|
| Access token | 30 minutes |
| Refresh token | 7 days |


# 🎯Endpoints


## Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | Obtain JWT token |
| POST | /auth/refresh | Refresh access token |


## User Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /users | List all users |
| POST | /users | Create user |
| PATCH | /users | Update user |
| DELETE | /users/{login} | Delete user |
| GET | /users/{login} | Get login and decrypted password |


## Naive Service

> [!WARNING]
> To modify site domains and ports use `/service/config/site-header` endpoints, not `/service/config`.

> [!NOTE]
> Available `block` values: `global_parameter`, `forward_proxy_parameter`, `reverse_proxy_header`, `reverse_proxy_parameter`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /service/config | Get all config parameters |
| POST | /service/config | Create config parameters |
| PATCH | /service/config | Update config parameters |
| GET | /service/config/site-header | Get site domains |
| POST | /service/config/site-header | Add site domain |
| DELETE | /service/config/site-header/{id} | Remove site domain |
| GET | /service/config/raw | Get generated Caddyfile as plain text |
