from fastapi import FastAPI

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

# ルートパス("/")に対するGETリクエストのハンドラーを定義
@app.get("/")
def read_root():
    # JSON形式でメッセージを返す
    return {"message": "Hello FastAPI 2026!"}