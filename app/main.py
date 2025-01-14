from fastapi import FastAPI, HTTPException, status
from passlib.hash import bcrypt
import jwt

from app.database import db
from app.config import SECRET_KEY, ALGORITHM
from app.schemas import UserLoginSchema
from bson import ObjectId


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

@app.post("/api/seed")
def seed_db():
    genres_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00001"), "title": "Pop", "description": "Musique populaire"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00002"), "title": "Rock", "description": "Musique rock"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00003"), "title": "Electro", "description": "Musique électronique"}
    ]

    artists_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "name": "Daft Punk", "avatar": "http://example.com/images/daftpunk.png", "biography": "Duo de musique électronique français"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "name": "Queen", "avatar": "http://example.com/images/queen.png", "biography": "Groupe de rock britannique formé en 1970"}
    ]

    albums_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "title": "Discovery", "cover_image": "http://example.com/images/discovery.jpg", "release_date": "2001-03-12", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "song_ids": []},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "title": "A Night at the Opera", "cover_image": "http://example.com/images/night_at_the_opera.jpg", "release_date": "1975-11-21", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "song_ids": []}
    ]

    songs_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30001"), "title": "One More Time", "duration": 320, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30002"), "title": "Around the World", "duration": 420, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30003"), "title": "Bohemian Rhapsody", "duration": 355, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00002")]}
    ]

    users_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e40001"), "username": "john_doe", "password": "hashed_password_goes_here", "email": "john@example.com"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e40002"), "username": "jane_doe", "password": "hashed_password_goes_here", "email": "jane@example.com"}
    ]

    db["genres"].delete_many({})
    db["artists"].delete_many({})
    db["albums"].delete_many({})
    db["songs"].delete_many({})
    db["users"].delete_many({})

    db["genres"].insert_many(genres_data)
    db["artists"].insert_many(artists_data)
    db["albums"].insert_many(albums_data)
    db["songs"].insert_many(songs_data)
    db["users"].insert_many(users_data)

    for song in songs_data:
        db["albums"].update_one(
            {"_id": song["album_id"]},
            {"$push": {"song_ids": song["_id"]}}
        )

    return {"message": "Database seeded successfully! Collections created and data inserted."}
