from fastapi import FastAPI
from .routes import users

app = FastAPI(title="API Gateway")

# Incluir rutas desde los módulos de users y orders
app.include_router(users.router)
# app.include_router(orders.router)


@app.get("/")
def read_root():
    return {"message": "API Gateway is running"}

# Para ejecutar el API Gateway:
# uvicorn api_gateway.main:app --host 0.0.0.0 --port 8000 --reload
