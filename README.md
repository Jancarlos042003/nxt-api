# 📋 LegalTech API - Backend de Gestión de Casos

API RESTful desarrollada con FastAPI para la gestión de casos/expedientes legales. Este backend proporciona servicios de autenticación y CRUD completo de casos, diseñado para ser consumido por el frontend Next.js.

## 🚀 Tecnologías Clave

- **FastAPI** - Framework web moderno y de alto rendimiento para construir APIs
- **Python 3.8+** - Lenguaje de programación principal
- **JWT (JSON Web Tokens)** - Sistema de autenticación y autorización
- **Passlib + Argon2** - Hash seguro de contraseñas
- **Python-Jose** - Implementación de JWT
- **Pydantic** - Validación de datos y serialización
- **DynamoDB** - Base de datos NoSQL (AWS)
- **Uvicorn** - Servidor ASGI de alto rendimiento

## 📁 Estructura del Proyecto

```
LegaltechApi/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuración y variables de entorno
│   │   └── security.py        # Funciones de seguridad y JWT
│   ├── di/
│   │   ├── case_providers.py  # Inyección de dependencias para casos
│   │   └── user_provider.py   # Inyección de dependencias para usuarios
│   ├── exceptions/
│   │   ├── domain_exceptions.py     # Excepciones de dominio
│   │   ├── technical_exceptions.py  # Excepciones técnicas
│   │   └── handler.py               # Manejadores de excepciones
│   ├── repositories/         # Capa de acceso a datos
│   │   ├── case_repository.py
│   │   └── user_repository.py
│   ├── routers/              # Endpoints de la API
│   │   ├── auth.py           # Rutas de autenticación
│   │   └── cases.py          # Rutas CRUD de casos
│   ├── schemas/              # Esquemas Pydantic
│   │   ├── case.py           # Schemas de casos
│   │   └── user.py           # Schemas de usuarios
│   ├── services/             # Lógica de negocio
│   │   ├── case_service.py
│   │   └── user_service.py
│   └── main.py               # Punto de entrada de la aplicación
└── README.md                # Documentación del proyecto
```

## 🚀 Instrucciones de Ejecución Local

### Prerrequisitos

- Python 3.8 o superior
- **UV** - Instalado globalmente (ver instrucciones de instalación abajo)
- Cuenta de AWS con acceso a DynamoDB (o DynamoDB Local)

### Instalar UV

Si aún no tienes UV instalado, puedes instalarlo con uno de estos métodos:

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Con pip (alternativa):**
```bash
pip install uv
```

Verifica la instalación:
```bash
uv --version
```

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/legaltech-api.git
   cd LegaltechApi
   ```

2. **Sincronizar dependencias con UV**
   
   UV creará automáticamente el entorno virtual y instalará todas las dependencias del proyecto:
   
   ```bash
   uv sync
   ```
   
   Este comando:
   - Crea un entorno virtual en `.venv/` (si no existe)
   - Instala todas las dependencias del `pyproject.toml`
   - Garantiza versiones consistentes mediante el lockfile

3. **Configurar variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto:
   
   ```bash
   # Copiar el ejemplo (si existe)
   cp .env.example .env
   ```
   
   Edita `.env` con tus valores:
   ```env
   SECRET_KEY=tu-clave-secreta-super-segura-de-al-menos-32-caracteres
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=tu-access-key
   AWS_SECRET_ACCESS_KEY=tu-secret-key
   DYNAMODB_TABLE_CASES=legaltech-cases
   DYNAMODB_TABLE_USERS=legaltech-users
   ```

4. **Iniciar el servidor de desarrollo**
   
   Usa UV para ejecutar el servidor con recarga automática:
   
   ```bash
   uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   O de forma más simple:
   ```bash
   uv run fastapi dev app/main.py
   ```

5. **Verificar que el servidor está corriendo**
   
   Abre tu navegador en: `http://localhost:8000`
   
   Deberías ver:
   ```json
   {
     "message": "Bienvenido a la API de Gestión de Casos"
   }
   ```

## 🐳 Docker (Opcional)

Si prefieres usar Docker:

```bash
# Construir la imagen
docker build -t legaltech-api .

# Ejecutar el contenedor
docker run -p 8000:8000 --env-file .env legaltech-api
```

## 🔐 Módulos de la API

### 🔹Autenticación

#### **POST /auth/login**
Autentica al usuario y genera un token JWT.

#### **GET /auth/me**

### 🔹Gestión de Casos (CRUD)

**Todos los endpoints** de casos requieren autenticación mediante JWT.

#### **POST /cases/create**
Crea un nuevo caso en el sistema.

#### **GET /cases/{case_id}**
Obtiene un caso específico por su ID.

#### **PUT /cases/{case_id}**
Actualiza un caso existente.

#### **GET /cases**
Lista todos los casos del sistema.

#### **DELETE /cases/{case_id}**
Elimina un caso del sistema.

## 📝 Notas Adicionales

### CORS

La API está configurada para aceptar peticiones desde:
- `http://localhost:3000` (desarrollo local)
- `https://nxt-legaltech-1.vercel.app` (producción)

Para agregar más orígenes, edita la lista `origins` en `app/main.py`.
