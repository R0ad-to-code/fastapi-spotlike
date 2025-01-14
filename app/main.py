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

# 1. GET - /api/albums : Récupère la liste de tous les albums
@app.get("/api/albums")
def get_albums():
    albums = list(db["albums"].find())
    for album in albums:
        album["_id"] = str(album["_id"])
        album["artist_id"] = str(album["artist_id"])
        album["song_ids"] = [str(song_id) for song_id in album.get("song_ids", [])]
    return {"albums": albums}

# 2. GET - /api/albums/{id} : Récupère les détails de l’album précisé par :id
@app.get("/api/albums/{id}")
def get_album(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid album ID format")
    album = db["albums"].find_one({"_id": ObjectId(id)})
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    album["_id"] = str(album["_id"])
    album["artist_id"] = str(album["artist_id"])
    album["song_ids"] = [str(song_id) for song_id in album.get("song_ids", [])]
    return {"album": album}

# 3. GET - /api/albums/{id}/songs : Récupère les morceaux de l’album précisé par :id
@app.get("/api/albums/{id}/songs")
def get_album_songs(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid album ID format")
    album = db["albums"].find_one({"_id": ObjectId(id)})
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    songs = list(db["songs"].find({"album_id": ObjectId(id)}))
    for song in songs:
        song["_id"] = str(song["_id"])
        song["artist_id"] = str(song["artist_id"])
        song["album_id"] = str(song["album_id"])
        song["genres"] = [str(genre_id) for genre_id in song.get("genres", [])]
    return {"songs": songs}

# 4. GET - /api/genres : Récupère la liste de tous les genres
@app.get("/api/genres")
def get_genres():
    genres = list(db["genres"].find())
    for genre in genres:
        genre["_id"] = str(genre["_id"])
    return {"genres": genres}

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
        {"_id": ObjectId("64b2bfcf9ba85bceb3e40001"), "username": "john_doe", "password": "password", "email": "john@example.com"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e40002"), "username": "jane_doe", "password": "password", "email": "jane@example.com"}
    ]

    for user in users_data:
        user["password"] = bcrypt.hash(user["password"])

    collections = {
        "genres": genres_data,
        "artists": artists_data,
        "albums": albums_data,
        "songs": songs_data,
        "users": users_data
    }

    for collection_name, data in collections.items():
        existing_count = db[collection_name].count_documents({})
        if existing_count > 0:
            print(f"{collection_name.capitalize()} contient {existing_count} document(s). Suppression en cours...")
            db[collection_name].delete_many({})
            print(f"Collection {collection_name} vidée.")
        else:
            print(f"Collection {collection_name} est vide.")

        db[collection_name].insert_many(data)
        print(f"Collection {collection_name} peuplée avec {len(data)} document(s).")

    for song in songs_data:
        db["albums"].update_one(
            {"_id": song["album_id"]},
            {"$push": {"song_ids": song["_id"]}}
        )
        print(f"Ajout du morceau '{song['title']}' à l'album ID {song['album_id']}.")

    return {"message": "Données insérées avec succès!"}