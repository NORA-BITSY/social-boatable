FROM python:3.11-slim-buster

WORKDIR /app

COPY marketplace/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY marketplace/ .
COPY common/ /app/backend/common
COPY social/ /app/backend/social

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
