#!/bin/bash

echo "CRYPTOGRAPHY_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env
echo "JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
echo "DEFAULT_SITE_PORT=443" >> .env
echo "NAIVE_PROXY=http://localhost:2019" >> .env
echo "JWT_ALGORITHM=HS256" >> .env
echo "JWT_EXPIRE_MINUTES=30" >> .env
echo "JWT_REFRESH_EXPIRE_DAYS=7" >> .env
echo "DATABASE_URL=sqlite:///./data/data.db" >> .env
