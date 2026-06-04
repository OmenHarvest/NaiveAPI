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
