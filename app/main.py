from fastapi import FastAPI

from app.routers import category, products, auth, permission, review

app = FastAPI()
app_v1 = FastAPI(title='API v1')


@app.get("/")
async def root():
    return {"message": "Hello World"}

app_v1.include_router(category.router)
app_v1.include_router(products.router)
app_v1.include_router(auth.router)
app_v1.include_router(permission.router)
app_v1.include_router(review.router)
app.mount(path='/v1', app=app_v1)