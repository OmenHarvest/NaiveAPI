from sqlmodel import SQLModel, create_engine, Session
from os import getenv

import models.caddyfile_model, models.user_model, models.site_header_model, models.admin_model

DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./data.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {},
)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
