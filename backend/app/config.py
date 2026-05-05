# backend/app/config.py
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    issuer_ui: AnyHttpUrl = "https://ui.hostname"
    issuer: AnyHttpUrl = "https://api.hostname:81"
    client_id: str = "jupyterhub-client"
    client_secret: str = "jupyterhub-secret"
    redirect_uri: AnyHttpUrl = "https://jupyterhub.hostname:8000/hub/oauth_callback"
    jwt_secret: str = "CHANGE_ME_TO_A_LONG_RANDOM_SECRET"
    jwt_alg: str = "HS256"  # or HS256 if you prefer symmetric
    access_token_lifetime: int = 600
    id_token_lifetime: int = 600

settings = Settings()
