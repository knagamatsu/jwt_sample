from sqlalchemy import Column, Integer, String
from .database import Base  # 相対インポートに変更

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, nullable=True)
    hashed_password = Column(String)
