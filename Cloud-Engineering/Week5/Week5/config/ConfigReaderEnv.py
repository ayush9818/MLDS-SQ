import sys
import yaml

def load_config(env):
    # Define the path for configuration files
    config_file = f"config_{env}.yaml"

    try:
        with open(config_file, "r") as yamlfile:
            config = yaml.load(yamlfile, Loader=yaml.FullLoader)
            return config
    except FileNotFoundError:
        print(f"Configuration file for environment '{env}' not found.")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <environment>")
        sys.exit(1)

    environment = sys.argv[1]  # Get the environment argument from command line
    config = load_config(environment)
    if config:
        print("Configuration loaded successfully:")
        print(config)
        # Access specific configuration settings as needed
        print("Name:", config['name'])
        print("Learning Rate:", config['lr'])
        print("Epochs:", config['epochs'])
