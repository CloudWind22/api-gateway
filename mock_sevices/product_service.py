# mock_services/product_service.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/products')
async def get_products():
        return {"service": "product",
                "data": ["iphone", "ipad"]}

@app.post('/products')
async def create_products(data: dict):
        return {"service": "product",
                "received": data}