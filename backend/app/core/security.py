from datetime import datetime, timedelta
import bcrypt
from jose import JWTError, jwt
from app.core.config import SECRET_KEY, ALGORITHM

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_minutes: int = 60):
    payload = data.copy()

    expire = (
        datetime.utcnow() + timedelta(minutes=expires_minutes)
    )

    payload.update({"exp": expire})

    return jwt.encode(
        payload, 
        SECRET_KEY, 
        algorithm=ALGORITHM
    )