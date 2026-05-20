from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud import item as item_crud
from app.schemas.item import ItemCreate, ItemResponse
from app.api.deps import get_current_user # 追加: 認証済みユーザー取得の依存性
from app.models.user import User # 追加: Userモデル

router = APIRouter()

# 商品一覧取得エンドポイント (認可不要)
@router.get("/", response_model=list[ItemResponse])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    items = await item_crud.get_items(db, skip=skip, limit=limit)
    return items

# 商品新規作成エンドポイント (ログイン必須)
@router.post("/", response_model=ItemResponse)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db),
    # 【重要】この一行で「ログイン必須」になる
    current_user: User = Depends(get_current_user) # 依存性注入: 認証済みユーザーを取得
):
    # ログインしているユーザーだけがここを通れる
    # current_userオブジェクトを使って、ユーザーに基づいた追加の認可ロジックを実装することも可能
    return await item_crud.create_item(db=db, item=item_in)