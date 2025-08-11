# app/main.py
from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db,create_tables
from app.services.crud import * 

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

# 全ユーザーを取得　ユーザー作成とはgetとpostで区別している。
@app.get("/users/")
def read_users_endpoint(db: Session = Depends(get_db)):
    users = get_users(db)
    return [{"id": user.id, "username": user.username, "email": user.email} for user in users]

# 特定のユーザーを取得
@app.get("/users/{user_id}")
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "email": user.email}

# ユーザー削除
@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    # ユーザーを削除
    try:
        result = delete_user(db, user_id)
        if not result:
            # 見つからない場合はエラーを返す
            raise HTTPException(status_code=404, detail="User not found")
        # 見つかった場合は削除
        return "delete success"
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ユーザー情報更新
@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, username: str, email: str, db: Session = Depends(get_db)):
    try:
        user = update_user(db, user_id=user_id, username=username, email=email)
        if user is None:
            # 見つからない場合はエラーを返す
            raise HTTPException(status_code=404, detail="User not found")
        # 見つかった場合は、更新
        return {"id": user.id, "username": user.username, "email": user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
