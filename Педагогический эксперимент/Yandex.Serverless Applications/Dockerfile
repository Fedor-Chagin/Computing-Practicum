FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY *.ttf .
COPY static ./static

RUN mkdir -p static/images
RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
