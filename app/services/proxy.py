#app/services/proxy.py
import httpx

TIMEOUT = 5.0 #秒

async def forward_request(method: str,
                          url: str,
                          headers: dict,
                          body: bytes):
            print(f"[Gateway] Forwarding request to: {url}")
            async with httpx.AsyncClient(timeout = TIMEOUT) as client: #创建HTTP异步客户端上下文
                try:
                    response = await client.request(method = method, 
                                                    url = url,
                                                    headers = headers,
                                                    content = body)
                    
                    print(response)
                    return {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content": response.content
                    }
                except httpx.TimeoutException:
                    return {
                        "status_code": 504,
                        "headers": {},
                        "content": b"Gateway Timeout"
                    }

                except Exception as e:
                    return {
                            "status_code": 500,                
                            "headers": {},
                            "content": str(e).encode()
                            }             #解析并返回json数据