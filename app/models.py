from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

# Astuce pour manipuler l'_id de MongoDB avec Pydantic
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

# ===========================
#   MODELES Pydantic
# ===========================

class ArtistModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    avatar: Optional[str] = None
    biography: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Daft Punk",
                "avatar": "http://example.com/images/daftpunk.png",
                "biography": "Duo de musique électronique français."
            }
        }


class GenreModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class SongModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    duration: int
    artist_id: str
    genres: List[str] = []
    album_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class AlbumModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    cover_image: Optional[str] = None
    release_date: Optional[str] = None
    artist_id: str
    song_ids: List[str] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    password: str
    email: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
