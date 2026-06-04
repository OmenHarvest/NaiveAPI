<div align="center">
  <img width="200" height="200" alt="logo" src="https://github.com/user-attachments/assets/9675e185-d7fb-44b8-9db8-17cb40a42846" />
</div>


# 👋Introduction
**NaiveAPI** is API Gateway for NaiveProxy based on FastAPI.

# ☄️How To Install

## Docker
First, let's install Naive using a Compose file. 

> [!WARNING]
> Whether you're using Docker or installing Naive natively, there's no need to change Caddy's settings via the Caddyfile, since NaiveAPI will apply its own settings as soon as it gains access

```
services:
  naiveproxy:
    image: pocat/naiveproxy:latest
    container_name: naiveproxy
    restart: unless-stopped
    network_mode: host
```

## Database

| Database | URL prefix | Driver | Notes |
|----------|------------|--------|-------|
| SQLite | `sqlite:///./data.db` | built-in | default, no setup required |
| PostgreSQL | `postgresql://user:pass@host/db` | `psycopg2-binary` | recommended for production |
| MySQL | `mysql+pymysql://user:pass@host/db` | `pymysql` | |
| MariaDB | `mariadb+pymysql://user:pass@host/db` | `pymysql` | |

# 🎯Endpoints

## Auth
| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| POST   | /auth/login           | Obtain JWT token                 |
| POST   | /auth/refresh         | Refresh access token             |
| POST   | /auth/logout          | Revoke token                     |

## User managment

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| GET    | /users                | List all users                   |
| POST   | /users                | Create user                      |
| PATCH  | /users/{login}        | Update user password             |
| DELETE | /users/{login}        | Delete user                      |
| GET    | /users/{login}/export | Get connection links and config  |

## Naive Services

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| GET    | /service/config       | Get current Caddy config         |
| PATCH  | /service/config       | Update a single config parameter |
| POST   | /service/config/raw   | Apply raw Caddyfile              |
