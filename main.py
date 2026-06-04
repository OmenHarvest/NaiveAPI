from fastapi import FastAPI
from routers import service, user

app = FastAPI()

app.include_router(service.service)
app.include_router(user.role)
