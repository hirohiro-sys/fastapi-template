from fastapi import APIRouter, Depends, HTTPException, status # FastAPIのコア機能
from fastapi.security import OAuth2PasswordRequestForm # OAuth2パスワードフローのフォームデータ処理
from sqlalchemy.ext.asyncio import AsyncSession # 非同期セッション
from sqlalchemy.future import select # SQLAlchemy 2.0のSELECT文構築
from app.db.session import get_db # DBセッションの依存性注入
from app.core import security # カスタムセキュリティモジュール
from app.models.user import User # User ORMモデル

router = APIRouter() # 新しいAPIRouterインスタンスを作成（認証関連エンドポイント用）

# ログインエンドポイント
@router.post("/login")
async def login(
    db: AsyncSession = Depends(get_db), # 依存性注入: DBセッションを取得
    form_data: OAuth2PasswordRequestForm = Depends() # 依存性注入: ログインフォームデータを取得
):
    # メールアドレスでユーザーをデータベースから検索
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()

    # ユーザーが見つからない、またはパスワードが一致しない場合の認証チェック
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        # 認証失敗の場合、401 Unauthorizedエラーを返す
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="メールアドレスまたはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"}, # OAuth2標準に準拠したヘッダー
        )

    # 認証成功の場合、アクセストークンを発行して返す
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}