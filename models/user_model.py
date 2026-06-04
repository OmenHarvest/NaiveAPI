from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    login: str = Field(primary_key=True)
    password: str