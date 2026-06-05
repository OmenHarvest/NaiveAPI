#!/bin/bash

echo "CRYPTOGRAPHY_KEY=$(tr -dc 'A-Za-z0-9' < /dev/urandom | head -c 16)" >> .env