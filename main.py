from fastapi import FastAPI

import models
from database import engine
from routes.products import router as products_router

app = FastAPI()
app.include_router(products_router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products/{id}")
async def print_product_info(id: str):
    return {"message": f"Product id: {id}"}
