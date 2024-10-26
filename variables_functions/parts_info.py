# mass in tonnes
# thrust in tonnes... i.e. maximum mass at altitude 0 for engine that can be lifted
# efficiency tonnes of fuel per second

from variables_functions import variables


parts = {
"commandpodussr": {
        "width": 31,
        "height": 32,
        "mass": 4,
        "image": variables.images["commandpodussr"],
        "class": "control"
    },
    "commandpodusa": {
        "width": 31,
        "height": 32,
        "mass": 4,
        "image": variables.images["commandpodusa"],
        "class": "control"
    },
"probecore": {
        "width": 31,
        "height": 32,
        "mass": 2,
        "image": variables.images["probecore"],
        "class": "control"
    },
    "engine1": {
        "width": 31,
        "height": 32,
        "mass": 4,
        "image": variables.images["engine1"],
        "class": "engine",
        "thrust": 100,
    },
    "fueltankru": {
        "width": 31,
        "height": 32,
        "mass": 8,
        "image": variables.images["fueltankru"],
        "class": "fuel"
    },

    "parachuteclosed": {
        "width": 31,
        "height": 32,
        "mass": 0.5,
        "image": variables.images["parachuteclosed"],
        "class": "aerodynamics"
    },
    "stageseparator": {
        "width": 31,
        "height": 5,
        "mass": 1,
        "image": variables.images["stageseparator"],
        "class": "staging"
    },
    "nosecone": {
        "width": 31,
        "height": 32,
        "mass": 1.5,
        "image": variables.images["nosecone"],
        "class": "aerodynamics"
    }
}
