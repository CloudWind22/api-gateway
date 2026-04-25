#获得token
from jose import jwt

SECRET_KEY = "wanghaolu8418"
ALGORITHM = "HS256"

token = jwt.encode({"user_id": 123}, SECRET_KEY, algorithm=ALGORITHM)

print(token)