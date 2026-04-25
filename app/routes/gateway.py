#app/routes/gateway.py
from fastapi import APIRouter, Request, Body, Response
from app.services.proxy import forward_request
from app.core.logger import logger
from app.core.auth import verify_token

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
        #获取访问IP地址
        client_ip = request.client.host
        #记录日志
        logger.info(f"[Request] {client_ip} {request.method}/{service_name}/{path}")

        #鉴权
        auth_header = request.headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                    content = b"Unauthorized",
                    status_code = 401
            )

        token = auth_header.split(' ')[1]

        user = verify_token(token)

        if not user:
             return Response(
                  content = b"Invalid Token",
                  status_code = 401
             )

        #匹配路由
        base_url = SERVICE_MAP.get(service_name)

        if not base_url:
            return Response(
                 content = b"serivce not found",
                 status_code = 404
                )
        
        url = f"{base_url}/{path}"

        #转发请求
        method = request.method
        headers = dict(request.headers)

        headers['X-User-Id'] = str(user['user_id'])
        
        #过滤请求报文中的危险header
        headers.pop("host", None)
        headers.pop("content-length", None)

        raw_body = await request.body()

        result = await forward_request(method, url, headers, raw_body)

        #过滤响应报文的header
        response_headers = {
            k: v for k, v in result["headers"].items()
            if k.lower() not in ["content-encoding", "transfer-encoding", "connection"]
        }

        return Response(
            content = result["content"],
            status_code = result["status_code"],
            headers = response_headers
        )
