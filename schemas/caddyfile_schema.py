from pydantic import BaseModel


class ConfigResponse(BaseModel):
    id: int
    block: str
    parameter: str
    value: str

    model_config = {"from_attributes": True}

class ConfigUpdate(BaseModel):
    block: str
    parameter: str
    value: str

class ConfigRaw(BaseModel):
    caddyfile: str 