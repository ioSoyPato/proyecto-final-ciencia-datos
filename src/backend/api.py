import pickle
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel
from mlflow import MlflowClient

dagshub_repo = "https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos"
MLFLOW_TRACKING_URI = "https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos.mlflow"


mlflow.set_tracking_uri(uri=MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

run_ = mlflow.search_runs(order_by=['metrics.rmse ASC'],
                          output_format="list",
                          experiment_names=["temp-prediction-experiment"]
                          )[0]


run_id = run_.info.run_id

run_uri = f"runs:/{run_id}/preprocessor"


client.download_artifacts(
    run_id=run_id,
    path='preprocessor',
    dst_path='.'
)

with open("preprocessor/preprocessor.b", "rb") as f_in:
    dv = pickle.load(f_in)


model_name = "MyModel"
alias = "champion"

model_uri = f"models:/{model_name}@{alias}"

champion_model = mlflow.pyfunc.load_model(
    model_uri=model_uri
)

def predict(input_data):

    X_pred = (input_data)

    return champion_model.predict(X_pred)

app = FastAPI()

class InputData(BaseModel):
    PULocationID: str
    DOLocationID: str
    trip_distance: float


@app.post("/predict")
def predict_endpoint(input_data: InputData):
    result = predict(input_data)[0]

    return {
        "prediction": float(result)
    }