import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("COINCAP_API_KEY")

headers = {
    "Authorization": "Bearer " + api_key,
    "accept": "application/json"
}
history = "history?interval=d1"
bitcoin = "bitcoin"
coincap_url = "https://rest.coincap.io/v3/assets/"
url = coincap_url + bitcoin + "/" + history

print(f"URL utilizada: {url}") # Depuración

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text) # Ver qué dice la API
        data = None

except requests.exceptions.RequestException as e:
    print(f"Error al hacer la solicitud: {e}")
    data = None
except ValueError as e:
    print(f"Error al procesar la respuesta JSON: {e}")
    data = None

if data:
    # Si 'data' es un diccionario con clave 'data' (común en Coincap), extraemos la lista
    lista_datos = data.get('data', data) if isinstance(data, dict) else data
    df = pd.DataFrame(lista_datos)

    # Eliminar las primeras 335 filas si es necesario (según script original)
    if len(df) > 335:
        df.drop(range(0, 335), axis=0, inplace=True)

    # --- LÓGICA DE FECHAS ---
    # --- LÓGICA DE FECHAS ---
    # Generar automáticamente una fecha para cada fila
    # Última fila = Ayer, filas anteriores = días previos
    if not df.empty:
        # Re-indexar el dataframe para evitar huecos en el índice tras el drop
        df.reset_index(drop=True, inplace=True)
        
        # El usuario indica que la última fila corresponde a AYER
        ayer = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)
        fechas = pd.date_range(end=ayer, periods=len(df), freq='D')
        df['fecha'] = fechas

    df.drop(columns=["time", "date"], inplace=True)
    df.to_csv("bitcoin_last_month.csv", index=False)
else:
    print("No hay datos disponibles.")
