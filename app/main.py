# app/main.py
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy import Session
from database import get_db,create_tables
from services.crud import create_user

app = FastAPI(
    title="My FastAPI Application",
    description="A simple FastAPI application example",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Hello FastAPI World!"}

# サーバー起動時にテーブル作成
create_tables()

# ユーザー作成エンドポイント
@app.post("/users/")
def create_user_endpoint(username: str, email: str, db: Session = Depends(get_db)):
    try:
        user =  create_user(db, username=username, email=email)
        return {"id": user.id, "username": user.username, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
