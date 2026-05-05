# backend/app/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class User(BaseModel):
    sub: str
    email: EmailStr
    name: str
    password_hash: str

class AuthCode(BaseModel):
    code: str
    client_id: str
    redirect_uri: str
    scope: str
    user_sub: str
    expires_at: int

class TokenRequest(BaseModel):
    grant_type: str
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int

class UserInfo(BaseModel):
    sub: str
    email: EmailStr
    name: str
