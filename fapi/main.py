from fastapi import FastAPI

from fapi.hello import Hello

app = FastAPI()


@app.get("/")
async def root() -> Hello:
    return Hello()
