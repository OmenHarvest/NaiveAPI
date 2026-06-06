from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from database import get_session
from schemas.auth_schema import AdminLogin, TokenResponse
from services.auth_service import (
    login as login_service,
    refresh as refresh_service,
    get_current_admin,
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from os import getenv

limiter = Limiter(key_func=get_remote_address)

auth = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

RATELIMIT_LOGIN_TPM = getenv("AUTH_LOGIN_ENDPOINT_RATELIMIT_TPM", 5)
RATELIMIT_REFRESH_TOKEN_TPM = getenv("AUTH_REFRESH_ENDPOINT_RATELIMIT_TPM", 10)

def current_admin(token: str = Depends(oauth2_scheme)):
    return get_current_admin(token)


@auth.post("/login", response_model=TokenResponse)
@limiter.limit(f"{RATELIMIT_LOGIN_TPM}/minute")
def login(request: Request, data: AdminLogin, session: Session = Depends(get_session)):
    return login_service(session=session, login=data.login, password=data.password)



@auth.post("/refresh", response_model=TokenResponse)
@limiter.limit(f"{RATELIMIT_REFRESH_TOKEN_TPM}/minute")
def refresh(request: Request, token: str, session: Session = Depends(get_session)):
    return refresh_service(token=token)
