from fastapi import FastAPI
from app.routers import items_routes

app = FastAPI(
    title="Items CRUD API"
)

app.include_router(items_routes.router)
