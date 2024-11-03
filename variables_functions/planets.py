import pygame, pymunk

from variables_functions import physics, planet, variables, ui


def setup():
    variables.planets["Alpha"] = planet.Planet(750, 150000900, 150000000, "planet")
    #1 pixel = 4m
def update():
    for planet in variables.planets.values():
        planet.update()