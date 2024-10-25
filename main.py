import os
from multiprocessing.forkserver import read_signed
import json
import pygame, pymunk, time
import keyboard
from pymunk.pygame_util import DrawOptions

from variables_functions import variables, ui, physics, serialiser, planets, rocketbuildui, camera, ui_elements
from pygame.locals import *

#physics.create_boundaries(variables.space, variables.screen_width, variables.screen_height)
ui.setup()
while variables.running:
    variables.screen.fill(variables.black)
    if variables.MODE == "building":
        rocketbuildui.update()

    ui.update()
    ui.close()
    ui.update_buttons()
    ui.update_mouse()
    ui.update_keys()
    planets.setup()
    if variables.MODE == "simulation":
        physics.update_cooldown()
        physics.update_movement()
        physics.lerp_angular_velocity()
        physics.create_parts()
        planets.update()
        #physics.draw(DrawOptions(variables.screen))
        camera.update()
        physics.update_screen()

    #if variables.to_follow != None:
      #  variables.screen.blit(variables.images["wood"], (variables.to_follow[0], variables.to_follow[1]))

    pygame.display.update()
