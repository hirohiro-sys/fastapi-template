from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

# ユーザーのデータベースORMモデル
class User(Base):
    __tablename__ = "users" # テーブル名を明示的に指定

    id = Column(Integer, primary_key=True, index=True) # 主キー、自動増分ID
    email = Column(String(255), unique=True, index=True, nullable=False) # メールアドレス（必須、ユニーク）
    hashed_password = Column(String(255), nullable=False) # ハッシュ化されたパスワード（必須）
    is_active = Column(Boolean, default=True) # アカウント有効フラグ（デフォルトTrue）
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 作成日時（DBで自動生成）