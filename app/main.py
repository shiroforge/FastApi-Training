# app/main.py
from fastapi import FastAPI

app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application example",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello FastAPI World!"}

# APIのバージョニング例
@app.get("/api/v1/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}