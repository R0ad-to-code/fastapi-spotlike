# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from config.database import engine, Base
from services.jwt_service import JWTService
from routers import users, genres, albums, artists, seed

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spotilike API",
    description="API REST pour la plateforme Spotilike",
    version="1.0.0",
    openapi_url="/api/openapi.json",   # Déplacer l'OpenAPI JSON sous /api
    docs_url="/docs",                  # Garder le Swagger UI à /docs
    swagger_ui_parameters={"defaultModelsExpandDepth": -1, "docExpansion": "none"}
)

# Configuration CORS
# Autoriser à la fois localhost et le domaine du load balancer
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:4200,http://spotlike-alb-699237754.eu-west-3.elb.amazonaws.com,*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API Spotilike"}

@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# Register the routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(genres.router, prefix="/api", tags=["genres"])
app.include_router(albums.router, prefix="/api", tags=["albums"])
app.include_router(artists.router, prefix="/api", tags=["artists"])
app.include_router(seed.router, prefix="/api", tags=["seed"])
