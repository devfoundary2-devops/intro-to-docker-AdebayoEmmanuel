from fastapi import FastAPI, HTTPException
import redis
import os
import psycopg2

app = FastAPI()

# Redis connection
try:
    r = redis.Redis(host="cache", port=6379, decode_responses=True)
    r.ping()
except Exception:
    r = None

# Postgres connection
def get_db():
    try:
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        return conn
    except Exception:
        return None

@app.get("/cache/{key}")
def cache_get(key: str):
    if not r:
        raise HTTPException(status_code=503, detail="Redis not available")
    val = r.get(key)
    return {"key": key, "value": val}

@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r:
        raise HTTPException(status_code=503, detail="Redis not available")
    r.set(key, value)
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}