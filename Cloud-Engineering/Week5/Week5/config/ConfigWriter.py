import yaml

def write_config():
    config = {
        'name': 'Iris Classifier',
        'lr': 0.01,
        'epochs': 5,
        'batch_size': 32,
        'optimizer': 'Adam',
        'loss_function': 'Cross Entropy',
        'input_size': 4,
        'hidden_layers': [16, 8],
        'activation_function': 'ReLU',
        'output_size': 3,
        'dropout': 0.2,
        'regularization': {
            'type': 'L2',
            'lambda': 0.001
        },
        'metrics': ['Accuracy'],
        'validation_split': 0.2,
        'early_stopping': True,
        'patience': 3,
        'data_augmentation': 'None',
        'normalization': 'Min-Max Scaling',
        'weight_initialization': 'He Initialization',
        'learning_rate_scheduler': {
            'type': 'ReduceLROnPlateau',
            'factor': 0.1,
            'patience': 2,
            'threshold': 0.01
        },
        'gradient_clipping': True,
        'gradient_clip_value': 0.5,
        'model_checkpointing': True,
        'model_checkpoint_path': "./saved_models/iris_classifier_checkpoint.pth",
        'model_architecture': 'Feedforward Neural Network',
        'input_data_format': 'NumPy arrays',
        'output_data_format': 'Class predictions as integers',
        'training_data': 'Iris dataset',
        'data_preprocessing': ['Shuffle', 'Train-Test Split (80:20)', 'One-Hot Encoding for Labels'],
        'gpu_acceleration': True,
        'gpu_device': 'cuda:0',
        'random_seed': 42,
        'logging': True,
        'log_directory': "./logs/iris_classifier/",
        'verbosity_level': 'INFO',
        'experiment_name': 'Iris_Classifier_Experiment',
        'experiment_description': 'Building and training a neural network classifier for the Iris dataset.'
    }
    print("Writing configuration file.. ")

    with open("config_output.yaml", "w") as outfile:
        yaml.dump(config, outfile, default_flow_style=False)

    print("Configuration file 'config_output.yaml' has been created.")

write_config()