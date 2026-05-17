# Pythonの公式スリムイメージをベースとする（より軽量で安全）
FROM python:3.12-slim

# コンテナ内の作業ディレクトリを/srcに設定
WORKDIR /src

# 必要なPythonライブラリをインストール
# --no-cache-dir オプションでキャッシュを生成せず、イメージサイズを削減
RUN pip install --no-cache-dir fastapi uvicorn

# ローカルのソースコードをコンテナ内の/srcにコピー
COPY . .

# コンテナが起動したときに実行されるコマンドを定義
# uvicornでFastAPIアプリケーションを起動し、0.0.0.0でコンテナ外部からのアクセスを許可
# --reload オプションでコード変更時に自動的にリロード
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]