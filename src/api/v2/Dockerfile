FROM python:3.10-slim

WORKDIR /app


COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY models/model.joblib /app/model.joblib

COPY src/api/v2/main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
