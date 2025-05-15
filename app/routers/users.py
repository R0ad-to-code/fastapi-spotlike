# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from services.user_service import UserService
from services.jwt_service import JWTService
from schemas import UserCreateSchema, UserLoginSchema
from config.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

@router.post("/users/signup")
def add_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_id = UserService.create_user(user, db)
    return {"message": "Utilisateur créé avec succès", "user_id": user_id}

@router.post("/users/login")
def login_user(payload: UserLoginSchema, db: Session = Depends(get_db)):
    user_id = UserService.login_user(payload, db)
    access_token = UserService.create_access_token({"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/users/{id}")
def delete_user(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = JWTService.decode_token(token) 
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    result = UserService.delete_user(id, db)
    return {"message": "User supprimé avec succès", "user_id": id}
