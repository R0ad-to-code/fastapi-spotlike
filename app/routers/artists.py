# app/routers/artists.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from services.artist_service import ArtistService
from services.jwt_service import JWTService
from schemas import ArtistUpdateSchema
from config.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

@router.get("/artists/{id}/songs")
def get_artist_songs(id: int, db: Session = Depends(get_db)):
    songs = ArtistService.get_artist_songs(id, db)
    return {"songs": songs}

@router.get("/artists/{id}")
def get_artist(id: int, db: Session = Depends(get_db)):
    return {"artist": ArtistService.get_artist_by_id(id, db)}

@router.put("/artists/{id}")
def update_artist(id: int, artist_update: ArtistUpdateSchema, db: Session = Depends(get_db)):
    ArtistService.update_artist(id, artist_update, db)
    return {"message": "Artiste mis à jour avec succès", "artist_id": id}

@router.delete("/artists/{id}")
def delete_artist(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = JWTService.decode_token(token)
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    result = ArtistService.delete_artist(id, db)
    return {"message": "Artiste supprimé avec succès", "artist_id": id}

@router.get("/artists")
def get_all_artists(db: Session = Depends(get_db)):
    artists = ArtistService.get_all_artists(db)
    return {"artists": artists}
