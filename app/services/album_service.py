# app/services/album_service.py
from bson import ObjectId
from fastapi import HTTPException, status

from app.config.database import db
from app.schemas import AlbumCreateSchema, AlbumUpdateSchema

class AlbumService:

    @staticmethod
    def get_all_albums():
        albums = list(db["albums"].find())
        for album in albums:
            album["_id"] = str(album["_id"])
            album["artist_id"] = str(album["artist_id"])
            album["song_ids"] = [str(sid) for sid in album.get("song_ids", [])]
        return albums

    @staticmethod
    def get_album_by_id(album_id: str):
        if not ObjectId.is_valid(album_id):
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")
        album = db["albums"].find_one({"_id": ObjectId(album_id)})
        if not album:
            raise HTTPException(status_code=404, detail="Album non trouvé")
        album["_id"] = str(album["_id"])
        album["artist_id"] = str(album["artist_id"])
        album["song_ids"] = [str(sid) for sid in album.get("song_ids", [])]
        return album

    @staticmethod
    def create_album(album: AlbumCreateSchema):
        if db["albums"].find_one({"title": album.title}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Album existe déjà"
            )
        album_dict = album.dict()
        result = db["albums"].insert_one(album_dict)
        return str(result.inserted_id)

    @staticmethod
    def update_album(album_id: str, album_update: AlbumUpdateSchema):
        if not ObjectId.is_valid(album_id):
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")

        album_data = {k: v for k, v in album_update.dict().items() if v is not None}
        if not album_data:
            raise HTTPException(status_code=400, detail="Paramètres d'entrées non valides")

        result = db["albums"].update_one({"_id": ObjectId(album_id)}, {"$set": album_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Album non trouvé")

    @staticmethod
    def delete_album(album_id: str):
        if not ObjectId.is_valid(album_id):
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")

        result = db["albums"].delete_one({"_id": ObjectId(album_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Album non trouvé")
