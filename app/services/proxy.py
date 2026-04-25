#app/services/proxy.py
import httpx
import time
from app.core.logger import logger

TIMEOUT = 5.0 #秒

async def forward_request(method: str,
                          url: str,
                          headers: dict,
                          body: bytes):
            #记录转发时间
            start_time = time.time()
            #记录日志
            logger.info(f"[Forward] {method}->{url}")
            
            async with httpx.AsyncClient(timeout = TIMEOUT) as client: #创建HTTP异步客户端上下文
                try:
                    #获取服务器端响应
                    response = await client.request(method = method, 
                                                    url = url,
                                                    headers = headers,
                                                    content = body)
                    
                    #计算等待时间
                    duration = int((time.time() - start_time) * 1000)

                    logger.info(f"[Response] {response.status_code}({duration}ms)")

                    return {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content": response.content
                    }
                
                except httpx.TimeoutException:
                    duration = int((time.time() - start_time) * 1000)

                    logger.error(f"[Error] 504 Gateway Timeout({duration}ms)")

                    return {
                        "status_code": 504,
                        "headers": {},
                        "content": b"Gateway Timeout"
                    }

                except Exception as e:
                    duration = int((time.time() - start_time) * 1000)

                    logger.error(f"[Error] 500 {str(e)} ({duration}ms)")
                    return {
                            "status_code": 500,                
                            "headers": {},
                            "content": str(e).encode()
                            }             #解析并返回json数据