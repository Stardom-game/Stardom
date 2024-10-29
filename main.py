import os
from multiprocessing.forkserver import read_signed
import json
import pygame, pymunk, time
import keyboard
from pymunk.pygame_util import DrawOptions
import time as t
from variables_functions import variables, ui, physics, serialiser, planets, rocketbuildui, camera, ui_elements
from pygame.locals import *
pygame.init()
pygame.mixer.music.load(variables.sounds["main"], "wav")
pygame.mixer.music.play(loops=-1)
#physics.create_boundaries(variables.space, variables.screen_width, variables.screen_height)
ui.setup()
while variables.running:
    variables.screen.fill(variables.black)
    variables.musiccounter += 1
    #if variables.MODE == "main_menu":
        # if variables.musiccounter%(72) == 0:
        #     pygame.mixer.music.load(variables.sounds["main"], "wav")
        #     pygame.mixer.music.play()
    # if variables.MODE == "building" and variables.musiccounter/69 == 1:
    #     pygame.mixer.music.load(variables.sounds["VAB"], "wav")
    #     pygame.mixer.music.play()
    # if variables.MODE == "simulation" and variables.musiccounter/78 == 1:
    #     pygame.mixer.music.load(variables.sounds["simulation"], "wav")
    #     pygame.mixer.music.play()
    if variables.MODE == "building":
        # if variables.musiccounter % 69 == 0:
        #     pygame.mixer.music.load(variables.sounds["VAB"], "wav")
        #     pygame.mixer.music.play()
        rocketbuildui.update()
        ui.close()
    ui.update()
    ui.close()
    ui.update_buttons()
    ui.update_mouse()
    ui.update_keys()
    planets.setup()
    if variables.MODE == "simulation":
        # if variables.musiccounter%78 == 0:
        #     pygame.mixer.music.load(variables.sounds["simulation"], "wav")
        #     pygame.mixer.music.play()
        physics.update_cooldown()
        ui.close()
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
