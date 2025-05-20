from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime
from passlib.hash import bcrypt

from config.database import get_db
from models import Genre, Artist, Album, Song, User, song_genre

router = APIRouter()

DEFAULT_COVER_IMAGE = "http://example.com/images/default_cover.png"

@router.post("/seed")
def seed_db(db: Session = Depends(get_db)):
    # Delete existing data - ordre important pour respecter les contraintes de clé étrangère
    try:
        # Supprimer d'abord les tables d'association (relations many-to-many)
        db.execute(song_genre.delete())
        db.commit()
        
        # Puis supprimer les entités dans l'ordre inverse de leurs dépendances
        db.query(Song).delete()
        db.commit()
        db.query(Album).delete()
        db.commit()
        db.query(Artist).delete() 
        db.commit()
        db.query(Genre).delete()
        db.commit()
        db.query(User).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
    
    # Create genres
    genres_data = [
        {"title": "Pop", "description": "Musique populaire"},
        {"title": "Rock", "description": "Musique rock"},
        {"title": "Electro", "description": "Musique électronique"}
    ]
    genres = []
    for genre_data in genres_data:
        genre = Genre(**genre_data)
        db.add(genre)
        genres.append(genre)
    db.commit()
    
    # Create artists
    artists_data = [
        {"name": "Daft Punk", "avatar": "http://example.com/images/daftpunk.png", "biography": "Duo de musique électronique français"},
        {"name": "Queen", "avatar": "http://example.com/images/queen.png", "biography": "Groupe de rock britannique formé en 1970"},
        {"name": "The Weeknd", "avatar": "http://example.com/images/theweeknd.png", "biography": "Chanteur et producteur canadien de R&B"}
    ]
    artists = []
    for artist_data in artists_data:
        artist = Artist(**artist_data)
        db.add(artist)
        artists.append(artist)
    db.commit()
    
    # Create albums
    albums_data = [
        {"title": "Discovery", "cover_image": DEFAULT_COVER_IMAGE, "release_date": datetime.date(2001, 3, 12), "artist_id": artists[0].id},
        {"title": "A Night at the Opera", "cover_image": DEFAULT_COVER_IMAGE, "release_date": datetime.date(1975, 11, 21), "artist_id": artists[1].id},
        {"title": "After Hours", "cover_image": DEFAULT_COVER_IMAGE, "release_date": datetime.date(2020, 3, 20), "artist_id": artists[2].id},
        {"title": "Random Access Memories", "cover_image": DEFAULT_COVER_IMAGE, "release_date": datetime.date(2013, 5, 17), "artist_id": artists[0].id}
    ]
    albums = []
    for album_data in albums_data:
        album = Album(**album_data)
        db.add(album)
        albums.append(album)
    db.commit()
    
    # Create songs
    songs_data = [
        {"title": "One More Time", "duration": 320, "artist_id": artists[0].id, "album_id": albums[0].id, "genres": [genres[2]]},
        {"title": "Aerodynamic", "duration": 210, "artist_id": artists[0].id, "album_id": albums[0].id, "genres": [genres[2]]},
        {"title": "Harder, Better, Faster, Stronger", "duration": 230, "artist_id": artists[0].id, "album_id": albums[0].id, "genres": [genres[2]]},
        {"title": "Digital Love", "duration": 250, "artist_id": artists[0].id, "album_id": albums[0].id, "genres": [genres[2]]},
        {"title": "Bohemian Rhapsody", "duration": 355, "artist_id": artists[1].id, "album_id": albums[1].id, "genres": [genres[1]]},
        {"title": "Love of My Life", "duration": 240, "artist_id": artists[1].id, "album_id": albums[1].id, "genres": [genres[1]]},
        {"title": "You're My Best Friend", "duration": 210, "artist_id": artists[1].id, "album_id": albums[1].id, "genres": [genres[1]]},
        {"title": "The Prophet's Song", "duration": 370, "artist_id": artists[1].id, "album_id": albums[1].id, "genres": [genres[1]]}
    ]
    
    for song_data in songs_data:
        genres_list = song_data.pop("genres")
        song = Song(**song_data)
        song.genres = genres_list
        db.add(song)
    
    db.commit()

    return {"message": "Base de données vidée et re-remplie avec succès!"}
