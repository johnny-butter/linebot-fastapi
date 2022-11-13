FROM python:3.6.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn",  "main:app",  "-k", "uvicorn.workers.UvicornWorker" ]
