from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")  # path operation decorator (path: / . operation: get)
async def read_item(item_id: int):  # path operation function
    # 型ヒントと合わないパラメタの場合は422  Unprocessable Entity
    return {"item_id": item_id}
