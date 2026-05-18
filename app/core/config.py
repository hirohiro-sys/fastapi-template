from pydantic_settings import BaseSettings, SettingsConfigDict

# アプリケーション全体の設定を管理するPydanticモデル
class Settings(BaseSettings):
    # データベース接続URLを型定義（必須項目）
    # 値を直接代入せず、.envまたは環境変数からの読み込みを強制
    # これにより、設定漏れがあった場合にPydanticがエラーを発生させ、起動時に検知可能
    DATABASE_URL: str

    # Pydantic Settingsのモデル設定
    model_config = SettingsConfigDict(
        # プロジェクトルートの.envファイルを自動的に読み込む
        env_file=".env"
    )

# Settingsクラスのインスタンスを作成（シングルトンパターン）
# アプリケーション全体でこのインスタンスを通じて設定にアクセス
settings = Settings()