
import requests

def dragon_ball_api():
    url = "https://dragonball-api.com/api/characters?page=1&limit=100"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        print("Solicitud exitosa!")
        return data

    except requests.exceptions.HTTPError as errh:
        print(f"Error HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error de conexión: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Error en la solicitud: {err}")