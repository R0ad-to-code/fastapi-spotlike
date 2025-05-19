from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserCreateSchema(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLoginSchema(BaseModel):
    username: str
    password: str

class AlbumCreateSchema(BaseModel):
    title: str
    cover_image: Optional[str] = None
    release_date: Optional[str] = None
    artist_id: str

class SongCreateSchema(BaseModel):
    title: str
    duration: int
    artist_id: str
    genres: List[str] = []

class ArtistUpdateSchema(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    biography: Optional[str] = None

class AlbumUpdateSchema(BaseModel):
    title: Optional[str] = None
    cover_image: Optional[str] = None
    release_date: Optional[str] = None

class GenreUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
