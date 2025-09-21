# Meal Calorie Backend (FastAPI) - v2 (Stable)

## Overview
FastAPI backend that searches USDA FoodData Central for foods and returns calories per serving and total calories.

## Quick start (local, SQLite)
1. Create virtualenv and activate:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy .env.example to .env and fill USDA_API_KEY and JWT_SECRET
   ```bash
   cp .env.example .env
   ```
4. Run the app:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. Open Swagger: http://localhost:8000/docs

## Run tests (uses HTTP mocking)
```bash
pytest -q
```

## Docker
Build and run:
```bash
docker build -t meal-backend .
docker run -p 8000:8000 --env-file .env meal-backend
```
Or use docker-compose:
```bash
docker-compose up --build
```
