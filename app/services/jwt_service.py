# app/services/jwt_service.py
import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from fastapi.openapi.utils import get_openapi
from typing import Union

from config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

class JWTService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: Union[int, None] = None) -> str:
        """Crée un token JWT avec une date d'expiration."""
        to_encode = data.copy()
        if expires_delta is None:
            expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict:
        """Décoder et valider un token JWT."""
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Le token est expiré",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalide",
                headers={"WWW-Authenticate": "Bearer"},
            )
    @staticmethod
    def custom_openapi(app):
        """
        Personnalise le schéma OpenAPI pour inclure OAuth2 avec JWT.
        """
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "OAuth2PasswordBearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
        openapi_schema["security"] = [{"OAuth2PasswordBearer": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema