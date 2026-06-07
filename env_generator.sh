#!/bin/bash

echo "DEFAULT_SITE_PORT=443" >> .env
echo "NAIVE_PROXY=http://localhost:2019" >> .env
echo "" >> .env
echo "DATABASE_URL=sqlite:///data.db" >> .env
echo "" >> .env
echo "AUTH_INIT_ENDPOINT_RATELIMIT_TPM=5" >> .env
echo "AUTH_ENDPOINT_RATELIMIT_TPM=10" >> .env
echo "CRYPTOGRAPHY_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')" >> .env