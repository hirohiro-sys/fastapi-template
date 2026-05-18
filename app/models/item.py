from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func # データベース関数（例: func.now()）を使うためにインポート
from app.db.session import Base # Baseクラスを継承してORMモデルを定義

# 商品のデータベースORMモデル
class Item(Base):
    # (1) データベース上でのテーブル名を明示的に指定
    # Pythonのクラス名（単数形）とDBのテーブル名（複数形）の慣習の違いに対応
    __tablename__ = "items"

    # (2) カラム（列）の定義。実際のDBの型と制約を記述
    id = Column(Integer, primary_key=True, index=True) # 主キー、整数、自動インデックス
    title = Column(String(100), index=True, nullable=False) # 商品名、文字列(最大100文字)、インデックス付き、NULL不可
    description = Column(String(500)) # 商品説明、文字列(最大500文字)
    price = Column(Integer, nullable=False) # 価格、整数、NULL不可

    # (3) 作成日時をサーバー側で自動付与する設定
    # 実務において、データが「いつ作られたか」を記録しておくことは必須
    # タイムゾーン情報を持つDateTime型、デフォルト値をDBのNOW関数で自動設定
    created_at = Column(DateTime(timezone=True), server_default=func.now())