import hashlib
import hmac
from os import getenv
from sqlmodel import Session, select
from fastapi import HTTPException
from fastapi.security import APIKeyHeader
from models.api_key_model import ApiKey
import secrets

from schemas.api_key_schema import ApiKeyCreate, ApiKeyDeleteRequest
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")
SECRET = getenv("CRYPTOGRAPHY_KEY")

def hash_key(key: str) -> str:
    return hmac.new(SECRET.encode(), key.encode(), hashlib.sha256).hexdigest()

def generate_api_key(name: str, session: Session, is_master: bool = False) -> str:
    raw_key = secrets.token_urlsafe(32)
    db_key = ApiKey(name=name, key_hash=hash_key(raw_key), is_master=is_master)
    session.add(db_key)
    session.commit()
    return raw_key

def verify_api_key(session: Session, key: str) -> ApiKey:
    db_key = session.exec(
        select(ApiKey).where(ApiKey.key_hash == hash_key(key), ApiKey.is_active == True)
    ).first()
    if not db_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return db_key

def verify_master_key(session: Session, key: str) -> ApiKey:
    db_key = session.exec(
        select(ApiKey).where(
            ApiKey.key_hash == hash_key(key),
            ApiKey.is_active == True,
            ApiKey.is_master == True
        )
    ).first()
    if not db_key:
        raise HTTPException(status_code=403, detail="Master key required")
    return db_key

def generate_master_key(session: Session, is_initial: bool) -> str:
    existing_master = session.exec(
        select(ApiKey).where(ApiKey.is_master == True)
    ).first()
    if existing_master:
        if is_initial:
            raise HTTPException(status_code=400, detail="Master API key already exists")
        session.delete(existing_master)
        session.commit()
    return generate_api_key("master", session, is_master=True)

def generate_default_api_key(data: ApiKeyCreate, session: Session) -> str:
    return generate_api_key(data.name, session)

def deactivate_api_key(session: Session, key_id: int):
    db_key = session.get(ApiKey, key_id)
    if not db_key:
        raise HTTPException(status_code=404, detail="API key not found")
    db_key.is_active = False
    session.add(db_key)
    session.commit()
    return db_key

def delete_api_keys(session: Session, keys: ApiKeyDeleteRequest):
    deleted_keys = []
    for key_id in keys.keys:
        db_key = session.get(ApiKey, key_id)
        if not db_key:
            continue
        if db_key.is_active:
            raise HTTPException(status_code=400, detail=f"Key {key_id} is still active")
        if db_key.is_master:
            raise HTTPException(status_code=403, detail="Cannot delete master key")
        session.delete(db_key)
        deleted_keys.append(db_key)
    session.commit()
    return deleted_keys

def get_api_keys(session: Session):
    return session.exec(select(ApiKey)).all()
