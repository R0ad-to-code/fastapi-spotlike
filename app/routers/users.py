# app/routers/users.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from services.user_service import UserService
from services.jwt_service import JWTService
from schemas import UserCreateSchema, UserLoginSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

@router.post("/users/signup")
def add_user(user: UserCreateSchema):
    user_id = UserService.create_user(user)
    return {"message": "Utilisateur créé avec succès", "user_id": user_id}

@router.post("/users/login")
def login_user(payload: UserLoginSchema):
    user_id = UserService.login_user(payload)
    access_token = UserService.create_access_token({"user_id": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/users/{id}")
def delete_user(id: str, token: str = Depends(oauth2_scheme)):
    payload = JWTService.decode_token(token) 
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    UserService.delete_user(id)
    return {"message": "User supprimé avec succès", "user_id": id}
