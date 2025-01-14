from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

# Définir un PyObjectId personnalisé pour sérialisation
class PyObjectId(ObjectId):
    """Extension de ObjectId pour la sérialisation JSON"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)  # Sérialiser l'ObjectId en string
        raise ValueError("Invalid ObjectId")

# ===========================
#   MODELES Pydantic
# ===========================

class ArtistModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Changer ici
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
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Changer ici
    title: str
    description: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class SongModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Changer ici
    title: str
    duration: int
    artist_id: str
    genres: List[str] = []
    album_id: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class AlbumModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Changer ici
    title: str
    cover_image: Optional[str] = None
    release_date: Optional[str] = None
    artist_id: str
    song_ids: List[str] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")  # Changer ici
    username: str
    password: str
    email: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
