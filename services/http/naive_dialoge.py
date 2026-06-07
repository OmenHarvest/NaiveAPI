import asyncio
import httpx
from os import getenv
from sqlmodel import Session

import state
from events_bus import listener
from services.naive_config_generator import get_naive_config

import logging
logger = logging.getLogger("uvicorn")

def _do_reload(session: Session):
    caddyfile = get_naive_config(session)
    httpx.post(
        f"{getenv('NAIVE_PROXY', 'http://localhost:2019')}/load",
        content=caddyfile.encode(),
        headers={"Content-Type": "text/caddyfile"},
    ).raise_for_status()


def _is_caddy_available() -> bool:
    try:
        httpx.get(
            f"{getenv('NAIVE_PROXY', 'http://localhost:2019')}/config/",
            timeout=2.0,
        ).raise_for_status()
        return True
    except (httpx.ConnectError, httpx.HTTPStatusError, httpx.TimeoutException) as e:
        print(e, flush=True)
        return False


async def caddy_sync_loop(session_factory):
    while True:
        print(f"TICK dirty={state.config_dirty} caddy={_is_caddy_available()}", flush=True)
        if state.config_dirty and _is_caddy_available():
            try:
                with session_factory() as session:
                    _do_reload(session)
                state.config_dirty = False
                print("RELOAD OK", flush=True)
            except Exception as e:
                print(f"RELOAD FAILED: {e}", flush=True)
        await asyncio.sleep(5)


@listener("user.changed")
@listener("config.changed")
def reload_caddy(session: Session):
    state.config_dirty = True
    try:
        _do_reload(session)
        state.config_dirty = False
    except (ValueError, httpx.ConnectError, httpx.HTTPStatusError):
        pass