from sqlmodel import Session, select, delete
from models.caddyfile_model import Caddyfile_parameter

from schemas.caddyfile_schema import ParameterAddOrUpdate


def get_naive_config(session:Session):
    parameters = session.exec(select(Caddyfile_parameter)).all()
    if not parameters:
        return None
    
    return parameters

def patch_naive_config(session: Session, parameters:list[ParameterAddOrUpdate]):
    pass        

def get_raw_config(session: Session):
    pass

def post_raw_config(session: Session):
    pass