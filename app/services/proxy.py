#app/services/proxy.py
import httpx
import time
from app.core.logger import logger
from app.core.circuit_breaker import CircuitBreaker

TIMEOUT = 5.0 #秒

#为所有服务提供熔断器
circuit_breakers = {
      "user": CircuitBreaker(),
      "order": CircuitBreaker(),
      "product": CircuitBreaker()
}

async def forward_request(service_name: str,
                          method: str,
                          url: str,
                          headers: dict,
                          body: bytes):
            
            breaker = circuit_breakers[service_name]
            if not breaker.allow_request():
                
                return {
                    "status_code": 503,
                    "headers": {},
                    "content": b"Service Unavailable (Circuit Open)"
                }
            
            
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

                    breaker.on_success()


                    logger.info(f"[Response] {response.status_code}({duration}ms)")

                    return {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content": response.content
                    }
                
                except httpx.TimeoutException:
                    duration = int((time.time() - start_time) * 1000)
                    breaker.on_failure()

                    logger.error(f"[Error] 504 Gateway Timeout({duration}ms)")

                    return {
                        "status_code": 504,
                        "headers": {},
                        "content": b"Gateway Timeout"
                    }

                except Exception as e:
                    duration = int((time.time() - start_time) * 1000)
                    breaker.on_failure()

                    logger.error(f"[Error] 500 {str(e)} ({duration}ms)")
                    return {
                            "status_code": 500,                
                            "headers": {},
                            "content": str(e).encode()
                            }             #解析并返回json数据