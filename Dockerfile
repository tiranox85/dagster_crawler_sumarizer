FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
COPY . /app

RUN mkdir -p /app/dagster_home

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 3000 4000

CMD ["dagster", "dev", "-h", "0.0.0.0"]
