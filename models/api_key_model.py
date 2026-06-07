from sqlmodel import SQLModel, Field

class ApiKey(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    key_hash: str
    is_active: bool = True
    is_master: bool = False