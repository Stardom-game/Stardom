# mass in tonnes
# thrust in tonnes... i.e. maximum mass at altitude 0 for engine that can be lifted
# efficiency tonnes of fuel per second

from variables_functions import variables
engine1 = {
    "mass": 4,
    "thrust": 100,
    "efficiency": 0.4,
    "partclass": "engine",
#    "texture": variables.images["engine1"]
}
fueltankru = {
    "mass": 15,
    "fuel_mass": 14,
    "empty_mass": 1,
    "type": "liquid",
    "partclass": "fuel",
#    "texture": variables.images["fueltankru"]
}
commandpodussr = {
    "mass": 3,
    "cosmonauts": 2,
    "partclass": "commandmodule",
    "torque": 4500,
#    "texture": variables.images["commandpodussr"]

}
commandpodusa = {
    "mass": 3,
    "cosmonauts": 1,
    "partclass": "commandmodule",
    "torque": 4500,
#    "texture": variables.images["commandpodusa"]
}