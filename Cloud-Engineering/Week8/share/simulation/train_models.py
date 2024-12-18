# train_models.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from surprise import Dataset, Reader, SVD
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import mlflow
import mlflow.sklearn

# Create synthetic user-item interaction data
np.random.seed(42)
n_users = 1000
n_items = 100
data = {
    'user_id': np.random.randint(1, n_users + 1, size=10000),
    'item_id': np.random.randint(1, n_items + 1, size=10000),
    'rating': np.random.randint(1, 6, size=10000)  # Ratings from 1 to 5
}
df = pd.DataFrame(data)

# Prepare data for collaborative filtering (using Surprise library)
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['user_id', 'item_id', 'rating']], reader)
trainset = data.build_full_trainset()

# Train collaborative filtering model (SVD)
model_cf = SVD()
model_cf.fit(trainset)

# For content-based filtering, let's assume we have item descriptions
item_descriptions = ['Description of item {}'.format(i) for i in range(1, n_items + 1)]
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(item_descriptions)
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

# Save cosine similarities in a DataFrame for easier lookup
cosine_sim_df = pd.DataFrame(cosine_similarities, index=np.arange(1, n_items + 1), columns=np.arange(1, n_items + 1))

# Log and save models to MLflow
mlflow.set_experiment("Recommendation_Engine_Comparison")

# Log and register Collaborative Filtering model
with mlflow.start_run(run_name="Collaborative_Filtering_Model") as run:
    mlflow.log_param("model_type", "collaborative_filtering")
    mlflow.sklearn.log_model(model_cf, "model_cf")
    mlflow.register_model(f"runs:/{run.info.run_id}/model_cf", "CollaborativeFilteringModel")

# Save cosine similarities for Content-Based model
cosine_sim_file = "cosine_similarities.pkl"
with open(cosine_sim_file, "wb") as f:
    pickle.dump(cosine_sim_df, f)

# Log and register Content-Based model
with mlflow.start_run(run_name="Content_Based_Model") as run:
    mlflow.log_param("model_type", "content_based")
    mlflow.log_artifact(cosine_sim_file, "cosine_similarities")
    mlflow.register_model(f"runs:/{run.info.run_id}/cosine_similarities", "ContentBasedModel")
