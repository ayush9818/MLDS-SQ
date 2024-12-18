# Recommendation Engine A/B Testing with MLflow

This project demonstrates how to perform A/B testing between two machine learning models: a Collaborative Filtering recommendation engine and a Content-Based recommendation engine. The project uses MLflow for tracking experiments, logging models, and analyzing results.

## Project Structure

1. **train_models.py**: Prepares data, trains both Collaborative Filtering and Content-Based models, logs them to MLflow, and registers them.
2. **simulate_user_clicks.py**: Simulates user interactions with the deployed models, logs results to MLflow.
3. **analysis.py**: Analyzes the logged results from MLflow to compare the performance of the two models.

## Getting Started

### Prerequisites

- Python 3.6+
- Required Python packages (listed in `requirements.txt`)

### Start MLFLow Tracking Server
mlflow server --host 127.0.0.1 --port 8080

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Usage

1. **Train Models and Register Them in MLflow:**
    ```bash
    python train_models.py
    ```

2. **Simulate User Clicks and Log Results:**
    ```bash
    python simulate_user_clicks.py
    ```

3. **Analyze Results:**
    ```bash
    python analysis.py
    ```

## Project Details

### 1. Data Preparation and Model Training (`train_models.py`)

This script:
- Creates synthetic user-item interaction data.
- Trains a Collaborative Filtering model using the Surprise library.
- Constructs a Content-Based recommendation model using TF-IDF and cosine similarity.
- Logs and registers both models to MLflow.

### 2. Simulate User Clicks (`simulate_user_clicks.py`)

This script:
- Loads the registered models from MLflow.
- Simulates user interactions with each model.
- Logs individual user interactions and summary metrics to MLflow.

### 3. Analysis (`analysis.py`)

This script:
- Retrieves experiment data from MLflow.
- Compares the total clicks for each model.
- Performs statistical tests to determine if there is a significant difference between the models' performance.