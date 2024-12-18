import os

from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(openapi_prefix="/" + os.getenv("APP_ENV", ""))


@app.get("/")
def root():
    return {"hello": "world"}


handler = Mangum(app)
