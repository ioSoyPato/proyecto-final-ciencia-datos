import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Configura la URI de rastreo de mlflow
MLFLOW_TRACKING_URI = "https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Nombre del modelo y alias
model_name = "MyModel"
alias = "champion"

# Define la clase InputData con todos los campos necesarios
class InputData(BaseModel):
    ts: float
    co: float
    humidity: float
    lpg: float
    smoke: float
    light: bool  
    motion: bool  

# Función para obtener el run_id a partir del alias
def get_run_id_from_alias(model_name: str, alias: str) -> str:
    client = MlflowClient()
    alias_info = client.get_model_version_by_alias(name=model_name, alias=alias)
    return alias_info.run_id

# Función de predicción
def predict(data: dict):
    # Obtén el run_id del modelo
    run_id = get_run_id_from_alias(model_name=model_name, alias=alias)

    # Carga el modelo desde MLflow
    model_uri = f"runs:/{run_id}/model"
    loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)

    # Convierte los datos a un DataFrame y realiza la predicción
    df = pd.DataFrame([data])
    pred = loaded_model.predict(df)

    return pred

# Endpoint de predicción
@app.post("/predict")
def predict_endpoint(input_data: InputData):
    # Convierte los datos de entrada a un diccionario
    input_dict = input_data.dict()

    # Llama a la función de predicción
    result = predict(input_dict)

    # Devuelve el resultado
    return {
        "prediction": result[0]
    }
