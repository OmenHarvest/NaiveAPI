from fastapi import APIRouter

service = APIRouter(prefix="/service", tags=["service"])

@service.get("/config")
def get_config():
    pass

@service.patch("/config")
def patch_config():
    pass

@service.post("/config/raw")
def post_config():
    pass