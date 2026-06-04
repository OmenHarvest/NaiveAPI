from sqlmodel import SQLModel, Field


class Caddyfile_parameter(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    block: str
    parameter: str
    value: str

