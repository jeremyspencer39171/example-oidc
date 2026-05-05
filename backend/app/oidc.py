# backend/app/oidc.py
from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import datetime, timedelta
import secrets
from jose import jwt, JWTError
from .config import settings
from .models import TokenRequest, TokenResponse, UserInfo
from .security import USERS, AUTH_CODES, TOKENS, authenticate_user, create_jwt_token

router = APIRouter()


@router.get("/.well-known/openid-configuration")
async def openid_configuration():
    return {
        "issuer": settings.issuer,
        "authorization_endpoint": f"{settings.issuer}/authorize",
        "token_endpoint": f"{settings.issuer}/token",
        "userinfo_endpoint": f"{settings.issuer}/userinfo",
        "jwks_uri": f"{settings.issuer}/jwks.json",
        "response_types_supported": ["code"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": [settings.jwt_alg],
        "scopes_supported": ["openid", "profile", "email"],
        "grant_types_supported": ["authorization_code"],
    }


@router.get("/jwks.json")
async def jwks():
    # For HS256 this is usually not exposed; for RS256 you’d expose public key here.
    # Minimal placeholder:
    return {"keys": []}


@router.get("/authorize")
async def authorize(
    request: Request,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str | None = None,
):
    if client_id != settings.client_id or redirect_uri != str(settings.redirect_uri):
        raise HTTPException(status_code=400, detail="Invalid client or redirect_uri")

    # In a real app, check user session cookie; if not logged in, redirect to login UI.
    # For now, redirect to Svelte login page with original params.
    login_url = (
        f"{settings.issuer_ui}login"
        f"?response_type={response_type}"
        f"&client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope={scope}"
    )
    if state:
        login_url += f"&state={state}"
    return RedirectResponse(login_url)


@router.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    response_type: str = Form(...),
    client_id: str = Form(...),
    redirect_uri: str = Form(...),
    scope: str = Form(...),
    state: str | None = Form(None),
):
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if response_type != "code":
        raise HTTPException(status_code=400, detail="Unsupported response_type")

    code = secrets.token_urlsafe(32)
    expires_at = int((datetime.utcnow() + timedelta(minutes=5)).timestamp())
    AUTH_CODES[code] = {
        "code": code,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "user_sub": user["sub"],
        "expires_at": expires_at,
    }

    redirect = f"{redirect_uri}?code={code}"
    if state:
        redirect += f"&state={state}"
    return RedirectResponse(redirect, status_code=302)

async def token_form(
    grant_type: str = Form(...),
    code: str = Form(None),
    redirect_uri: str = Form(None),
    client_id: str = Form(None),
    client_secret: str = Form(None),
):
    return TokenRequest(
        grant_type=grant_type,
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=client_secret,
    )


@router.post("/token", response_model=TokenResponse)
async def token(form: TokenRequest = Depends(token_form)):
    if form.grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")

    if (
        form.client_id != settings.client_id
        or form.client_secret != settings.client_secret
    ):
        raise HTTPException(status_code=401, detail="Invalid client credentials")

    auth_code = AUTH_CODES.get(form.code or "")
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid code")

    if auth_code["redirect_uri"] != form.redirect_uri:
        raise HTTPException(status_code=400, detail="Invalid redirect_uri")

    if auth_code["expires_at"] < int(datetime.utcnow().timestamp()):
        raise HTTPException(status_code=400, detail="Code expired")

    user_sub = auth_code["user_sub"]
    print(auth_code)
    user = USERS.get(user_sub)
    if not user:
        raise HTTPException(status_code=400, detail="Unknown user")

    access_token = create_jwt_token(
        user_sub,
        settings.access_token_lifetime,
        extra_claims={"scope": auth_code["scope"]},
    )
    id_token = create_jwt_token(
        user_sub,
        settings.id_token_lifetime,
        extra_claims={
            "email": user["email"],
            "name": user["name"],
        },
    )
    TOKENS[access_token] = {"sub": user_sub, "scope": auth_code["scope"]}

    # One-time use code
    del AUTH_CODES[form.code or ""]

    return TokenResponse(
        access_token=access_token,
        id_token=id_token,
        expires_in=settings.access_token_lifetime,
    )


@router.get("/userinfo", response_model=UserInfo)
async def userinfo(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
            audience=settings.client_id,
        )
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")

    sub = payload.get("sub")
    user = USERS.get(sub)
    if not user:
        raise HTTPException(status_code=401, detail="Unknown user")

    return UserInfo(sub=sub, email=user["email"], name=user["name"])
