#app/core/auth.py

from jose import jwt, JWTError

SECRET_KEY = "wanghaolu8418"
ALGORITHM = "HS256"

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])

        #从解码后的payload中取出需要的字段
        user_id = payload.get("user_id")

        if user_id is None:
            return None
        return {
            "user_id": user_id
            }
    
    except JWTError:
        return None