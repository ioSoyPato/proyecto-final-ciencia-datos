import mlflow
import pandas as pd
from mlflow.tracking import MlflowClient
from fastapi import FastAPI

app = FastAPI()

# Configura la URI de rastreo de mlflow (cambia esto si necesitas otra dirección)
MLFLOW_TRACKING_URI = "https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Nombre del modelo y alias
model_name = "MyModel"
alias = "champion"

InputData = pd.DataFrame({
    "ts": [1594512094.9],
    "co": [0.001171],
    "humidity": [1.1],
    "lpg": [0.002693],
    "smoke": [0.006692]
})

class InputData:
    ts: float
    co: float
    humidity: float
    lgp: float
    smoke: float

def get_run_id_from_alias(model_name: str, alias: str) -> str:
    client = MlflowClient()
    alias_info = client.get_model_version_by_alias(name=model_name, alias=alias)
    return alias_info.run_id

def predict(data: dict):
    model_name = "patricio-model"
    alias = "champion"

    run_id = get_run_id_from_alias(model_name=model_name, alias=alias)

    model_uri = f"runs:/{run_id}/   "

    loaded_model = mlflow.pyfunc.load_model(model_uri=model_uri)


    df = pd.DataFrame(data)
    pred = loaded_model.predict(df)

    return pred

@app.post("/predict")
def predict_endpoint(input_data: InputData):
    input_dict = input_data.dict()

    result = predict(input_dict)

    return {
        "prediction": result[0]
    }
