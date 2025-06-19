from decouple import config
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone


JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_ALGORITH = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITH)
    return encoded_jwt