from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routers import service, user, auth
import services.naive_config_generator

limiter = Limiter(key=)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(service.service)
app.include_router(user.role)
app.include_router(auth.auth)