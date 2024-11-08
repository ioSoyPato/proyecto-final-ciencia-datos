import mlflow
import pandas as pd

# Configura la URI de rastreo de mlflow (cambia esto si necesitas otra dirección)
MLFLOW_TRACKING_URI = "https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos.mlflow"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Nombre del modelo y alias
model_name = "MyModel"
alias = "champion"

# URI del modelo
model_uri = f"models:/{model_name}@{alias}"

# Carga el modelo
champion_model = mlflow.pyfunc.load_model(model_uri=model_uri)

input_data = pd.DataFrame({
    "ts": [1594512094.9],
    "co": [0.001171],
    "humidity": [1.1],
    "lpg": [0.002693],
    "smoke": [0.006692]
})


# Realiza la predicción
prediction = champion_model.predict(input_data)

# Imprime la predicción
print("Predicción:", prediction)
