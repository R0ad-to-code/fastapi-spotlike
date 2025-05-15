# app/services/genre_service.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from models import Genre
from schemas import GenreUpdateSchema

class GenreService:

    @staticmethod
    def get_all_genres(db: Session = Depends(get_db)):
        genres = db.query(Genre).all()
        return genres

    @staticmethod
    def update_genre(genre_id: int, genre_update: GenreUpdateSchema, db: Session = Depends(get_db)):
        try:
            genre_id_int = int(genre_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id de genre invalide")

        genre_data = {k: v for k, v in genre_update.dict().items() if v is not None}
        if not genre_data:
            raise HTTPException(status_code=400, detail="Paramètres d'entrées non valides")

        genre = db.query(Genre).filter(Genre.id == genre_id_int).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre non trouvé")
            
        for key, value in genre_data.items():
            setattr(genre, key, value)
            
        db.commit()
        return genre
