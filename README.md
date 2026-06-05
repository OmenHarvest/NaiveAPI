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
| GET    | /users/{login}        | Get connection links and config  |

## Naive Services

> [!WARNING]
> To modify a site block (I mean the block itself, not its attributes), use the "site-header" identifier instead of the standard "site" identifier, which is used for this block's parameters

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| GET    | /service/config       | Get current Caddy config         |
| PATCH  | /service/config       | Update a config parameters.      |
| POST   | /service/config       | Create a config parameters.      |

