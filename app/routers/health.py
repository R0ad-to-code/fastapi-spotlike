from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """
    Vérification de l'état de l'application.
    Cette route est utilisée par les contrôles de santé d'AWS.
    """
    try:
        # Vérifier la connexion à la base de données
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)} 