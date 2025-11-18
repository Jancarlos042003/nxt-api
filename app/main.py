from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.handler import register_handlers
from app.routers.auth import auth_router
from app.routers.cases import cases_router

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",
    "https://nxt-legaltech.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

# Registro de manejadores de excepciones personalizados
register_handlers(app)


@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Gestión de Casos"}


app.include_router(router=cases_router, prefix="/cases")
app.include_router(router=auth_router, prefix="/auth")
