# simulate_user_clicks.py
import numpy as np
import mlflow
import mlflow.sklearn
import pickle
import random
import os

# Define the number of items (should match the number used in training)
n_items = 100

# Load Collaborative Filtering model
cf_model = mlflow.sklearn.load_model("models:/CollaborativeFilteringModel/1")

# Load Content-Based model similarities
cb_model_uri = "models:/ContentBasedModel/1"
cb_similarities_path = mlflow.artifacts.download_artifacts(cb_model_uri)

# Print the downloaded path for debugging
print(f"Downloaded content-based model artifacts to: {cb_similarities_path}")

# Ensure the artifact exists
artifact_file_path = os.path.join(cb_similarities_path, "cosine_similarities.pkl")
if not os.path.exists(artifact_file_path):
    raise FileNotFoundError(f"Artifact file not found: {artifact_file_path}")

# Load the artifact
with open(artifact_file_path, "rb") as f:
    cosine_sim_df = pickle.load(f)

# Function to simulate user clicks for CF model
def simulate_cf_clicks(model, user_id, top_n=10):
    # For simplicity, we generate random recommendations
    recommended_items = random.sample(range(1, n_items + 1), top_n)
    # Simulate clicks (1 if clicked, 0 if not)
    clicks = [random.choices([0, 1], weights=[0.9, 0.1])[0] for _ in recommended_items]
    return recommended_items, clicks

# Function to simulate user clicks for CB model
def simulate_cb_clicks(similarities, user_id, top_n=10):
    # For simplicity, we generate random recommendations based on similarities
    random_item = random.choice(range(1, n_items + 1))
    similar_items = cosine_sim_df.loc[random_item].nlargest(top_n + 1).index.tolist()[1:]
    # Simulate clicks (1 if clicked, 0 if not)
    clicks = [random.choices([0, 1], weights=[0.9, 0.1])[0] for _ in similar_items]
    return similar_items, clicks

# Simulate clicks and log results
mlflow.set_experiment("Recommendation_Engine_Comparison")

total_clicks_cf = 0
total_clicks_cb = 0

for user_id in range(1, 101):  # Simulate for 100 users
    with mlflow.start_run(run_name=f"Simulate_Clicks_CF_User_{user_id}"):
        recommended_items, clicks = simulate_cf_clicks(cf_model, user_id)
        user_clicks = sum(clicks)
        total_clicks_cf += user_clicks
        mlflow.log_param("user_id", user_id)
        mlflow.log_param("model", "Collaborative_Filtering_Model")
        mlflow.log_metric("user_clicks", user_clicks)
    
    with mlflow.start_run(run_name=f"Simulate_Clicks_CB_User_{user_id}"):
        recommended_items, clicks = simulate_cb_clicks(cosine_sim_df, user_id)
        user_clicks = sum(clicks)
        total_clicks_cb += user_clicks
        mlflow.log_param("user_id", user_id)
        mlflow.log_param("model", "Content_Based_Model")
        mlflow.log_metric("user_clicks", user_clicks)

# Log total clicks for both models
with mlflow.start_run(run_name="Simulate_Clicks_Summary"):
    mlflow.log_param("total_users", 100)
    mlflow.log_metric("total_clicks_cf", total_clicks_cf)
    mlflow.log_metric("total_clicks_cb", total_clicks_cb)

print(f"Total clicks for Collaborative Filtering Model: {total_clicks_cf}")
print(f"Total clicks for Content-Based Model: {total_clicks_cb}")
