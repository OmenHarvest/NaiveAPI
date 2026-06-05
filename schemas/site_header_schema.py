from pydantic import BaseModel


class SiteAddOrUpdate(BaseModel):
    id: int | None = None
    domain: str
    port: int | None = None


class SiteResponse(BaseModel):
    id: int
    domain: str
    port: int

    model_config = {"from_attributes": True}
