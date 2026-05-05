# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .oidc import router as oidc_router
from .security import create_user

app = FastAPI(title="Demo OIDC Provider")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ui.hostname","https://jupyterhub.hostname"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(oidc_router)

# Seed a demo user
@app.on_event("startup")
async def startup():
    create_user(
        sub="user123",
        email="user@example.com",
        name="Demo User",
        password="123",
    )
