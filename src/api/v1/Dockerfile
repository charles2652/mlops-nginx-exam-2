FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY src/api/v1 /app

#  Copier le modèle ML
COPY model/model.joblib /app/model.joblib

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
