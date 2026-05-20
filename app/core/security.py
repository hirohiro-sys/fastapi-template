from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError # JWTの生成と検証のためのライブラリ
from passlib.context import CryptContext # パスワードハッシュ化のためのライブラリ

# パスワードハッシュ化の設定
# bcryptスキームを使用し、古いハッシュ形式にも対応
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWTの設定（実務ではこれらも環境変数から読み込みます）
# 【重要】本番環境では、SECRET_KEYは環境変数から安全に取得すべき
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256" # JWT署名に使用するアルゴリズム
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # アクセストークンの有効期限（30分）

# 平文パスワードとハッシュ済みパスワードが一致するかを照合する
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# パスワードをハッシュ化する
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# JWTトークン(入館証)を発行する
def create_access_token(data: dict):
    to_encode = data.copy() # JWTペイロードに含めるデータをコピー
    # 有効期限をUTCで現在時刻 + ACCESS_TOKEN_EXPIRE_MINUTES に設定
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # ペイロードに有効期限(exp)を追加
    # JWTをエンコードして返す
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)