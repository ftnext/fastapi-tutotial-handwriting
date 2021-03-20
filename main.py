from fastapi import FastAPI

app = FastAPI()


@app.get("/")  # path operation decorator (path: / . operation: get)
async def root():  # path operation function
    return {"massage": "Hello World"}
