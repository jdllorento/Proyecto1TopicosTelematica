import requests

API_GATEWAY_URL = "http://localhost:8000"


def get_user(user_id):
    """Consulta un usuario a través del API Gateway"""
    url = f"{API_GATEWAY_URL}/users/{user_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es 200
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Solicita un ID al usuario
    user_id = int(input("Ingrese el ID del usuario: "))
    user_data = get_user(user_id)
    print("\n🔹 Respuesta del API Gateway:")
    print(user_data)
