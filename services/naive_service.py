from sqlmodel import Session, select, delete
from models.caddyfile_model import Caddyfile_parameter

from schemas.caddyfile_schema import ParameterAddOrUpdate

import logging

logger = logging.getLogger("uvicorn")


def get_naive_config(session:Session):
    parameters = session.exec(select(Caddyfile_parameter)).all()
    if not parameters:
        return None
    
    return parameters

def patch_naive_config(session: Session, parameters:list[ParameterAddOrUpdate]):

    targets = []

    for parameter in parameters:
        target = session.get(Caddyfile_parameter, parameter.id)
        if not target:
            logger.warning(f"Parameter with id {parameter.id} not found, skipping")
            continue;
        target.block = parameter.block
        target.parameter = parameter.parameter
        target.value = parameter.value
        targets.append(target)
    
    session.commit()

    for updated_parameter in targets:
        session.refresh(updated_parameter)

    return targets


def create_new_parameter(session: Session, parameters:list[ParameterAddOrUpdate]):

    created_parameters = []

    for parameter in parameters:
        new_parameter = Caddyfile_parameter(
            block=parameter.block,
            parameter=parameter.parameter,
            value=parameter.value
        )
        session.add(new_parameter)

        created_parameters.append(new_parameter)

    session.commit()

    for param in created_parameters:
        session.refresh(param)

    return created_parameters


def get_raw_config(session: Session):
    pass

def post_raw_config(session: Session):
    pass