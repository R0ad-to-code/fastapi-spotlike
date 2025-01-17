# app/routers/artists.py
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.artist_service import ArtistService
from app.services.jwt_service import JWTService
from app.schemas import ArtistUpdateSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")

@router.get("/artists/{id}/songs")
def get_artist_songs(id: str):
    songs = ArtistService.get_artist_songs(id)
    return {"songs": songs}

@router.get("/artists/{id}")
def get_album(id: str):
    return {"artist": ArtistService.get_artist_by_id(id)}

@router.put("/artists/{id}")
def update_artist(id: str, artist_update: ArtistUpdateSchema):
    ArtistService.update_artist(id, artist_update)
    return {"message": "Artiste mis à jour avec succès", "artist_id": id}

@router.delete("/artists/{id}")
def delete_artist(id: str, token: str = Depends(oauth2_scheme)):
    payload = JWTService.decode_token(token)
    user_id_from_token = payload.get("user_id")
    if not user_id_from_token:
        raise HTTPException(status_code=401, detail="Token invalide")

    ArtistService.delete_artist(id)
    return {"message": "Artiste supprimé avec succès", "artist_id": id}

@router.get("/artists")
def get_all_artists():
    artists = ArtistService.get_all_artists()
    return {"artists": artists}
