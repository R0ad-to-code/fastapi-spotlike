# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Spotilike API",
    description="API REST pour la plateforme Spotilike",
    version="1.0.0",
)

# Configuration CORS
cors_origins = os.environ.get("CORS_ORIGINS", "http://localhost:4200").split(",")

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
