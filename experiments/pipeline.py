import pickle
import mlflow
import pathlib
import dagshub
import pandas as pd
import xgboost as xgb
from hyperopt.pyll import scope
from sklearn.metrics import root_mean_squared_error
from sklearn.feature_extraction import DictVectorizer
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from prefect import flow, task
from mlflow.entities import ViewType
from sklearn.model_selection import train_test_split



@task(name="Read Data")
def read_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    X = df.drop(columns=["temp","device"])
    y = df["temp"]
    return train_test_split(X, y, test_size=0.33, random_state=42)



@task(name="Hyper-Parameter Tunning")
def hyper_parameter_tunning(X_train, X_val, y_train, y_val, dv):
    
    mlflow.xgboost.autolog()

    train = xgb.DMatrix(X_train, label=y_train)
    
    valid = xgb.DMatrix(X_val, label=y_val)
    
    def objective(params):
        with mlflow.start_run(nested=True):
             
            # Tag model
            mlflow.set_tag("model_family", "xgboost")
            
            # Train model
            booster = xgb.train(
                params=params,
                dtrain=train,
                num_boost_round=100,
                evals=[(valid, 'validation')],
                early_stopping_rounds=10
            )
            
            # Predict in the val dataset
            y_pred = booster.predict(valid)
            
            # Calculate metric
            rmse = root_mean_squared_error(y_val, y_pred)
            
            # Log performance metric
            mlflow.log_metric("rmse", rmse)
    
        return {'loss': rmse, 'status': STATUS_OK}

    with mlflow.start_run(run_name="Xgboost Hyper-parameter Optimization", nested=True):
        search_space = {
            'max_depth': scope.int(hp.quniform('max_depth', 4, 100, 1)),
            'learning_rate': hp.loguniform('learning_rate', -3, 0),
            'reg_alpha': hp.loguniform('reg_alpha', -5, -1),
            'reg_lambda': hp.loguniform('reg_lambda', -6, -1),
            'min_child_weight': hp.loguniform('min_child_weight', -1, 3),
            'objective': 'reg:squarederror',
            'seed': 42
        }
        
        best_params = fmin(
            fn=objective,
            space=search_space,
            algo=tpe.suggest,
            max_evals=10,
            trials=Trials()
        )
        best_params["max_depth"] = int(best_params["max_depth"])
        best_params["seed"] = 42
        best_params["objective"] = "reg:squarederror"
        
        mlflow.log_params(best_params)

    return best_params

@task(name="Train Best Model")
def train_best_model(X_train, X_val, y_train, y_val, dv, best_params) -> None:
    """train a model with best hyperparams and write everything out"""

    with mlflow.start_run(run_name="Best model ever"):
        train = xgb.DMatrix(X_train, label=y_train)
        valid = xgb.DMatrix(X_val, label=y_val)

        mlflow.log_params(best_params)

        # Log a fit model instance
        booster = xgb.train(
            params=best_params,
            dtrain=train,
            num_boost_round=100,
            evals=[(valid, 'validation')],
            early_stopping_rounds=10
        )

        y_pred = booster.predict(valid)
        rmse = root_mean_squared_error(y_val, y_pred)
        mlflow.log_metric("rmse", rmse)

        pathlib.Path("models").mkdir(exist_ok=True)
        with open("models/preprocessor.b", "wb") as f_out:
            pickle.dump(dv, f_out)
        
        mlflow.log_artifact("models/preprocessor.b", artifact_path="preprocessor")
    
    return None


@task(name="select challenger", retries=4, retry_delay_seconds=30)
def select_best_model(experiment_name):
    try:
        experiment = mlflow.get_experiment_by_name(experiment_name)
        if experiment is None:
            raise ValueError(f"Experimento con nombre '{experiment_name}' no encontrado.")
        
        experiment_id = experiment.experiment_id
        runs = mlflow.search_runs(experiment_ids=[experiment_id], run_view_type=ViewType.ACTIVE_ONLY)

        best_run = runs.sort_values(by='metrics.rmse').iloc[0]
        best_run_id = best_run['run_id']
        best_model_uri = f"runs:/{best_run_id}/model"
        
        # Registrar el modelo
        model_version = mlflow.register_model(best_model_uri, "MyModel")

        # Esperar a que el modelo se registre 
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name="MyModel",
            version=model_version.version,
            stage="Staging"
        )

        # Asignar alias "challenger" al modelo registrado
        client.update_model_version(
            name="MyModel",
            version=model_version.version,
            description="Este modelo busca desafiar al Champion"
        )
        client.set_registered_model_alias(
            name="MyModel",
            alias="challenger",
            version=model_version.version
        )

        print(f"El mejor modelo fue: {best_run_id} con el RMSE: {best_run['metrics.rmse']}")
    except Exception as e:
        print(f"Error al seleccionar el mejor modelo: {str(e)}")


@task(name="update_champion_model", retries=4, retry_delay_seconds=30)
def update_champion_model(model_name="MyModel"):
    try:
        client = mlflow.tracking.MlflowClient()
        
        # Obtener la versión del modelo "Champion"
        champion_version = None
        for mv in client.search_model_versions(f"name='{model_name}'"):
            if "champion" in mv.aliases:
                champion_version = mv
                break

        if not champion_version:
            raise ValueError("No se encontró la versión del modelo con el alias 'Champion'.")
        
        # Obtener la versión del modelo "Challenger"
        challenger_version = None
        for mv in client.search_model_versions(f"name='{model_name}'"):
            if "challenger" in mv.aliases:
                challenger_version = mv
                break

        if not challenger_version:
            raise ValueError("No se encontró la versión del modelo con el alias 'Challenger'.")

        # Obtener los RMSE del "Champion" y "Challenger"
        champion_run_id = champion_version.run_id
        challenger_run_id = challenger_version.run_id

        champion_run = client.get_run(champion_run_id)
        challenger_run = client.get_run(challenger_run_id)

        champion_rmse = champion_run.data.metrics.get('rmse')
        challenger_rmse = challenger_run.data.metrics.get('rmse')

        if champion_rmse is None or challenger_rmse is None:
            raise ValueError("No se encontró el valor de RMSE para uno de los modelos.")

        # Comparar RMSE y actualizar el "Champion" si el "Challenger" es mejor
        if challenger_rmse < champion_rmse:
            client.delete_registered_model_alias(name=model_name, alias="champion")
            client.set_registered_model_alias(name=model_name, alias="champion", version=challenger_version.version)
            print(f"El modelo 'Challenger' se ha convertido en el nuevo 'Champion' con RMSE: {challenger_rmse}")
        else:
            print(f"El modelo 'Champion' sigue siendo el mejor con RMSE: {champion_rmse}")

    except Exception as e:
        print(f"Error al actualizar el modelo Champion: {str(e)}")


@flow(name="Main Flow")
def main_flow() -> None:
    """The main training pipeline"""

    # MLflow settings
    dagshub.init(url="https://dagshub.com/ioSoyPato/proyecto-final-ciencia-datos", mlflow=True)
    
    MLFLOW_TRACKING_URI = mlflow.get_tracking_uri()
    
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(experiment_name="nyc-taxi-experiment-prefect")

    # Transform
    X_train, X_val, y_train, y_val, dv = read_data("../data/raw/data.csv")
    
    # Hyper-parameter Tunning
    best_params = hyper_parameter_tunning(X_train, X_val, y_train, y_val, dv)
    
    # Train
    train_best_model(X_train, X_val, y_train, y_val, dv, best_params)

    # Select best model as a challenger
    select_best_model("nyc-taxi-experiment-prefect")

    # Update challenger
    update_champion_model()

main_flow()