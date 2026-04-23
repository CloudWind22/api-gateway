#app/routes/gateway.py
from fastapi import APIRouter, Request, Body, Response
from app.services.proxy import forward_request

router = APIRouter()

SERVICE_MAP = {
    "user": "http://localhost:8001",
    "order": "http://localhost:8002",
    "product": "http://localhost:8003",
}

@router.api_route("/{service_name}/{path:path}", methods = ['GET', 'POST', 'PUT', 'DELETE'])
async def getway(service_name: str, 
                 path: str, 
                 request: Request,
                 ):
        base_url = SERVICE_MAP.get(service_name)

        if not base_url:
            return {"error": "serivce not found"}
        
        url = f"{base_url}/{path}"

        method = request.method
        headers = dict(request.headers)
        headers.pop("host", None)
        
        raw_body = await request.body()

        result = await forward_request(method, url, headers, raw_body)
        return Response(
            content = result['content'],
            status_code = result['status_code'],
            headers = result['headers']
        )
