from fastapi import FastAPI

import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products/{product_id}")
async def print_product_info(id: str):
    return {"message": f"Product id: {id}"}
