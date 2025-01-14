# app/routers/genres.py
from fastapi import APIRouter
from app.services.genre_service import GenreService
from app.schemas import GenreUpdateSchema

router = APIRouter()

@router.get("/genres")
def get_genres():
    return {"genres": GenreService.get_all_genres()}

@router.put("/genres/{id}")
def update_genre(id: str, genre_update: GenreUpdateSchema):
    GenreService.update_genre(id, genre_update)
    return {"message": "Genre mis à jour avec succès", "genres_id": id}
