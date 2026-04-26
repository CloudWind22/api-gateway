#app/mian.py
from fastapi import FastAPI
from app.middleware.auth_middleware import AuthMiddleWare
from app.routes.gateway import router
from app.middleware.logging_middleware import LoginMiddleWare

app = FastAPI(title = "API Gateway")

app.add_middleware(AuthMiddleWare)
app.add_middleware(LoginMiddleWare)
app.include_router(router)
