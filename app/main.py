#app/mian.py
from fastapi import FastAPI
from app.middleware.auth_middleware import AuthMiddleWare
from app.middleware.logging_middleware import LoggingMiddleWare
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.routes.gateway import router

app = FastAPI(title = "API Gateway")

app.add_middleware(AuthMiddleWare)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(LoggingMiddleWare)

app.include_router(router)
