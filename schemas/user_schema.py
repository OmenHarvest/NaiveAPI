import secrets
import string
from pydantic import BaseModel, model_validator


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(16))


def generate_login() -> str:
    return secrets.token_hex(8)


class UserCreateOrUpdate(BaseModel):
    login: str | None = None
    password: str | None = None

    @model_validator(mode="after")
    def generate_if_empty(self):
        if not self.password:
            self.password = generate_password()
        if not self.login:
            self.login = generate_login()
        return self


class UserResponse(BaseModel):
    login: str

    model_config = {"from_attributes": True}


class UserExportResponse(BaseModel):
    login: str
    password: str
