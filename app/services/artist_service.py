# app/services/artist_service.py
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models import Artist, Song, Album
from schemas import ArtistUpdateSchema

class ArtistService:

    @staticmethod
    def get_artist_songs(artist_id: int, db: Session = Depends(get_db)):
        try:
            artist_id = int(artist_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if not artist:
            raise HTTPException(status_code=404, detail="Artist non trouvé")

        songs = db.query(Song).filter(Song.artist_id == artist_id).all()
        return songs

    @staticmethod
    def get_artist_by_id(artist_id: int, db: Session = Depends(get_db)):
        try:
            artist_id = int(artist_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'ID d'artiste invalide")
        
        artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if not artist:
            raise HTTPException(status_code=404, detail="Artiste non trouvé")
        
        return artist
    
    @staticmethod
    def update_artist(artist_id: int, artist_update: ArtistUpdateSchema, db: Session = Depends(get_db)):
        try:
            artist_id = int(artist_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        artist_data = {k: v for k, v in artist_update.dict().items() if v is not None}
        if not artist_data:
            raise HTTPException(status_code=400, detail="Paramètres d'entrées non valides")

        artist = db.query(Artist).filter(Artist.id == artist_id).first()
        if not artist:
            raise HTTPException(status_code=404, detail="Artist non trouvé")
            
        for key, value in artist_data.items():
            setattr(artist, key, value)
            
        db.commit()
        db.refresh(artist)
        return artist

    @staticmethod
    def delete_artist(artist_id: int, db: Session = Depends(get_db)):
        try:
            artist_id = int(artist_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Format d'id d'artiste invalide")

        # Delete related songs
        db.query(Song).filter(Song.artist_id == artist_id).delete()
        
        # Delete related albums
        db.query(Album).filter(Album.artist_id == artist_id).delete()
        
        # Delete the artist
        result = db.query(Artist).filter(Artist.id == artist_id).delete()
        if result == 0:
            raise HTTPException(status_code=404, detail="Artist non trouvé")
            
        db.commit()
        return {"message": "Artiste et ses oeuvres supprimés avec succès"}
        
    @staticmethod
    def get_all_artists(db: Session = Depends(get_db)):
        artists = db.query(Artist).all()
        return artists
