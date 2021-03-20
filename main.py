from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")  # path operation decorator (path: / . operation: get)
async def read_item(item_id: int):  # path operation function
    # 型ヒントと合わないパラメタの場合は422  Unprocessable Entity
    return {"item_id": item_id}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/me")  # 上に定義されていない場合、全てread_userで実行されてしまう
async def read_user_me():
    return {"user_id": "the current user"}
