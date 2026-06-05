from datetime import datetime, timedelta
from os import getenv
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session
from models.admin_model import Admin
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = getenv("JWT_SECRET")
ALGORITHM = getenv("JWT_ALGORITHM", "HS256")
ACCESS_EXPIRE = int(getenv("JWT_EXPIRE_MINUTES", "30"))
REFRESH_EXPIRE = int(getenv("JWT_REFRESH_EXPIRE_DAYS", "7"))


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(data: dict, expires_delta: timedelta) -> str:
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)

def create_tokens(login: str) -> dict:
    access = create_token(
        {"sub": login, "role": "admin"},
        timedelta(minutes=ACCESS_EXPIRE)
    )
    refresh = create_token(
        {"sub": login, "role": "admin", "type": "refresh"},
        timedelta(days=REFRESH_EXPIRE)
    )
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}

def login(session: Session, login: str, password: str) -> dict:
    admin = session.get(Admin, login)
    if not admin or not verify_password(password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_tokens(login)

def refresh(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return create_tokens(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_admin(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")