from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):  # APIドキュメント向けにstrの継承が必要
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:  # 列挙型のメンバとの比較
        # 返り値の中の列挙型は文字列に変換される
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":  # 列挙型の値を取得して比較
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


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


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    # /files//home/johndoe/myfile.txt -> /home/johndoe/myfile.txt
    return {"file_path": file_path}
