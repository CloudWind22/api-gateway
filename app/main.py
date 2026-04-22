#app/mian.py
from fastapi import FastAPI
from app.routes.gateway import router

app = FastAPI(title = "API Gateway")

app.include_router(router)
