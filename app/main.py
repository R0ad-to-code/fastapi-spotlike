from fastapi import FastAPI, HTTPException, status
from passlib.hash import bcrypt
import jwt

from app.database import db
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import UserLoginSchema

app = FastAPI(
    title="Spotilike API",
    description="API REST pour la plateforme Spotilike",
    version="1.0.0",
)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/users/login")
def login_user(payload: UserLoginSchema):
    user = db["users"].find_one({"username": payload.username})
    if not user or not bcrypt.verify(payload.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password"
        )

    access_token = create_access_token({"user_id": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
