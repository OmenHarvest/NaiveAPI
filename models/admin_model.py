from sqlmodel import SQLModel, Field

class Admin(SQLModel, table=True):
    login: str = Field(primary_key=True)
    password_hash: str