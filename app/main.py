# app/main.py
from fastapi import FastAPI
from app.services.jwt_service import JWTService
from app.routers import users, albums, genres, artists, seed
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Spotilike API",
    description="API REST pour la plateforme Spotilike",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Adresse de ton frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(albums.router, prefix="/api", tags=["Albums"])
app.include_router(genres.router, prefix="/api", tags=["Genres"])
app.include_router(artists.router, prefix="/api", tags=["Artists"])
app.include_router(seed.router, prefix="/api", tags=["Seed"])

app.openapi = lambda: JWTService.custom_openapi(app)
