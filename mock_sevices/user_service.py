#mock_service/user_service
from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get('/users')
async def get_users():
        return {"service": "user",
                "data": ["Alice", "Bob"]}

@app.post('/users')
async def create_user(data: dict):
        return {
            "service": "user",
            "received": data
        }

@app.get('/slow')
async def slow():
        await asyncio.sleep(10)
        return {"msg": "too slow"}