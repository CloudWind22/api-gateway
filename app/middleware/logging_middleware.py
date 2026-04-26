#app/middleware.logging_middleware.py

import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from app.core.logger import logger

class LoginMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        #记录时间
        start = time.time()

        #获取客户端IP/HTTP方法/URL.path
        client_ip = request.client.host
        method = request.method
        path = request.url.path

        logger.info(f'[Request] {client_ip} {method} {path}')

        response = await call_next(request)

        duration = int((time.time() - start) * 1000)

        logger.info(f'[Request] {response.status_code} ({duration}ms)')

        return response
        