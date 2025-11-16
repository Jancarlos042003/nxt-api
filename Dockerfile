FROM python:3.12-slim

# 2. Instala uv (la parte clave)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Prepara el directorio de la app
COPY . /app
WORKDIR /app

# 4. Instala las dependencias con uv
RUN uv sync --frozen --no-cache

# 5. Define el comando para correr la app
CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]