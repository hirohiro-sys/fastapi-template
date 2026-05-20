from sqlalchemy.ext.asyncio import AsyncSession # 非同期セッション
from sqlalchemy.future import select # SQLAlchemy 2.0のSELECT文構築
from app.models.item import Item # Item ORMモデル
from app.schemas.item import ItemCreate # Item作成用スキーマ

# IDを指定して1件取得
async def get_item(db: AsyncSession, item_id: int):
    # 非同期での検索クエリ実行: Itemモデルからitem_idでフィルタリング
    result = await db.execute(select(Item).filter(Item.id == item_id))
    # 結果から単一のスカラー値（Itemオブジェクト）を取得
    return result.scalars().first()

# 商品一覧を取得（オフセットと上限を指定可能にするのが一般的です）
async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    # 非同期での検索クエリ実行: オフセットとリミットを適用して一覧取得
    result = await db.execute(select(Item).offset(skip).limit(limit))
    # 結果から複数のスカラー値（Itemオブジェクトのリスト）を取得
    return result.scalars().all()

# 新規作成
async def create_item(db: AsyncSession, item: ItemCreate):
    # PydanticスキーマからSQLAlchemy ORMモデルのインスタンスを作成
    # これがschemasとmodelsの橋渡しとなる
    db_item = Item(
        title=item.title,
        price=item.price,
        description=item.description
    )
    # データベースセッションに新しいアイテムを追加
    db.add(db_item)
    # トランザクションをコミットし、変更を永続化
    await db.commit()
    # 自動採番されたIDやcreated_atなどを取得するため、ORMオブジェクトをリフレッシュ
    await db.refresh(db_item)
    # 作成されたORMオブジェクトを返す
    return db_item