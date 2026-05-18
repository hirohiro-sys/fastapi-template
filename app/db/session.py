from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings # 秘密情報は.envからcore/config経由で読み込む

# 非同期用エンジンの作成
# settings.DATABASE_URLからDB接続文字列を取得
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,          # 開発中はSQLログを出力し、デバッグを効率化
    pool_pre_ping=True, # 接続切れを自動検知する、実務で必須の安定化設定
    # その他のオプション: pool_size, max_overflowなど、必要に応じて調整
)

# セッション作成ファクトリ
# このファクトリを使ってAsyncSessionのインスタンスを生成
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False, # コミット後もオブジェクトを保持し、非同期特有のエラーを回避
)

# モデルのベースクラス (models/ ディレクトリで使用)
# すべてのORMモデルはこのクラスを継承する
class Base(DeclarativeBase):
    pass

# FastAPIのDependsで使用する、DBセッション取得用のジェネレータ関数
# 各リクエストで新しいDBセッションを提供し、終了時に適切にクローズ
async def get_db():
    async with async_session() as session:
        try:
            yield session # FastAPIにセッションを供給（自動セッション管理）
            await session.commit() # トランザクションをコミット
        except Exception:
            await session.rollback() # 万が一エラー時は自動で巻き戻し、データを保護
            raise # 例外を再スローし、FastAPIのHTTPExceptionハンドラーに委ねる
        finally:
            await session.close() # 処理が終われば確実に接続を閉じ、リソースを解放する