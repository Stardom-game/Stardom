import pygame, pymunk

from variables_functions import physics, planet, variables, ui


def setup():
    variables.planets["Alpha"] = planet.Planet(variables.screen_width/2, variables.screen_height/2, 100, "planet")
def update():
    for planet in variables.planets.values():
        planet.update()