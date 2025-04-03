from fastapi import FastAPI

app = FastAPI()

# Base de datos simulada
users_db = {
    1: {"id": 1, "name": "Alice", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob", "email": "bob@example.com"},
}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id in users_db:
        return users_db[user_id]
    return {"error": "User not found"}, 404

# Para ejecutar el servicio:
# uvicorn microservices.user_service.main:app --host 0.0.0.0 --port 8001 --reload
