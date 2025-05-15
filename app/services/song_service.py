from bson import ObjectId
from fastapi import HTTPException, status
from config.database import db
from schemas import SongCreateSchema


class SongService:
    @staticmethod
    def add_song_to_album(album_id: str, song_data: SongCreateSchema):
        if not ObjectId.is_valid(album_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format d'id d'album invalide"
            )
        album = db["albums"].find_one({"_id": ObjectId(album_id)})
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album non trouvé"
            )

        song_data = song_data.dict()

        if not ObjectId.is_valid(song_data["artist_id"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format d'ObjectId invalide pour artist_id"
            )
        song_data["album_id"] = ObjectId(album_id)
        song_data["artist_id"] = ObjectId(song_data["artist_id"])
        song_data["genres"] = [ObjectId(genre) for genre in song_data.get("genres", [])]

        result = db["songs"].insert_one(song_data)
        inserted_id = result.inserted_id

        db["albums"].update_one(
            {"_id": ObjectId(album_id)},
            {"$push": {"song_ids": inserted_id}}
        )

        return inserted_id
