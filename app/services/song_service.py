from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models import Song, Album, Genre
from schemas import SongCreateSchema


class SongService:
    @staticmethod
    def add_song_to_album(album_id: int, song_data: SongCreateSchema, db: Session = Depends(get_db)):
        try:
            album_id_int = int(album_id)
            artist_id_int = int(song_data.artist_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Format d'id d'album ou d'artiste invalide"
            )
        
        # Verify album exists
        album = db.query(Album).filter(Album.id == album_id_int).first()
        if not album:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Album non trouvé"
            )
            
        # Create a new song object
        new_song = Song(
            title=song_data.title,
            duration=song_data.duration,
            artist_id=artist_id_int,
            album_id=album_id_int
        )
        
        # Add genres if any
        if song_data.genres:
            genre_objs = []
            for genre_id in song_data.genres:
                try:
                    genre_id_int = int(genre_id)
                    genre = db.query(Genre).filter(Genre.id == genre_id_int).first()
                    if genre:
                        genre_objs.append(genre)
                except ValueError:
                    # Skip invalid genre IDs
                    pass
                    
            new_song.genres = genre_objs
            
        # Add the song to the database
        db.add(new_song)
        db.commit()
        db.refresh(new_song)

        return new_song.id
