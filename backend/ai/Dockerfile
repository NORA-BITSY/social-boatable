FROM python:3.11-slim-buster

WORKDIR /app

# Use the ai folder for requirements and source files
COPY ai/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai/ .
COPY common/ /app/backend/common

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]
