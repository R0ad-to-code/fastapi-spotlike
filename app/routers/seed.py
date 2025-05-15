from fastapi import APIRouter
from bson import ObjectId
from passlib.hash import bcrypt

from config.database import db

router = APIRouter()

DEFAULT_COVER_IMAGE = "http://example.com/images/default_cover.png"

@router.post("/seed")
def seed_db():
    collections = ["genres", "artists", "albums", "songs"]
    for collection in collections:
        db[collection].delete_many({})
    
    genres_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00001"), "title": "Pop", "description": "Musique populaire"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00002"), "title": "Rock", "description": "Musique rock"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e00003"), "title": "Electro", "description": "Musique électronique"}
    ]
    db["genres"].insert_many(genres_data)

    artists_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "name": "Daft Punk", "avatar": "http://example.com/images/daftpunk.png", "biography": "Duo de musique électronique français"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "name": "Queen", "avatar": "http://example.com/images/queen.png", "biography": "Groupe de rock britannique formé en 1970"},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e10003"), "name": "The Weeknd", "avatar": "http://example.com/images/theweeknd.png", "biography": "Chanteur et producteur canadien de R&B"}
    ]
    db["artists"].insert_many(artists_data)

    albums_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "title": "Discovery", "cover_image": DEFAULT_COVER_IMAGE, "release_date": "2001-03-12", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "song_ids": []},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "title": "A Night at the Opera", "cover_image": DEFAULT_COVER_IMAGE, "release_date": "1975-11-21", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "song_ids": []},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20003"), "title": "After Hours", "cover_image": DEFAULT_COVER_IMAGE, "release_date": "2020-03-20", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10003"), "song_ids": []},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e20004"), "title": "Random Access Memories", "cover_image": DEFAULT_COVER_IMAGE, "release_date": "2013-05-17", "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "song_ids": []}
    ]
    db["albums"].insert_many(albums_data)
    
    songs_data = [
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30001"), "title": "One More Time", "duration": 320, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30002"), "title": "Aerodynamic", "duration": 210, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30003"), "title": "Harder, Better, Faster, Stronger", "duration": 230, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30004"), "title": "Digital Love", "duration": 250, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10001"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20001"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00003")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30005"), "title": "Bohemian Rhapsody", "duration": 355, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00002")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30006"), "title": "Love of My Life", "duration": 240, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00002")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30007"), "title": "You're My Best Friend", "duration": 210, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00002")]},
        {"_id": ObjectId("64b2bfcf9ba85bceb3e30008"), "title": "The Prophet's Song", "duration": 370, "artist_id": ObjectId("64b2bfcf9ba85bceb3e10002"), "album_id": ObjectId("64b2bfcf9ba85bceb3e20002"), "genres": [ObjectId("64b2bfcf9ba85bceb3e00002")]}
    ]

    db["songs"].insert_many(songs_data)

    for song in songs_data:
        db["albums"].update_one({"_id": song["album_id"]}, {"$push": {"song_ids": song["_id"]}})

    return {"message": "Base de données vidée et re-remplie avec succès!"}
