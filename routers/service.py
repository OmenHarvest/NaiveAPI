from fastapi import APIRouter

router = APIRouter(prefix="/service", tags=["service"])

# Status controller
@router.get("/status")
def get_status():
    return {"status": "running"}

# Caddy editor 
# Restart controller