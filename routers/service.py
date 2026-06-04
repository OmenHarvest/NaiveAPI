from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel import Session
from database import get_session
from schemas.caddyfile_schema import ParameterResponse, ParameterAddOrUpdate

from services.naive_service import get_naive_config

service = APIRouter(prefix="/service", tags=["service"])

@service.get("/config", response_model=ParameterResponse)
def get_config(response:Response, session: Session = Depends(get_session)):
    parameters = get_naive_config(session)
    if not parameters:
        return HTTPException(status_code=404, detail="Config is empty")
    response.code=200
    return parameters

@service.patch("/config")
def patch_config(parameters:list[ParameterAddOrUpdate], session: Session = Depends(get_session)):
    pass

@service.get("/config/raw")
def get_raw_config():
    pass

@service.post("/config/raw")
def post_raw_config():
    pass