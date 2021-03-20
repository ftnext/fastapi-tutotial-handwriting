from enum import Enum
from typing import Optional

from fastapi import FastAPI


class ModelName(str, Enum):  # APIドキュメント向けにstrの継承が必要
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_item_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:  # 列挙型のメンバとの比較
        # 返り値の中の列挙型は文字列に変換される
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":  # 列挙型の値を取得して比較
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:  # query parameterのshortは1でもTrueでも文字列でもよい
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


@app.get("/items/")
async def read_item1(skip: int = 0, limit: int = 10):
    return fake_item_db[skip: skip + limit]


@app.get("/items/{item_id}")  # path operation decorator (path: / . operation: get)
async def read_item0(item_id: int):  # path operation function
    # 型ヒントと合わないパラメタの場合は422  Unprocessable Entity
    return {"item_id": item_id}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/me")  # 上に定義されていない場合、全てread_userで実行されてしまう
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    # /files//home/johndoe/myfile.txt -> /home/johndoe/myfile.txt
    return {"file_path": file_path}
