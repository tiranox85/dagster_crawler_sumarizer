
## Overview

This project fetches press releases from the SEC using an Apify scraper, summarizes unseen articles with 
OpenAI's `gpt-4o-mini` model, stores them in Postgres, and serves them via Dagster assets. The pipeline runs every 15 minutes and avoids double-processing.

---

## Environment Variables

Set the following variables before running:

```bash
export DATABASE_URL="postgresql+psycopg2://postgres:postgres@postgres:5432/pressdb"
export APIFY_ACTOR_ID="your_apify_actor_id"
export APIFY_API_TOKEN="your_apify_api_token"
export OPENAI_API_KEY="your_openai_api_key"
```

Or include them in `docker-compose.yml`.

---

## Setup

### 1. Build Docker Containers

```bash
docker compose build
```

### 2. Start Services

```bash
docker compose up -d
```

### 3. Run Migrations

```bash
docker compose exec dagster alembic -c /app/alembic.ini upgrade head
```

### 4. Run Tests

```bash
docker exec -it <container-name> bash
cd /app
PYTHONPATH=/app pytest -v
```

### 5. Next Steps

* Make apify actor to work properly, right now id defaulting to mock data, that works for testing purposes
* Add better tests
* Remove the hardcoded values for Apify actor id and openai model name
* Add logging
* Add error handling

---

* Postgres database will run on `localhost:5432`
* Dagster UI will be available at `http://localhost:3000`


* Visit `http://localhost:3000` to see asset graph and schedule.
* Ensure the `every_15m` schedule is ticking.

---

