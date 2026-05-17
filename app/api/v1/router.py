from fastapi import APIRouter

from app.api.v1 import health

# v1 配下のエンドポイントはここに集約する
api_router = APIRouter()
api_router.include_router(health.router)
