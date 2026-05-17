# Pythonの公式スリムイメージをベースとする（より軽量で安全）
FROM python:3.12-slim

# コンテナ内の作業ディレクトリを/srcに設定
WORKDIR /src

# 1. 先に「ライブラリのリスト」だけをコンテナにコピー
# この層はrequirements.txtが変更されない限りキャッシュされるため、ビルドが高速化される
COPY requirements.txt .

# 2. まとめて依存ライブラリをインストール
# --no-cache-dir オプションでキャッシュを生成せず、イメージサイズを削減
RUN pip install --no-cache-dir -r requirements.txt

# 3. 最後に「ソースコード全体」をコピー
# アプリケーションコードは頻繁に変わるため、この層を後回しにすることでキャッシュを最大限活用
COPY . .

# コンテナが起動したときに実行されるコマンドを定義
# uvicornでFastAPIアプリケーションを起動し、ホストの全インターフェースからアクセス可能に
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]