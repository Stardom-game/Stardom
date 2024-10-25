# mass in tonnes
# thrust in tonnes... i.e. maximum mass at altitude 0 for engine that can be lifted
# efficiency tonnes of fuel per second

from variables_functions import variables


parts = {
    "engine1": {
        "width": 32,
        "height": 32,
        "mass": 4,
        "image": variables.images["engine1"],
        "class": "engine",
        "thrust": 100,
    },
    "fueltankru": {
        "width": 32,
        "height": 32,
        "mass": 8,
        "image": variables.images["fueltankru"],
        "class": "fuel"
    },
    "commandpodussr": {
        "width": 32,
        "height": 32,
        "mass": 4,
        "image": variables.images["commandpodussr"],
        "class": "control"
    },
    "commandpodusa": {
        "width": 32,
        "height": 32,
        "mass": 4,
        "image": variables.images["commandpodusa"],
        "class": "control"
    }
}
