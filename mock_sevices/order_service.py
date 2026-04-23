# mock_services/order_service.py
from fastapi import FastAPI

app = FastAPI()

@app.get('/orders')
async def get_orders():
        return {"service": "order",
                "data": ["order1", "order2"]}

@app.post('/orders')
async def create_orders(data: dict):
        return {"service": "order",
                "received": data}
