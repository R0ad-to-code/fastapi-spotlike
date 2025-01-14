# app/services/user_service.py
from bson import ObjectId
from passlib.hash import bcrypt
from fastapi import HTTPException, status

from app.config.database import db
from app.schemas import UserCreateSchema, UserLoginSchema
from app.services.jwt_service import JWTService

class UserService:

    @staticmethod
    def create_user(user: UserCreateSchema):
        if db["users"].find_one({"email": user.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà enregistré"
            )
        hashed_password = bcrypt.hash(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_password

        result = db["users"].insert_one(user_dict)
        return str(result.inserted_id)

    @staticmethod
    def login_user(payload: UserLoginSchema):
        user = db["users"].find_one({"username": payload.username})
        if not user or not bcrypt.verify(payload.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nom d'utilisateur ou mot de passe invalide"
            )
        return str(user["_id"])

    @staticmethod
    def delete_user(user_id: str):
        result = db["users"].delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User non trouvé")

    @staticmethod
    def create_access_token(data: dict):
        """
        Crée un token JWT en utilisant le JWTService.
        """
        return JWTService.create_access_token(data)
