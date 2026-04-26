#app/middleware/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.auth import verify_token
from app.utils.whitelist import is_whitelisted

class AuthMiddleWare(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        #白名单放行
        if is_whitelisted(request.url.path, request.method):
            return await call_next(request)
        
        #鉴权
        auth_header = request.headers.get('authorization')

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                content = b"Unauthorized",
                status_code = 401
            )
        
        #HTTP报文首部中authorization的字段通常为："Authorization": Bearer <Token>
        #从字段中分割Token
        token = auth_header.split(' ')[1] 

        user = verify_token(token)

        if not user:
            return Response(
                content = b"Invalid Token",
                status_code = 401
            )
        
        request.state.user = user

        return await call_next(request)