from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLiteデータベース設定
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# データベースエンジンを作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッションファクトリを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデル作成用のベースクラス
Base = declarative_base()

# セッション依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
