from sqlmodel import Session, select, delete
from models.caddyfile_model import Caddyfile_parameter

def get_naive_config(session:Session):
    parameters = session.exec(select(Caddyfile_parameter)).all()
    if not parameters:
        return None
    
    return parameters