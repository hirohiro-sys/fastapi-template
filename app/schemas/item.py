from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional # Python 3.9以前の場合はtyping.Optionalを使用

# 共通のベーススキーマ
# 商品の基本的な属性を定義し、再利用性を高める
class ItemBase(BaseModel):
    # 商品名: 必須、文字列、長さ1〜100文字のバリデーション
    # description引数はSwagger UIのドキュメントに表示される
    title: str = Field(..., min_length=1, max_length=100, description="商品名")
    # 価格: 必須、整数、0より大きい値のバリデーション
    price: int = Field(..., gt=0, description="価格(0円より大きいこと)")

# ユーザーからデータを受け取るときに使用するスキーマ（作成時）
# ItemBaseを継承し、新しい項目を追加または上書きする
class ItemCreate(ItemBase):
    # 商品説明: オプション、文字列、最大500文字
    # Noneはdescriptionがオプションであることを示す
    description: Optional[str] = Field(None, max_length=500)

# ユーザーにデータを返すときに使用するスキーマ（レスポンス時）
# ItemBaseを継承し、データベースで生成されるIDと作成日時を追加
class ItemResponse(ItemBase):
    id: int # データベースで自動生成されるID
    created_at: datetime # データベースで自動生成される作成日時

    # SQLAlchemyのモデル (ORM) をPydanticスキーマに変換するための設定
    # これにより、DBから取得したORMオブジェクトを直接Pydanticスキーマとして扱える
    model_config = {"from_attributes": True}