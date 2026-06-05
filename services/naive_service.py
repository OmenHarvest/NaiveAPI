from sqlmodel import Session, select
from models.caddyfile_model import Caddyfile_parameter
from models.site_header_model import Header

from schemas.caddyfile_schema import ParameterAddOrUpdate
from schemas.site_header_schema import SiteAddOrUpdate

from events_bus import emit

import logging

logger = logging.getLogger("uvicorn")


def get_naive_config(session: Session):
    parameters = session.exec(select(Caddyfile_parameter)).all()
    if not parameters:
        return None

    return parameters


def patch_naive_config(session: Session, parameters: list[ParameterAddOrUpdate]):

    targets = []

    for parameter in parameters:
        target = session.get(Caddyfile_parameter, parameter.id)
        if not target:
            logger.warning(f"Parameter with id {parameter.id} not found, skipping")
            continue
        target.block = parameter.block
        target.parameter = parameter.parameter
        target.value = parameter.value
        targets.append(target)

    session.commit()

    for updated_parameter in targets:
        session.refresh(updated_parameter)

    emit("config.changed", session=session)
    return targets


def create_new_parameter(session: Session, parameters: list[ParameterAddOrUpdate]):

    created_parameters = []

    for parameter in parameters:
        new_parameter = Caddyfile_parameter(
            block=parameter.block, parameter=parameter.parameter, value=parameter.value
        )
        session.add(new_parameter)

        created_parameters.append(new_parameter)

    session.commit()

    for param in created_parameters:
        session.refresh(param)

    emit("config.changed", session=session)

    return created_parameters


def get_site_headers(session: Session):
    headers = session.exec(select(Header)).all()
    if not headers:
        return None

    return headers


def create_new_headers(session: Session, headers: list[SiteAddOrUpdate]):
    created_headers = []

    for header in headers:
        new_header = Header(domain=header.domain, port=header.port)

        session.add(new_header)
        created_headers.append(new_header)

    session.commit()

    for header in created_headers:
        session.refresh(header)

    emit("config.changed", session=session)

    return created_headers


def patch_headers(session: Session, headers: list[SiteAddOrUpdate]):

    targets = []

    for header in headers:
        target = session.get(Header, header.id)
        if not target:
            logger.warning(f"Header with id {header.id} not found, skipping")
            continue
        target.domain = header.domain
        target.port = header.port
        targets.append(target)

    session.commit()

    for updated_header in targets:
        session.refresh(updated_header)

    emit("config.changed", session=session)

    return targets
