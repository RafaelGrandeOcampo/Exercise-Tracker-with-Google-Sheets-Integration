import requests
from datetime import datetime
import os

# Obtener las claves de las variables de entorno
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("OWM_API_KEY")
SHEET_ENDPOINT = os.environ.get("SHEET_ENDPOINT")
TOKEN = os.environ.get("TOKEN")

# Verificar que todas las claves se hayan obtenido correctamente
if not all([APP_ID, APP_KEY, SHEET_ENDPOINT, TOKEN]):
    print("Por favor, asegúrate de configurar todas las variables de entorno correctamente.")
    exit()

GENERO = "MALE"
PESO = 82
ALTURA = 180
EDAD = 30

nutrix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers_nutrix = {
    "x-app-id": APP_ID,
    "x-app-key": APP_KEY,
}

ejercicio = input("¿Qué ejercicio has hecho hoy? ")

parameters = {
    "query": ejercicio,
    "gender": GENERO,
    "weight_kg": PESO,
    "height_cm": ALTURA,
    "age": EDAD
}

# Realizar la solicitud a la API de Nutritionix
response = requests.post(nutrix_endpoint, json=parameters, headers=headers_nutrix)

# Verificar si la solicitud fue exitosa
if response.ok:
    resultado = response.json()
    print(resultado)
else:
    print("Hubo un problema al obtener los datos del ejercicio.")
    exit()

# Obtener la fecha y hora actual
FECHA = datetime.now().strftime("%d/%m/%Y")
HORA = datetime.now().strftime("%H:%M:%S")

# Preparar los datos para la hoja de cálculo
sheet_inputs = {
    "hoja1": []
}

# Procesar los datos de cada ejercicio obtenido
for ejercicio in resultado.get("exercises", []):
    sheet_inputs["hoja1"].append({
        "date": FECHA,
        "time": HORA,
        "exercise": ejercicio["user_input"].title(),
        "duration": ejercicio["duration_min"],
        "calories": ejercicio["nf_calories"]
    })

# Realizar la solicitud para agregar los datos a la hoja de cálculo
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

sheets_response = requests.post(SHEET_ENDPOINT, json=sheet_inputs, headers=headers)

# Verificar si la solicitud fue exitosa
if sheets_response.ok:
    final_sheets = sheets_response.json()
    print(final_sheets)
else:
    print("Hubo un problema al agregar los datos a la hoja de cálculo.")
