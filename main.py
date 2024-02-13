from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products/{product_id}")
async def print_product_info(id: str):
    return {"message": f"Product id: {id}"}
