import pandas as pd
from src.trainer import Trainer


def get_trainer_config():
    """
    Fixture to provide trainer configuration.
    """
    return {
        "model_name": "RandomForestClassifier",
        "params": {"n_estimators": 100},
        "train_features": ["feature1", "feature2", "feature3"],
        "test_size": 0.2,
        "random_state": 42,
    }


def get_sample_data():
    """
    Fixture to provide sample data.
    """
    return pd.DataFrame(
        {
            "feature1": [1, 2, 3, 4, 5],
            "feature2": [6, 7, 8, 9, 10],
            "feature3": [11, 12, 13, 14, 15],
            "target": [0, 1, 0, 1, 0],
        }
    )


def test_save_data_valid_directory(tmp_path):
    """
    Test saving data to a valid directory.
    """
    trainer = Trainer({})
    sample_data = get_sample_data()
    train_data = sample_data.iloc[:3]
    test_data = sample_data.iloc[3:]
    save_dir = tmp_path / "data"

    trainer.save_data(train_data, test_data, save_dir)

    assert (save_dir / "train_data.csv").exists()
    assert (save_dir / "test_data.csv").exists()


def test_save_model_success(tmp_path):
    """
    Test saving model to a valid path.
    """
    trainer_config = get_trainer_config()
    trainer = Trainer(trainer_config)
    sample_data = get_sample_data()
    model, _, _ = trainer.train_model(sample_data)
    save_path = tmp_path / "model.pkl"

    trainer.save_model(model, save_path)

    assert save_path.exists()
