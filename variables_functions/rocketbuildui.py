##--IMPORTS--##

import json
import pygame
import pymunk
import keyboard
from variables_functions import variables, physics
from variables_functions import ui_elements, ui
from variables_functions.variables import numofparts
import os

##--BUILDING FUNCTIONS--##

if len(variables.parts) == 0:
    a = 50
else:
    a = 0
def make_ussrcommandpod():
    variables.parts.append(["commandpodussr", variables.screen_width/2, a+variables.numofparts*128])
    variables.parts_sim.append(["commandpodussr_unsized", 0, 0 + variables.numofparts * 31, 31, 31, 10])
    variables.numofparts += 1

def make_fueltank():
    variables.parts.append(["fueltankru", variables.screen_width/2, a+variables.numofparts*128])
    variables.parts_sim.append(["fueltankru_unsized", 0, 0 + variables.numofparts * 31, 31, 31, 10])
    variables.numofparts += 1

def make_engine1():
    #Next time make the origin of all points the same as the minimum empty position (i.e. all rockets start from 0,0 regardless of where they are built)
    variables.parts.append(["engine1", variables.screen_width/2, a+variables.numofparts*128])
    variables.parts_sim.append(["engine1_unsized", 0, 0 + variables.numofparts * 31, 31, 31, 10])
    variables.numofparts += 1

def back():
    ui.change_mode("main_menu")
def get_dimensions_of_rocket():
    min_height = 0
    min_width = 0
    for part in variables.parts_sim:
        if part[1] + part[3] > min_width:
            part_pos_width = part[1] + part[3]
            min_width = part_pos_width
        if part[2] + part[4] > min_height:
            part_pos_height = part[2] + part[4]
            min_height = part_pos_height
    return [min_width, min_height]
def compound_rocket_img():
    rocket_dims = get_dimensions_of_rocket()
    out_img = pygame.Surface((rocket_dims[0], rocket_dims[1]), pygame.SRCALPHA)

    for part in variables.parts_sim:
        out_img.blit(variables.images[part[0]], (part[1], part[2]))
    #pygame.image.save(out_img, "test.png")
    return out_img

def launch():
    ui.change_mode("simulation")
    #
    rocket_dimensions = get_dimensions_of_rocket()
    variables.images["rocket"] = compound_rocket_img()
    #physics.create_block("rocket", 750,400,rocket_dimensions[0], rocket_dimensions[1], 30, 0, 0)
    original_part = None
    i = 0
    for part in variables.parts_sim:

        block_id = physics.create_block(part[0], 750+part[1], 350+part[2], part[3], part[4], part[5],0, 0)
        block = variables.blocks[block_id]
        if i == 0:
            original_part = block
        else:
            physics.create_joint(block, original_part)
        i += 1
def clearscreen():
    variables.parts.clear()
    variables.numofparts = 0
def saverocket():
    root_dir = (os.path.abspath(os.path.join(os.getcwd())))
    save_path = (os.path.join(root_dir, "save"))
    with open(os.path.join(save_path, 'rocketsave.json'), 'w') as jsonfile:
        json.dump([variables.parts, variables.parts_sim], jsonfile)
        #json.dump(dump, jsonfile)
def loadrocket():
    root_dir = (os.path.abspath(os.path.join(os.getcwd())))
    save_path = (os.path.join(root_dir, "save"))
    with open(os.path.join(save_path, 'rocketsave.json'), 'r') as jsonfile:
        read = json.load(jsonfile)
        variables.parts, variables.parts_sim = read[0], read[1]


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
                           variables.blank, "summon soviet command module", make_ussrcommandpod,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 140, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Make Fuel Tank",
                           variables.blank, "summon fuel tank", make_fueltank,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 280, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Make Engine",
                           variables.blank, "summon engine1", make_engine1,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width-100, variables.screen_height-75, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Clear",
                           variables.blank, "Clear screen", clearscreen,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 100, variables.screen_height - 165, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Save",
                           variables.blank, "Saverocket", saverocket,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 100, variables.screen_height - 255, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Load",
                           variables.blank, "Loadrocket", loadrocket,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
def update():
    variables.screen.blit(variables.images["buildbg"], (0, 0))
    for part in variables.parts:
        #variables.screen.blit(variables.images[part[0]], (variables.screen_width/2, variables.screen_height-10+variables.numofparts*31))
        variables.screen.blit(variables.images[part[0]],
                                        (part[1], part[2]))