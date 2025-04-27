FROM python:3.11-slim-buster

WORKDIR /app

COPY social/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY social/ .
COPY common/ /app/backend/common

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
