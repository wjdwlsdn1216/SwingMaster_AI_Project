import yaml
from easydict import EasyDict as edict

def update_config(config_file):
    # import os
    # print("=================================")
    # print(config_file)
    # print (os.path.abspath(config_file) )
    # print("=================================")
    with open(config_file) as f:
        config = edict(yaml.load(f, Loader=yaml.FullLoader))
        return config
