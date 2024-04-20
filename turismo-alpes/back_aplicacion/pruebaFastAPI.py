import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from transforms import svc_pipeline

app = FastAPI()
pipeline = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Resena(BaseModel):
    res: str


class ModelBuilder(BaseModel):
    pipeline_dump_name: str
    vectorizer_dump_name: str
    data_name: str


@app.on_event("startup")
async def startup_event():
    global pipeline
    # Your startup logic here
    print("Aplicacion inicializada")
    # Carga el pipeline
    pipeline = svc_pipeline.load_pipeline(
        'models/pipe_alpha_1.joblib',
        'models/vecto_alpha_1.joblib'
    )
    if pipeline is not None:
        print("Pipeline cargado correctamente")
    else:
        print("Error de carga del pipeline")


@app.post("/model-builder")
async def build_model(modelBuilder: ModelBuilder):
    global pipeline
    # Consigue los paths relativos al proyecto
    pipeline_dump_path = "models/" + modelBuilder.pipeline_dump_name + ".joblib"
    vectorizer_dump_path = "models/" + modelBuilder.vectorizer_dump_name + ".joblib"
    data_path = "../data/raw/" + modelBuilder.data_name + ".csv"

    print("Construyendo pipeline...")
    print("CWD: ", os.getcwd())
    print("PIPELINE: ", os.getcwd() + "/" + pipeline_dump_path)
    print("VECTORIZER: ", os.getcwd() + "/" + vectorizer_dump_path)
    print("DATA: ", os.getcwd() + "/" + data_path)

    # Construye el pipeline
    pipeline = svc_pipeline.build_pipeline(pipeline_dump_path, vectorizer_dump_path, data_path)


@app.get("/health-check")
async def health_check():
    global pipeline
    return {"msg": 200, "pipeline_loaded": (bool)(pipeline is not None)}


@app.get("/predict-test")
async def predict_test():
    global pipeline
    if pipeline is None:
        print("No pipeline loaded")
        return {"error": "No pipeline loaded"}
    else:
        p = pipeline.predict(pd.DataFrame({'Review': ['asqueroso']}))
        # se debe convertir al tipo correcto
        return {"pred": int(p[0]), "score": 50}


@app.post("/a")
async def read_root(resena: Resena):
    global pipeline
    if pipeline is None:
        print("No pipeline loaded")
        return {"error": "No pipeline loaded"}
    else:
        p = pipeline.predict(pd.DataFrame({'Review': [resena.res]}))
        # se debe convertir al tipo correcto
        return {"pred": int(p[0]), "score": -1}


@app.post("/b")
async def csvPred(file: UploadFile = File(...)):
    global pipeline

    if pipeline is None:
        print("No pipeline loaded")
        # TODO: devolver mensaje de error
        return {}

    csv_content = await file.read()
    df = pd.read_csv(io.BytesIO(csv_content))
    df1 = df.copy()
    print(df.head(5))
    print(df.shape)

    preds = pipeline.predict(df)
    df1['Clasificacion'] = preds


    processed_csv = df1.to_csv(index=False)

    return StreamingResponse(io.BytesIO(processed_csv.encode()), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=processed_file.csv"})
