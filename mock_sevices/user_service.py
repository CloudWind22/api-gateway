#mock_service/user_service
from fastapi import FastAPI

app = FastAPI()

@app.get('/users')
async def get_users():
    return {"services": "user",
            "data": ["Alice", "Bob"]}