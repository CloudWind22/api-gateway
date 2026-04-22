#app/routes/gateway.py
from fastapi import APIRouter
from app.services.proxy import forward_request

router = APIRouter()

SERVICE_MAP = {
    "user": "http://localhost:8001",
    "order": "http://localhost:8002",
    "product": "http://localhost:8003",
}

@router.get('/{service_name}')
async def gateway(service_name: str):
    base_url = SERVICE_MAP.get(service_name)

    if not base_url:
        return {"error": "service not found"}
    
    url = f"{base_url}/{service_name}"
    result = await forward_request(url)

    return result
