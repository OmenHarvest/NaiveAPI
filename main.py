import asyncio

from dotenv import load_dotenv
from os import getenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db, session_factory
from routers import auth, service, user

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from services.http.naive_dialoge import caddy_sync_loop
from services.auth_service import generate_master_key
from models.api_key_model import ApiKey

import services.http.naive_dialoge
import logging
logger = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    if(getenv("RESET_MASTER_KEY_ON_STARTUP", "false").lower() == "true"):
        with session_factory() as session:
            logger.warning("Resetting master key on startup")
            key = generate_master_key(session=session, is_initial=False)
            logger.info(f"new master key: {key}")
    task = asyncio.create_task(caddy_sync_loop(session_factory))
    await asyncio.sleep(0)
    yield
    task.cancel()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(service.service)
app.include_router(user.role)
app.include_router(auth.auth)
