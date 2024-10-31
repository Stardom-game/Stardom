
#! Imports
import os
from multiprocessing.forkserver import read_signed
import json
import pygame, pymunk, time
import keyboard
from pymunk.pygame_util import DrawOptions
from variables_functions import variables, ui, physics, serialiser, planets, rocketbuildui, camera, ui_elements
from pygame.locals import *
import time
import sys
from tqdm import tqdm
from datetime import datetime

#! Init
pygame.init()
pygame.mixer.music.load(variables.sounds["main"], "wav")
pygame.mixer.music.play(loops=-1)
#physics.create_boundaries(variables.space, variables.screen_width, variables.screen_height)
ui.setup()

def run():
    while variables.running:
        variables.screen.fill(variables.black)
        if variables.MODE == "building":
            rocketbuildui.update()
            ui.close()

        ui.update()
        if variables.DEBUG == True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"DEBUG: UI Update at {now}")
        ui.close()
        ui.update_buttons()
        ui.update_mouse()
        ui.update_keys()
        planets.setup()
        if variables.MODE == "simulation":
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

if __name__ == "__main__":
    if variables.DEBUG == True:
        print("DEBUG: Not lib, running...")
    try:
        if variables.DEBUG == True:
            print("DEBUG: run() issued!")
        run()
    except KeyboardInterrupt:
        print("Shutting down...")
        for i in tqdm(range(20)):
            time.sleep(0.05)
        if variables.DEBUG == True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(f"DEBUG: Sys exit issued at {now}")
        sys.exit()
    except Exception as e:
        print(f"Encountered error {e}. Please add a github issue.")