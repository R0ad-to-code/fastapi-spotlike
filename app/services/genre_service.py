# app/services/genre_service.py
from bson import ObjectId
from fastapi import HTTPException

from app.config.database import db
from app.schemas import GenreUpdateSchema

class GenreService:

    @staticmethod
    def get_all_genres():
        genres = list(db["genres"].find())
        for genre in genres:
            genre["_id"] = str(genre["_id"])
        return genres

    @staticmethod
    def update_genre(genre_id: str, genre_update: GenreUpdateSchema):
        if not ObjectId.is_valid(genre_id):
            raise HTTPException(status_code=400, detail="Format d'id de genre invalide")

        genre_data = {k: v for k, v in genre_update.dict().items() if v is not None}
        if not genre_data:
            raise HTTPException(status_code=400, detail="Paramètres d'entrées non valides")

        result = db["genres"].update_one({"_id": ObjectId(genre_id)}, {"$set": genre_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Genre non trouvé")
