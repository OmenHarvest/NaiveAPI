from fastapi import APIRouter, Depends, Response, HTTPException
from sqlmodel import Session
from database import get_session
from schemas.caddyfile_schema import ParameterResponse, ParameterAddOrUpdate

from services.naive_service import get_naive_config, patch_naive_config, create_new_parameter

service = APIRouter(prefix="/service", tags=["service"])

@service.get("/config", response_model=list[ParameterResponse])
def get_config(response:Response, session: Session = Depends(get_session)):
    parameters = get_naive_config(session)
    if not parameters:
        return HTTPException(status_code=404, detail="Config is empty")
    response.code=200
    return parameters

@service.patch("/config", response_model=list[ParameterResponse])
def patch_config(response:Response, parameters:list[ParameterAddOrUpdate], session: Session = Depends(get_session)):
    response.status_code=200
    return patch_naive_config(parameters=parameters, session=session)

@service.post("/config", response_model=list[ParameterResponse])
def post_config(response:Response, parameters:list[ParameterAddOrUpdate], session: Session = Depends(get_session)):
    response.status_code=200
    return create_new_parameter(parameters=parameters, session=session)