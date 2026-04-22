# mock_services/product_service.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/products')
async def get_products():
    return {"service": "product",
            "data": ["iphone", "ipad"]}
