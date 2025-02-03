erDiagram
    GENRE {
      ObjectId _id PK
      string title
      string description
    }
    
    ARTIST {
      ObjectId _id PK
      string name
      string avatar
      string biography
    }
    
    ALBUM {
      ObjectId _id PK
      string title
      string cover_image
      date release_date
      ObjectId artist_id FK
      array song_ids
    }
    
    SONG {
      ObjectId _id PK
      string title
      int duration
      ObjectId artist_id FK
      ObjectId album_id FK
      array genres
    }
    
    USER {
      ObjectId _id PK
      string username
      string password
      string email
    }
    
    ARTIST ||--o{ ALBUM : "crée"
    ARTIST ||--o{ SONG : "interprète"
    ALBUM ||--o{ SONG : "contient"
    GENRE ||--o{ SONG : "appartient à"
