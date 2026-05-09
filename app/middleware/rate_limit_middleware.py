# app/middleware/rate_limit_middleware.py

import time

from collections import defaultdict
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from app.core.redis import redis_client

#限流配置
RATE_LIMIT = 5   #次数
TIME_WINDOW = 10 #秒

class RateLimitMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        #获取客户端IP
        client_ip = request.client.host
        
        current_time = time.time()

        redis_key = f"rate_limit:{client_ip}"

        #删除窗口外的请求
        await redis_client.zremrangebyscore(
                redis_key,
                0,
                current_time - TIME_WINDOW
            )

        #当前窗口内请求数
        request_count =  await redis_client.zcard(redis_key)

        if request_count > RATE_LIMIT:
            return Response(
                content = b"Too many requests",
                status_code = 429
            )
        
        #记录当前请求
        await redis_client.zadd(
            redis_key,
            {str(current_time): current_time}
        )

        #设置过期时间
        redis_client.expire(redis_key, TIME_WINDOW)

        return await call_next(request)