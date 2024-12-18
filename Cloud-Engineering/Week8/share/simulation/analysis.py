# analysis.py
import mlflow
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Load runs from MLflow
experiment_name = "Recommendation_Engine_Comparison"
experiment = mlflow.get_experiment_by_name(experiment_name)
runs_df = mlflow.search_runs(experiment_ids=[experiment.experiment_id])

# Print available columns for debugging
print(runs_df.columns)

# Debugging: print available metrics
print(runs_df[['run_id', 'metrics.total_clicks_cf', 'metrics.total_clicks_cb']])

# Retrieve total clicks for each model from the summary run
summary_run = runs_df[runs_df['tags.mlflow.runName'] == 'Simulate_Clicks_Summary']
if not summary_run.empty:
    total_clicks_cf = summary_run['metrics.total_clicks_cf'].values[0]
    total_clicks_cb = summary_run['metrics.total_clicks_cb'].values[0]

    print(f"Total clicks for Collaborative Filtering Model: {total_clicks_cf}")
    print(f"Total clicks for Content-Based Model: {total_clicks_cb}")

    # Statistical test to compare the clicks
    z_stat, p_value = proportions_ztest([total_clicks_cf, total_clicks_cb], [100 * 10, 100 * 10])  # Assuming 100 users and 10 recommendations each
    print(f"Z-test statistic: {z_stat}, p-value: {p_value}")

    # Interpretation
    alpha = 0.05
    if p_value < alpha:
        print("There is a significant difference between the two models.")
    else:
        print("There is no significant difference between the two models.")
else:
    print("Summary run not found.")
