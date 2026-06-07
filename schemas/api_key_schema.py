from pydantic import BaseModel

class ApiKeyCreate(BaseModel):
    name: str

class ApiKeyResponse(BaseModel):
    id: int
    name: str
    is_active: bool

class ApiKeyCreatedResponse(BaseModel):
    id: int
    name: str
    key: str
    is_active: bool

class ApiKeyDeleteRequest(BaseModel):
    keys: list[int]
    
class ApiKeyList(BaseModel):
    keys: list[ApiKeyResponse]

class ApiKeyDeleteResponse(BaseModel):
    deleted_count: int
    deleted: list[ApiKeyResponse]