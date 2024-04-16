from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import time
import pandas as pd
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)
   
class Resena(BaseModel):
    res: str

@app.post("/a")
async def read_root(resena: Resena):
    #Resena a predecir
    res = resena.res 
    #Falta hacer la prediccion
    time.sleep(2)
    #Enviar prediccion
    return {"pred": random.randint(1, 5)}

@app.post("/b")
async def csvPred(file: UploadFile = File(...)):
    csv_content = await file.read()
    df = pd.read_csv(io.BytesIO(csv_content))
    print(df.head(5))
    print(df.shape)
    processed_csv = df.to_csv(index=False)
    
    return StreamingResponse(io.BytesIO(processed_csv.encode()), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=processed_file.csv"})