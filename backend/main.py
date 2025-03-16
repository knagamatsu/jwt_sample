from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
# 相対インポートに変更
from . import models, schemas, auth
from .database import engine, get_db
from sqlalchemy.orm import Session
from typing import Annotated
import traceback

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORSの設定をより詳細に指定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# エラーハンドリングとデバッグ用のミドルウェア
@app.middleware("http")
async def log_requests(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        print(traceback.format_exc())
        raise

# 動作確認用エンドポイント
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# ユーザー登録エンドポイント
@app.post("/api/register", response_model=schemas.User)
async def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # メールアドレスがすでに存在するか確認
        existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # 新しいユーザーの作成 (メールアドレスをユーザー名として使用)
        hashed_password = auth.get_password_hash(user_data.password)
        db_user = models.User(
            email=user_data.email, 
            username=None,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        print(f"ユーザー登録エラー: {str(e)}")
        print(traceback.format_exc())
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@app.post("/api/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return {
        "email": current_user.email,
        "id": current_user.id,
        "username": current_user.username
    }

# デスクトップアプリ統合のため、静的ファイル提供を追加
from fastapi.staticfiles import StaticFiles
import os

# 静的ファイルのディレクトリを確認
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

# スクリプトが直接実行された場合のみサーバーを起動（デスクトップアプリでは使用しない）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
