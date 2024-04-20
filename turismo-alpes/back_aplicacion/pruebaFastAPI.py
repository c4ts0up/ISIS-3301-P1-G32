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
    percent_train: float


class ModelLoader(BaseModel):
    pipeline_dump_name: str
    vectorizer_dump_name: str


@app.on_event("startup")
async def startup_event():
    await load_model(
        ModelLoader(
            pipeline_dump_name="pipe_3p_beta",
            vectorizer_dump_name="vecto_3p_beta"
        )
    )


@app.post("/load-model")
async def load_model(modelLoader: ModelLoader):
    global pipeline
    pipeline_path = 'models/' + modelLoader.pipeline_dump_name + '.joblib'
    vectorizer_path = 'models/' + modelLoader.vectorizer_dump_name + '.joblib'

    pipeline = svc_pipeline.load_pipeline(pipeline_path, vectorizer_path)

    if pipeline is not None:
        print(modelLoader.pipeline_dump_name, "cargado correctamente")
    else:
        print("ERROR: no se pudo cargar", modelLoader.pipeline_dump_name)


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
    pipeline = svc_pipeline.build_pipeline(
        pipeline_dump_path,
        vectorizer_dump_path,
        data_path,
        percent_train=modelBuilder.percent_train
    )


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
        df_entrada = pd.DataFrame({'Review': ['asqueroso']})
        print(df_entrada)
        df_respuesta = svc_pipeline.get_prediction(pipeline, df_entrada)

        # se debe convertir al tipo correcto
        return {
            "pred": int(df_respuesta.iloc[0]['Class']),
            "score": float(df_respuesta.iloc[0]['Score'])
        }


@app.post("/a")
async def read_root(resena: Resena):
    print("Haciendo predicción")
    global pipeline
    if pipeline is None:
        print("No pipeline loaded")
        return {"error": "No pipeline loaded"}
    else:
        df_entrada = pd.DataFrame({'Review': [resena.res]})
        print(df_entrada)
        df_respuesta = svc_pipeline.get_prediction(pipeline, df_entrada)

        # se debe convertir al tipo correcto
        return {
            "pred": int(df_respuesta.iloc[0]['Class']),
            "score": float(df_respuesta.iloc[0]['Score'])
        }


@app.post("/b")
async def csvPred(file: UploadFile = File(...)):
    global pipeline

    if pipeline is None:
        print("No pipeline loaded")
        # TODO: devolver mensaje de error
        return {"error": "No pipeline loaded"}

    csv_content = await file.read()
    df = pd.read_csv(io.BytesIO(csv_content))

    df_respuesta = svc_pipeline.get_prediction(pipeline, df)

    print(df.head(5))
    print(df.shape)

    processed_csv = df_respuesta.to_csv(index=False)

    return StreamingResponse(io.BytesIO(processed_csv.encode()), media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=processed_file.csv"})
