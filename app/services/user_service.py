# app/services/user_service.py
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from config.database import get_db
from models import User
from schemas import UserCreateSchema, UserLoginSchema
from services.jwt_service import JWTService

class UserService:

    @staticmethod
    def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà enregistré"
            )
        
        # Créer le nouvel utilisateur
        hashed_password = bcrypt.hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user.id

    @staticmethod
    def login_user(payload: UserLoginSchema, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.username == payload.username).first()
        if not user or not bcrypt.verify(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nom d'utilisateur ou mot de passe invalide"
            )
        return user.id

    @staticmethod
    def delete_user(user_id: int, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User non trouvé")
        
        db.delete(user)
        db.commit()
        return {"message": "Utilisateur supprimé avec succès"}

    @staticmethod
    def create_access_token(data: dict):
        """
        Crée un token JWT en utilisant le JWTService.
        """
        return JWTService.create_access_token(data)
