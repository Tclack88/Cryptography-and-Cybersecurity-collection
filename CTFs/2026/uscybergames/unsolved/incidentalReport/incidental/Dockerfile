FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static

EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
