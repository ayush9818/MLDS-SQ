import sys
import yaml
import logging

class ConfigReader:
    @classmethod
    def load_config(cls, env):
        # Define the path for configuration files
        config_file = f"config_{env}.yaml"
        config_path = "../config/"
        config_file =  config_path + config_file
        try:
            with open(config_file, "r") as yamlfile:
                config = yaml.load(yamlfile, Loader=yaml.FullLoader)
                return config
        except FileNotFoundError:
            logging.error(f"Configuration file for environment '{env}' not found.")
            return None