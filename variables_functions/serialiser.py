import math, os, json, pygame
from variables_functions import variables, physics
root_dir = (os.path.abspath(os.path.join(os.getcwd())))
save_path = (os.path.join(root_dir, "save"))
def jsonDump():
    with open(os.path.join(save_path, 'save.json'), 'w') as jsonfile:
        todump = json.dumps(physics.get_save_data())
        json.dump(todump, jsonfile)
def jsonRead():
    with open(os.path.join(save_path, 'save.json'), 'r') as jsonfile:
        read = json.load(jsonfile)
        return json.loads(read)


def save():
    jsonDump()
def load():
    newData = jsonRead()
    physics.load_data(newData)