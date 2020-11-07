import json


def load_json(json_path):
    '''Function to load a json'''
    with open(json_path) as f:
        data = json.load(f)
    return data