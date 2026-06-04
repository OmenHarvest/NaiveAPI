import secrets
import string
from pydantic import BaseModel, field_validator


def generate_password(v):
    if not v:
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(16))
    return v


class UserCreate(BaseModel):
    login: str
    password: str | None = None

    @field_validator("password", mode="before")
    @classmethod
    def generate_if_empty(cls, v):
        return generate_password(v)


class UserUpdate(BaseModel):
    password: str | None = None

    @field_validator("password", mode="before")
    @classmethod
    def generate_if_empty(cls, v):
        return generate_password(v)


class UserResponse(BaseModel):
    login: str

    model_config = {"from_attributes": True}


class UserExportResponse(BaseModel):
    login: str
    naive_uri: str
    https_url: str
    json_config: dict
    plain: str