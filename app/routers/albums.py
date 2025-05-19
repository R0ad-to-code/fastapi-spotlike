# app/routers/albums.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from services.album_service import AlbumService
from services.song_service import SongService
from services.jwt_service import JWTService
from schemas import AlbumCreateSchema, AlbumUpdateSchema, SongCreateSchema
from config.database import get_db

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


@router.get("/albums")
def get_albums(db: Session = Depends(get_db)):
    return {"albums": AlbumService.get_all_albums(db)}

@router.get("/albums/{id}")
def get_album(id: int, db: Session = Depends(get_db)):
    return {"album": AlbumService.get_album_by_id(id, db)}

@router.get("/albums/{id}/songs")
def get_album_songs(id: int, db: Session = Depends(get_db)):
    songs = AlbumService.get_album_songs(id, db)
    return {"songs": songs}

@router.post("/albums")
def add_album(album: AlbumCreateSchema, db: Session = Depends(get_db)):
    album_id = AlbumService.create_album(album, db)
    return {"message": "Album ajouté avec succès", "album_id": album_id}

@router.post("/albums/{id}/songs")
def add_song_to_album(id: int, song: SongCreateSchema, db: Session = Depends(get_db)):
    inserted_id = SongService.add_song_to_album(id, song, db)
    return {
        "message": "Son ajouté à l'album avec succès",
        "song_id": inserted_id,
        "album_id": id
    }

@router.put("/albums/{id}")
def update_album(id: int, album_update: AlbumUpdateSchema, db: Session = Depends(get_db)):
    AlbumService.update_album(id, album_update, db)
    return {"message": "Album mis à jour avec succès", "album_id": id}

@router.delete("/albums/{id}")
def delete_album(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = JWTService.decode_token(token)
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    result = AlbumService.delete_album(id, db)
    return {"message": "Album supprimé avec succès", "album_id": id}
