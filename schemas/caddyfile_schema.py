from pydantic import BaseModel


class ParameterResponse(BaseModel):
    id: int
    block: str
    parameter: str
    value: str

    model_config = {"from_attributes": True}

class ParameterAddOrUpdate(BaseModel):
    block: str
    parameter: str
    value: str

class ConfigRaw(BaseModel):
    caddyfile: str 