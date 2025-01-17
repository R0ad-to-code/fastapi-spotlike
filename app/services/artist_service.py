# app/services/artist_service.py
from bson import ObjectId
from fastapi import HTTPException
from typing import List, Dict

from app.config.database import db
from app.schemas import ArtistUpdateSchema

class ArtistService:

    @staticmethod
    def get_artist_songs(artist_id: str):
        if not ObjectId.is_valid(artist_id):
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        artist = db["artists"].find_one({"_id": ObjectId(artist_id)})
        if not artist:
            raise HTTPException(status_code=404, detail="Artist non trouvé")

        songs = list(db["songs"].find({"artist_id": ObjectId(artist_id)}))
        for song in songs:
            song["_id"] = str(song["_id"])
            song["artist_id"] = str(song["artist_id"])
            song["album_id"] = str(song["album_id"])
            song["genres"] = [str(genre_id) for genre_id in song.get("genres", [])]
        return songs

    @staticmethod
    def get_artist_by_id(artist_id: str):
        # Validation de l'ID de l'artiste
        if not ObjectId.is_valid(artist_id):
            raise HTTPException(status_code=400, detail="Format d'ID d'artiste invalide")
        
        # Recherche de l'artiste dans la collection "artists"
        artist = db["artists"].find_one({"_id": ObjectId(artist_id)})
        if not artist:
            raise HTTPException(status_code=404, detail="Artiste non trouvé")
        
        # Formatage des champs de l'artiste
        artist["_id"] = str(artist["_id"])
        
        return {
            "_id": artist["_id"],
            "name": artist.get("name"),
            "avatar": artist.get("avatar"),
            "biography": artist.get("biography"),
        }
    
    @staticmethod
    def update_artist(artist_id: str, artist_update: ArtistUpdateSchema):
        if not ObjectId.is_valid(artist_id):
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        artist_data = {k: v for k, v in artist_update.dict().items() if v is not None}
        if not artist_data:
            raise HTTPException(status_code=400, detail="Paramètres d'entrées non valides")

        result = db["artists"].update_one({"_id": ObjectId(artist_id)}, {"$set": artist_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Artist non trouvé")

    @staticmethod
    def delete_artist(artist_id: str):
        if not ObjectId.is_valid(artist_id):
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        db["songs"].delete_many({"artist_id": ObjectId(artist_id)})
        db["albums"].delete_many({"artist_id": ObjectId(artist_id)})

        result = db["artists"].delete_one({"_id": ObjectId(artist_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Artist non trouvé")
        
    @staticmethod
    def get_all_artists() -> List[Dict]:
        artists = list(db["artists"].find({}))
        for artist in artists:
            artist["_id"] = str(artist["_id"])
        return artists
