import asyncio

from dotenv import load_dotenv

load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db, session_factory
from routers import auth, service, user

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from services.http.naive_dialoge import caddy_sync_loop

import services.http.naive_dialoge

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(caddy_sync_loop(session_factory))
    await asyncio.sleep(0)  # отдаём управление event loop
    yield
    task.cancel()
    
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(service.service)
app.include_router(user.role)
app.include_router(auth.auth)
