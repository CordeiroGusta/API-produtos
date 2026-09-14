from fastapi import FastAPI, status
from app.schemas.items_schemas import MessageResponse
from app.routers import items_routes

app = FastAPI(
    title="Items CRUD API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(items_routes.router)

@app.get(
    '/api/v1',
    status_code=status.HTTP_200_OK,
    response_model=MessageResponse
)
def status_check():
    return {'message': 'Olá, se você esta lendo isso, a API esta funcionando!'}