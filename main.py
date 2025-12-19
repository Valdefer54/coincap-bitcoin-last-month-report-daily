import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("COINCAP_API_KEY") #get your API KEY at coincap page

headers = {
    "Authorization": "Bearer " + api_key,
    "accept": "application/json"
}
history = "history?interval=d1"
bitcoin = "bitcoin"
coincap_url = "https://rest.coincap.io/v3/assets/"
url = coincap_url + bitcoin + "/" + history

print(f"URL: {url}") 

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text) # API response
        data = None

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
    data = None
except ValueError as e:
    print(f"JSON response error: {e}")
    data = None

if data:
    lista_datos = data.get('data', data) if isinstance(data, dict) else data
    df = pd.DataFrame(lista_datos)

    #we set only last 30 days.
    if len(df) > 335:
        df.drop(range(0, 335), axis=0, inplace=True)


    # dates generator, last row means yesterday
    if not df.empty:
        # Re-indexar el dataframe para evitar huecos en el índice tras el drop
        df.reset_index(drop=True, inplace=True)
        
        # last row means last day 
        ayer = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)
        fechas = pd.date_range(end=ayer, periods=len(df), freq='D')
        df['Date'] = fechas

    df.drop(columns=["time", "date"], inplace=True)
    df.to_csv("bitcoin_last_month.csv", index=False)
else:
    print("No data available.")
