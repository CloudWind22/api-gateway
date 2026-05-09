#app/core/circuit_breaker.py

import time

class CircuitBreaker:

    def __init__(self, fail_threshold = 3, recovery_timeout = 60):
        self.fail_threshold = fail_threshold
        self.recovery_timeout = recovery_timeout

        self.fail_count = 0

        self.state = "CLOSED"

        self.last_failure_time = None

        #是否允许请求通过
    def allow_request(self):

        #正常状态
        if self.state == "CLOSED":
            return True
            
        #熔断状态
        elif self.state == "OPEN":
            current_time = time.time()

            #超过恢复时间
            if current_time - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                return True
            
            #未超过回复时间，熔断服务连接
            else:
                return False
            
        #半开状态：允许一次请求测试
        elif self.state == "HALF_OPEN":
            return True
        
    #请求成功
    def on_success(self):
        self.fail_count = 0
        self.state = "CLOSED"
        
    #请求失败
    def on_failure(self):
        self.fail_count += 1
        self.last_failure_time = time.time()
        if self.fail_count > self.fail_threshold:
            self.state = "OPEN"