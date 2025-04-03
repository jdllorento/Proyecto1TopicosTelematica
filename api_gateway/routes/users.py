from fastapi import APIRouter, HTTPException
import requests
from ..config import USER_SERVICE_URL  # Importamos la URL desde config.py

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
def get_user(user_id: int):
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{user_id}")
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=503, detail="User service unavailable")
