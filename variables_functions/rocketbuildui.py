##--IMPORTS--##

import json
import pygame
import pymunk
import keyboard
from variables_functions import variables
from variables_functions import ui_elements

##--BUILDING FUNCTIONS--##
parts = []
def make_commandpod():
    variables.numofparts += 1
    parts.append(["commandpodussr", variables.screen_width/2, 0+variables.numofparts*128])


##--CLASS BUILDUI--##

#class BuildUI:
#    def __init__(self, screen):
#        self.screen = screen
#        self.command = None#
#
#    def buildUI(self):
#        self.command = ui_elements.Button(variables.screen, 20, 20, 100, 50,
#                           variables.white, variables.black, "consolas", 15, 20, "Capsule",
#                           variables.commandbuttonimg, "summon command module", make_commandpod,
#                           hide_fill=True, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5)

def build_ui():
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 20, 100, 50,
                           variables.white, variables.black, "consolas", 15, 20, "",
                           variables.commandbuttonimg, "summon command module", make_commandpod,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))

def update():
    for part in parts:
        #variables.screen.blit(variables.images[part[0]], (variables.screen_width/2, variables.screen_height-10+variables.numofparts*31))
        variables.screen.blit(variables.images[part[0]],
                              (part[1], part[2]))