import pygame, pymunk

from variables_functions import physics, planet, variables, ui


def setup():
    variables.planets["Alpha"] = planet.Planet(1500, variables.screen_height * 1.5, 700, "planet")
def update():
    for planet in variables.planets.values():
        planet.update()