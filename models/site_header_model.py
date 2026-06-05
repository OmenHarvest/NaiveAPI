from sqlmodel import SQLModel, Field
from os import getenv


class Header(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    domain: str
    port: int = Field(default_factory=lambda: int(getenv("DEFAULT_SITE_PORT", "443")))
