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
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    txtfile = z.open(z.namelist()[0])
    
    df = pd.read_csv(txtfile, sep=",", engine='python')
    return df

@app.get("/api/cot/{symbol}")
async def get_symbol_data(symbol: str):
    df = get_cot_data()
    
    if symbol.upper() not in MARKETS:
        return {"error": "Símbolo no soportado"}
    
    code = MARKETS[symbol.upper()]
    filtered = df[df['CFTC Contract Market Code'].astype(str) == code]
    
    if filtered.empty:
        return {"error": "No se encontraron datos para este activo"}
    
    result = filtered[[
        'Report_Date_as_YYYY-MM-DD',
        'Prod_Desc',
        'Noncommercial_Long_All',
        'Noncommercial_Short_All',
        'Noncommercial_Spreading_All'
    ]].sort_values('Report_Date_as_YYYY-MM-DD', ascending=False).to_dict(orient="records")
    
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

