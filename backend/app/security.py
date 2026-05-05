# backend/app/security.py
from datetime import datetime, timedelta, timezone
from typing import Dict
from jose import jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory stores (replace with DB/redis in real system)
USERS: Dict[str, dict] = {}
AUTH_CODES: Dict[str, dict] = {}
TOKENS: Dict[str, dict] = {}

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_user(sub: str, email: str, name: str, password: str):
    USERS[sub] = {
        "sub": sub,
        "email": email,
        "name": name,
        "password_hash": hash_password(password),
    }

def authenticate_user(username: str, password: str):
    # Here we treat username as email for simplicity
    for u in USERS.values():
        if u["email"] == username and verify_password(password, u["password_hash"]):
            return u
    return None

def create_jwt_token(sub: str, lifetime: int, extra_claims: dict | None = None) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "iss": str(settings.issuer),
        "sub": sub,
        "aud": settings.client_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(seconds=lifetime)).timestamp()),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)
