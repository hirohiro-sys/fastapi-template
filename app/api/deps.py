from fastapi import Depends, HTTPException, status # FastAPIの依存性注入とエラーハンドリング
from fastapi.security import OAuth2PasswordBearer # OAuth2Bearerトークンからのトークン抽出
from jose import jwt, JWTError # JWTのデコードとエラーハンドリング
from sqlalchemy.ext.asyncio import AsyncSession # 非同期セッション
from sqlalchemy.future import select # SQLAlchemy 2.0のSELECT文構築
from app.db.session import get_db # DBセッションの依存性注入
from app.core import security # カスタムセキュリティモジュール
from app.models.user import User # User ORMモデル

# ログインURLを指定。これでSwagger UIに「鍵マーク」が出現します
# AuthorizationヘッダーからBearerトークンを抽出するOAuth2スキーマ
oauth2_scheme = OAuth2PasswordBearer (tokenUrl="/api/v1/login")

# 現在のユーザーを取得するための依存性関数
# 認証されたユーザーオブジェクトを返す
async def get_current_user(
    db: AsyncSession = Depends(get_db), # DBセッションを注入
    token: str = Depends(oauth2_scheme) # AuthorizationヘッダーからJWTトークンを抽出
) -> User:
    # 認証情報が無効な場合に発生させる例外
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, # HTTP 401 Unauthorized
        detail="認証資格情報が検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"}, # OAuth2標準に準拠
    )
    try:
        # JWTトークンを解読(デコード)
        # SECRET_KEYとALGORITHMを使って署名を検証し、ペイロードを抽出
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub") # トークンからユーザーのメールアドレス（subクレーム）を取得
        if email is None: # メールアドレスがない場合、認証情報が無効
            raise credentials_exception
    except JWTError: # JWTの検証に失敗した場合（署名無効、期限切れなど）
        raise credentials_exception

    # DBからユーザー情報を取得
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()

    if user is None: # ユーザーが見つからない場合、認証情報が無効
        raise credentials_exception
    return user # 認証されたユーザーオブジェクトを返す