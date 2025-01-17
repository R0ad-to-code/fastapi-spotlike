# app/routers/albums.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId

from app.services.album_service import AlbumService
from app.services.song_service import SongService
from app.services.jwt_service import JWTService
from app.schemas import AlbumCreateSchema, AlbumUpdateSchema, SongCreateSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


@router.get("/albums")
def get_albums():
    return {"albums": AlbumService.get_all_albums()}

@router.get("/albums/{id}")
def get_album(id: str):
    return {"album": AlbumService.get_album_by_id(id)}

@router.get("/albums/{id}/songs")
def get_album_songs(id: str):
    songs = AlbumService.get_album_songs(id)
    return {"songs": songs}

@router.post("/albums")
def add_album(album: AlbumCreateSchema):
    album_id = AlbumService.create_album(album)
    return {"message": "Album ajouté avec succès", "album_id": album_id}

@router.post("/albums/{id}/songs")
def add_song_to_album(id: str, song: SongCreateSchema):
    inserted_id = SongService.add_song_to_album(id, song)
    return {
        "message": "Son ajouté à l'album avec succès",
        "song_id": str(inserted_id),
        "album_id": id
    }

@router.put("/albums/{id}")
def update_album(id: str, album_update: AlbumUpdateSchema):
    AlbumService.update_album(id, album_update)
    return {"message": "Album mis à jour avec succès", "album_id": id}

@router.delete("/albums/{id}")
def delete_album(id: str, token: str = Depends(oauth2_scheme)):
    payload = JWTService.decode_token(token)
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    AlbumService.delete_album(id)
    return {"message": "Album supprimé avec succès", "album_id": id}
