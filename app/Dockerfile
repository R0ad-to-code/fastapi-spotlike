FROM --platform=linux/amd64 python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier tous les fichiers nécessaires
COPY alembic.ini /app/
COPY alembic/ /app/alembic/
COPY app/ /app/

EXPOSE 8000

# Démarrer directement l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
