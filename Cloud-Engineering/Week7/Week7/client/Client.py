import mlflow
from mlflow.tracking.client import MlflowClient

mr_uri = mlflow.get_registry_uri()
print("Current registry uri: {}".format(mr_uri))

tracking_uri = mlflow.get_tracking_uri()
print("Current tracking uri: {}".format(tracking_uri))

# Get search results filtered by the registered model name that matches
# prefix pattern
filter_string = "name LIKE 'Iris%'"
results = mlflow.search_registered_models(filter_string=filter_string)
print("-" * 80)
for res in results:
    for mv in res.latest_versions:
        print("name={}; run_id={}; version={}".format(mv.name, mv.run_id, mv.version))

# client.update_registered_model(
#   name=model_name,
#   description="This model forecasts the power output of a wind farm based on weather data. The weather data consists of three features: wind speed, wind direction, and air temperature."
# )