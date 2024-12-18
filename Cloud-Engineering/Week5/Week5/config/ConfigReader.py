
import yaml
import json
import pprint

print("Reading configuration file.. ")
with open("config_sample.yaml", "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    pprint.pprint(config)

    #print out a few config settings
    print("Name:", config['name'])
    print("Learning Rate:", config['lr'])
    print("Epochs:", config['epochs'])