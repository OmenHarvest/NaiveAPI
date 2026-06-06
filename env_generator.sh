#!/bin/bash

echo "DEFAULT_SITE_PORT=443" >> .env
echo "NAIVE_PROXY=http://localhost:2019" >> .env
echo "" >> .env
echo "DATABASE_URL=sqlite:///data.db" >> .env
echo "" >> .env
echo "AUTH_LOGIN_ENDPOINT_RATELIMIT_TPM=5" >> .env
echo "AUTH_REFRESH_TOKEN_RATELIMIT_TPM=10" >> .env
echo "JWT_ALGORITHM=HS256" >> .env
echo "JWT_EXPIRE_MINUTES=30" >> .env
echo "JWT_REFRESH_EXPIRE_DAYS=7" >> .env
echo "CRYPTOGRAPHY_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env
echo "JWT_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" >> .env
echo "" >> .env