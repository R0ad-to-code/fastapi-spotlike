# app/routers/genres.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services.genre_service import GenreService
from schemas import GenreUpdateSchema
from config.database import get_db

router = APIRouter()

@router.get("/genres")
def get_genres(db: Session = Depends(get_db)):
    return {"genres": GenreService.get_all_genres(db)}

@router.put("/genres/{id}")
def update_genre(id: int, genre_update: GenreUpdateSchema, db: Session = Depends(get_db)):
    GenreService.update_genre(id, genre_update, db)
    return {"message": "Genre mis à jour avec succès", "genres_id": id}
