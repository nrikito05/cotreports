import uvicorn
from fastapi import FastAPI
import requests
import zipfile
import io
import pandas as pd

app = FastAPI()

MARKETS = {
    "GOLD": "088691",
    "BTC": "133741",
    "EURUSD": "099741",
    "GBPUSD": "096742",
    "JPYUSD": "097741",
    "CADUSD": "090741",
    "CHFUSD": "092741",
    "AUDUSD": "232741",
    "NZDUSD": "112741",
    "MXNUSD": "095741",
    "ZARUSD": "092744"
}

def get_cot_data():
    url = "https://www.cftc.gov/files/dea/history/fut_disagg_txt_2024.zip"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()  # Lanza excepción si hubo error HTTP
        
        z = zipfile.ZipFile(io.BytesIO(r.content))
        txtfile = z.open(z.namelist()[0])
        
        df = pd.read_csv(txtfile, sep=",", engine='python', on_bad_lines='skip')
        return df
    except Exception as e:
        print(f"Error al descargar o procesar COT: {e}")
        raise
