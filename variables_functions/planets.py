import pygame, pymunk

from variables_functions import physics, planet, variables, ui


def setup():
    variables.planets["Alpha"] = planet.Planet(750, 2000, 1000, "planet")
def update():
    for planet in variables.planets.values():
        planet.update()