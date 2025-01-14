# app/routers/seed.py
from fastapi import APIRouter
from bson import ObjectId
from passlib.hash import bcrypt

from app.config.database import db

router = APIRouter()

@router.post("/seed")
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

    # Hash des mots de passe
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
