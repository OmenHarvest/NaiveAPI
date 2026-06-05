<div align="center">
  <img width="200" height="200" alt="logo" src="https://github.com/user-attachments/assets/9675e185-d7fb-44b8-9db8-17cb40a42846" />
</div>



# 👋Introduction
**NaiveAPI** is API Gateway for NaiveProxy based on FastAPI.


# ☄️How To Install



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

| Method | Endpoint | Description | Success | Error |
|--------|----------|-------------|---------|-------|
| GET | /users | List all users | 200 / 204 | — |
| POST | /users | Create user | 201 | 409 login taken |
| PATCH | /users | Update user | 200 | 404 not found |
| DELETE | /users/{login} | Delete user | 204 | 404 not found |
| GET | /users/{login} | Get login and decrypted password | 200 | 404 not found |


## Naive Service

> [!WARNING]
> To modify site domains and ports use `/service/config/site-header` endpoints, not `/service/config`.

> [!NOTE]
> Available `block` values: `global_parameter`, `forward_proxy_parameter`, `reverse_proxy_header`, `reverse_proxy_parameter`

| Method | Endpoint | Description | Success | Error |
|--------|----------|-------------|---------|-------|
| GET | /service/config | Get all config parameters | 200 / 204 | — |
| POST | /service/config | Create config parameters | 201 | 409 duplicate |
| PATCH | /service/config | Update config parameters | 200 | 404 not found |
| GET | /service/config/site-header | Get site domains | 200 / 204 | — |
| POST | /service/config/site-header | Add site domain | 201 | — |
| DELETE | /service/config/site-header/{id} | Remove site domain | 204 | 404 not found |