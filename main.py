from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # 追加: CORSミドルウェアをインポート
from app.api.v1.endpoints import item, auth

app = FastAPI(title="FastAPI Practical Guide")

# 【重要】CORSの設定
# 許可するフロントエンドのURL（オリジン）をリストで指定します
# 本番環境では、localhostではなく実際のフロントエンドのドメインを指定する
origins = [
    "<http://localhost:3000>",  # Reactアプリケーションのデフォルト開発サーバー
    "<http://localhost:5173>",  # Viteアプリケーションのデフォルト開発サーバー
    "<http://127.0.0.1:3000>",  # 多くの環境でlocalhostの代替として使われる
    # "<https://your-frontend-domain.com>", # 本番環境のフロントエンドドメインを追加
]

# CORSMiddlewareをアプリケーションに追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # 許可するオリジンのリスト
    allow_credentials=True, # クッキーやAuthorizationヘッダーなどの認証情報を許可するか
    allow_methods=["*"], # 許可するHTTPメソッド (GET, POST, PUT, DELETE, OPTIONSなど)
    allow_headers=["*"], # 許可するHTTPヘッダー (Content-Type, Authorizationなど)
)

app.include_router(item.router, prefix="/api/v1/items", tags=["items"])
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])