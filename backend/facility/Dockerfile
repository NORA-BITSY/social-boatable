FROM python:3.11-slim-buster

WORKDIR /app

# Use the facility folder for requirements and source files
COPY facility/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY facility/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
