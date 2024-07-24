import json 
import yaml

def yaml_load(dir): 
    result = yaml.load(open(dir, 'r'), Loader=yaml.FullLoader)
    return result

def dict_to_json(content: dict): 
    result = json.dumps(content, indent=4)
    return result
