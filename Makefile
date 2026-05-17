.PHONY: help up down build logs ps restart shell exec test clean

help:
	@echo "Available commands:"
	@echo "  make up        - コンテナをバックグラウンドで起動"
	@echo "  make down      - コンテナを停止して削除"
	@echo "  make build     - イメージを再ビルド"
	@echo "  make logs      - api コンテナのログを追従表示"
	@echo "  make ps        - 起動中のコンテナを表示"
	@echo "  make restart   - api コンテナを再起動"
	@echo "  make shell     - api コンテナに bash で入る"
	@echo "  make exec CMD=\"...\" - api コンテナで任意コマンドを実行"
	@echo "  make clean     - __pycache__ などのキャッシュを削除"

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build --no-cache

logs:
	docker compose logs -f api

ps:
	docker compose ps

restart:
	docker compose restart api

shell:
	docker compose exec api bash

exec:
	docker compose exec api $(CMD)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
