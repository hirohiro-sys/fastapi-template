.PHONY: build up down restart logs ps hash db-reset deploy-setup deploy remove

# Dockerイメージのビルド
build:
	docker compose build

# コンテナの起動 (バックグラウンドモード)
up:
	docker compose up -d

# コンテナの停止
down:
	docker compose down

# コンテナの再起動 (停止後、起動)
restart:
	docker compose down && docker compose up -d

# ログのリアルタイム表示
logs:
	docker compose logs -f

# コンテナの稼働状況確認
ps:
	docker compose ps

# パスワードハッシュ生成ユーティリティ
# 使い方: make hash pw=your_password （your_passwordを実際のパスワードに置き換える）
hash:
	@docker compose exec api python3 -c"from passlib.context import CryptContext; ctx = CryptContext(schemes=['bcrypt'], deprecated='auto'); print(ctx.hash('$(pw)'))"

# 【超便利】DBを完全に初期化（ボリューム削除を伴う再起動）
# 開発データベースをクリーンな状態に戻したい場合に利用
db-reset:
	docker compose down -v # コンテナと関連ボリュームを削除
  docker compose up -d   # コンテナを再起動（init.sqlが再実行される）

# Serverless Frameworkのデプロイ用プラグインインストール
# 初回のみ実行、またはプラグイン変更時に実行
deploy-setup:
	docker compose exec -u root api npm install -D serverless-python-requirements

# アプリケーションのAWS Lambdaへのデプロイ
deploy:
	docker compose exec api npx serverless deploy

# デプロイしたAWSリソースの削除 (後片付け)
remove:
	docker compose exec api npx serverless remove
