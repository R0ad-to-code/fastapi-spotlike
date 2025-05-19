# app/services/album_service.py
from datetime import datetime
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models import Album, Song
from schemas import AlbumCreateSchema, AlbumUpdateSchema

class AlbumService:

    @staticmethod
    def get_all_albums(db: Session = Depends(get_db)):
        albums = db.query(Album).all()
        return albums

    @staticmethod
    def get_album_by_id(album_id: int, db: Session = Depends(get_db)):
        try:
            album_id = int(album_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")
            
        album = db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album non trouvé")
        return album
    
    @staticmethod
    def get_album_songs(album_id: int, db: Session = Depends(get_db)):
        try:
            album_id = int(album_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")

        album = db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album non trouvé")

        songs = db.query(Song).filter(Song.album_id == album_id).all()
        return songs

    @staticmethod
    def create_album(album: AlbumCreateSchema, db: Session = Depends(get_db)):
        try:
            artist_id = int(album.artist_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")
            
        existing_album = db.query(Album).filter(Album.title == album.title).first()
        if existing_album:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Album existe déjà"
            )
            
        # Convert release_date string to date object if provided
        release_date = None
        if album.release_date:
            try:
                release_date = datetime.strptime(album.release_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD")
        
        new_album = Album(
            title=album.title,
            cover_image=album.cover_image,
            release_date=release_date,
            artist_id=artist_id
        )
        
        db.add(new_album)
        db.commit()
        db.refresh(new_album)
        
        return new_album.id

    @staticmethod
    def update_album(album_id: int, album_update: AlbumUpdateSchema, db: Session = Depends(get_db)):
        try:
            album_id = int(album_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")

        album = db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album non trouvé")
            
        update_data = {k: v for k, v in album_update.dict().items() if v is not None}
        
        # Convert release_date string to date object if provided
        if "release_date" in update_data and update_data["release_date"]:
            try:
                update_data["release_date"] = datetime.strptime(update_data["release_date"], "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Format de date invalide. Utilisez YYYY-MM-DD")
        
        for key, value in update_data.items():
            setattr(album, key, value)
            
        db.commit()
        db.refresh(album)
        return album

    @staticmethod
    def delete_album(album_id: int, db: Session = Depends(get_db)):
        try:
            album_id = int(album_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'album invalide")

        album = db.query(Album).filter(Album.id == album_id).first()
        if not album:
            raise HTTPException(status_code=404, detail="Album non trouvé")
        
        # Get the number of songs to be deleted
        songs_count = db.query(Song).filter(Song.album_id == album_id).count()
        
        # Delete associated songs
        db.query(Song).filter(Song.album_id == album_id).delete()
        
        # Delete the album
        db.delete(album)
        db.commit()

        return {"message": f"Album et {songs_count} chanson(s) supprimée(s) avec succès"}
        
