#app/services/proxy.py
import httpx

async def forward_request(url: str):
    async with httpx.AsyncClient() as client: #创建HTTP异步客户端上下文
        response = await client.get(url)   #发送异步请求
        return response.json()             #解析并返回json数据

