# app/core/redis.py

import redis.asyncio as redis

#创建一个redis连接客户端
redis_client = redis.Redis(
    #host = 'localhost',
    host = "redis",
    port = 6379,
    db = 0,
    decode_responses = True
)