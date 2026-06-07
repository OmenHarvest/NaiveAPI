from fastapi import APIRouter, Depends, Response, Security
from sqlmodel import Session

from database import get_session
from os import getenv
from routers import service
from services.auth_service import (
    API_KEY_HEADER,
    generate_master_key,
    deactivate_api_key,
    delete_api_keys,
    generate_default_api_key,
    get_api_keys,
    verify_master_key
)

from schemas.api_key_schema import (
    ApiKeyDeleteRequest,
    ApiKeyResponse,
    ApiKeyCreatedResponse,
    ApiKeyList,
    ApiKeyDeleteResponse,
    ApiKeyCreate
)
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

limiter = Limiter(key_func=get_remote_address)
INIT_AUTH_ENDPOINT_RATELIMIT_TPM = getenv("AUTH_INIT_ENDPOINT_RATELIMIT_TPM", 5)
AUTH_ENDPOINT_RATELIMIT_TPM = getenv("AUTH_ENDPOINT_RATELIMIT_TPM", 10)


auth = APIRouter(prefix="/auth", tags=["auth"])

@auth.post("/init")
@limiter.limit(f"{INIT_AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def init_auth_endpoint(request: Request, response: Response, session: Session = Depends(get_session)):
    master_key = generate_master_key(session=session, is_initial=True)
    response.status_code = 201
    return master_key

@auth.post("/keys", summary="Generate a new API key", response_model=ApiKeyCreatedResponse)
@limiter.limit(f"{AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def generate_api_key_endpoint(request: Request, data: ApiKeyCreate, response: Response, key: str = Security(API_KEY_HEADER), session: Session = Depends(get_session)):
    verify_master_key(session, key)
    response.status_code = 201
    key = generate_default_api_key(data, session=session)
    return key


@auth.get("/keys", summary="List all API keys", response_model=ApiKeyList)
@limiter.limit(f"{AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def get_api_keys_endpoint(request: Request, response: Response, key: str = Security(API_KEY_HEADER), session: Session = Depends(get_session)):
    verify_master_key(session, key)
    keys = get_api_keys(session=session)
    if not keys:
        return {"keys": []}
    response.status_code = 200
    return keys

@auth.patch("/keys/{key_id}/deactivate", summary="Deactivate an API key", response_model=ApiKeyResponse)
@limiter.limit(f"{AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def deactivate_api_key_endpoint(request: Request, key_id: int, response: Response, session: Session = Depends(get_session)):
    verify_master_key(session, key)
    key = deactivate_api_key(session=session, key_id=key_id)
    response.status_code = 200
    return key
    

@auth.delete("/keys", summary="Delete an API keys", response_model=ApiKeyDeleteResponse)
@limiter.limit(f"{AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def delete_api_keys_endpoint(request: Request, keys: ApiKeyDeleteRequest, response: Response, key: str = Security(API_KEY_HEADER), session: Session = Depends(get_session)):
    verify_master_key(session, key)    
    deleted_keys = delete_api_keys(session=session, keys=keys)
    response.status_code = 200
    return deleted_keys

@auth.post("/rotate-master-key", summary="Rotate the master API key")
@limiter.limit(f"{AUTH_ENDPOINT_RATELIMIT_TPM}/minute")
def rotate_master_key_endpoint(request: Request, response: Response, key: str = Security(API_KEY_HEADER),session: Session = Depends(get_session)):
    verify_master_key(session, key)
    new_master_key = generate_master_key(session=session, is_initial=False)
    response.status_code = 200
    return new_master_key