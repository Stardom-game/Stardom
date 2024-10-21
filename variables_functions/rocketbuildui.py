##--IMPORTS--##

import json
import pygame
import pymunk
import keyboard
from variables_functions import variables
from variables_functions import ui_elements, ui

##--BUILDING FUNCTIONS--##
parts = []
if len(parts) == 0:
    a = 50
else:
    a = 0
def make_commandpod():
    parts.append(["commandpodussr", variables.screen_width/2, a+variables.numofparts*128])
    variables.numofparts += 1

def make_fueltank():
    parts.append(["fueltankru", variables.screen_width/2, a+variables.numofparts*128])
    variables.numofparts += 1

def make_engine1():
    parts.append(["engine1", variables.screen_width/2, a+variables.numofparts*128])
    variables.numofparts += 1

def back():
    ui.change_mode("main_menu")

def launch():
    ui.change_mode("simulation")
        
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
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width-125, 20, 100, 75,
                            variables.white, variables.black, "consolas", 15, 20, "<",
                            variables.blank, "back button", back,
                            hide_fill=False, outline=False, outlinecolor=(255, 255, 255),
                            outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 125, 140, 100, 75,
                            variables.white, variables.black, "consolas", 15, 20, "Launch",
                            variables.blank, "back button", launch,
                            hide_fill=False, outline=False, outlinecolor=(255, 255, 255),
                            outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 0, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Make Command Module",
                           variables.blank, "summon command module", make_commandpod,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 140, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Make Fuel Tank",
                           variables.blank, "summon fuel tank", make_fueltank,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 280, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Make Engine",
                           variables.blank, "summon engine1", make_engine1,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))

def update():
    variables.screen.blit(variables.images["buildbg"], (0, 0))
    for part in parts:
        #variables.screen.blit(variables.images[part[0]], (variables.screen_width/2, variables.screen_height-10+variables.numofparts*31))
        variables.screen.blit(variables.images[part[0]],
                              (part[1], part[2]))