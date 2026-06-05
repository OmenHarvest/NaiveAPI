import httpx
from services.naive_config_generator import get_naive_config
from sqlmodel import Session
from os import getenv

from events_bus import listener

@listener("user.changed")
@listener("config.changed")
def reload_caddy(session: Session):
    caddyfile = get_naive_config(session)
    response = httpx.post(
        f"{getenv("NAIVE_PROXY", "http://localhost:2019")}/load",
        content=caddyfile.encode(),
        headers={"Content-Type": "text/caddyfile"}
    )
    response.raise_for_status()