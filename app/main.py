from fastapi import FastAPI

from app.exceptions.handler import register_handlers
from app.routers.auth import auth_router
from app.routers.cases import cases_router

app = FastAPI()
register_handlers(app)


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Casos"}


app.include_router(router=cases_router, prefix="/cases")
app.include_router(router=auth_router, prefix="/auth")
