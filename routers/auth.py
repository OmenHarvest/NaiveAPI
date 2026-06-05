from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from database import get_session
from schemas.auth_schema import AdminLogin, TokenResponse
from services.auth_service import login as login_service, refresh as refresh_service, get_current_admin

auth = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def current_admin(token: str = Depends(oauth2_scheme)):
    return get_current_admin(token)


@auth.post("/login", response_model=TokenResponse)
def login(data: AdminLogin, session: Session = Depends(get_session)):
    return login_service(session=session, login=data.login, password=data.password)


@auth.post("/refresh", response_model=TokenResponse)
def refresh(token: str, session: Session = Depends(get_session)):
    return refresh_service(token=token)