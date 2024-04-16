from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import random
import time

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
    time.sleep(20)

    #Enviar prediccion
    return {"pred": random.randint(1, 5)}
