##--IMPORTS--##

import json
import pygame
import pymunk
import keyboard
from variables_functions import variables, physics
from variables_functions import ui_elements, ui, zoomer
from variables_functions.variables import numofparts, num_of_rockets, moving_part, moving
import os


##--BUILDING FUNCTIONS--##

if len(variables.parts) == 0:
    a = 50
else:
    a = 0
def make_ussrcommandpod():
    variables.moving_part = [["commandpodussr", "mouseX", "mouseY"], ["commandpodussr", "mouseX", "mouseY", 31, 31, 10]]

def make_fueltank():
    variables.moving_part = [["fueltankru", "mouseX", "mouseY"], ["fueltankru", "mouseX", "mouseY", 31, 31, 10]]

def make_engine1():
    variables.moving_part = [["engine1", "mouseX", "mouseY"], ["engine1", "mouseX", "mouseY", 31, 31, 10]]

def make_commandpodusa():
    variables.moving_part = [["commandpodusa", "mouseX", "mouseY"], ["commandpodusa", "mouseX", "mouseY", 31, 31, 10]]

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
    variables.num_of_rockets += 1
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
def zoom_in():
    variables.zoomui = (variables.zoomui[0] + 0.4, variables.zoomui[1] + 0.4)
def zoom_out():
    if variables.zoomui[0] > 0.4:
        variables.zoomui = (variables.zoomui[0] - 0.4, variables.zoomui[1] - 0.4)
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
                           variables.white, variables.black, "consolas", 15, 20, "",
                           pygame.transform.scale(variables.images["commandpodussr"], (62, 62)), "summon soviet command module", make_ussrcommandpod,
                           hide_fill=True, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 82, 100, 75,
                                                variables.white, variables.black, "consolas", 15, 20, "",
                                                pygame.transform.scale(variables.images["commandpodusa"], (62, 62)),
                                                "summon usa command pod", make_commandpodusa,
                                                hide_fill=True, outline=False, outlinecolor=(255, 255, 255),
                                                outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 164, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "",
                           pygame.transform.scale(variables.images["fueltankru"], (62, 62)), "summon fuel tank", make_fueltank,
                           hide_fill=True, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, 20, 246, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "",
                           pygame.transform.scale(variables.images["engine1"], (62, 62)), "summon engine1", make_engine1,
                           hide_fill=True, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))



    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 100, variables.screen_width-75, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Clear",
                           variables.blank, "Clear screen", clearscreen,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen.get_width() - 100, variables.screen.get_height() - 165, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Save",
                           variables.blank, "Saverocket", saverocket,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen.get_width() - 100, variables.screen.get_height() - 255, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Load",
                           variables.blank, "Loadrocket", loadrocket,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(
        ui_elements.Button(variables.screen, variables.screen.get_width() - 150, variables.screen.get_height() - 165,
                           30, 30,
                           variables.white, variables.black, "consolas", 15, 20, "+",
                           variables.blank, "zoomin", zoom_in,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(
        ui_elements.Button(variables.screen, variables.screen.get_width() - 150, variables.screen.get_height() - 255,
                           30, 30,
                           variables.white, variables.black, "consolas", 15, 20, "-",
                           variables.blank, "zoomout", zoom_out,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
def update():
    variables.screen.blit(pygame.transform.scale(variables.images["buildbg"], (variables.screen.get_width(), variables.screen.get_height())), (0, 0))
    variables.screen.blit(pygame.transform.scale(variables.images["sidebarbuildmenu"], (140, 3000)), (0, 0))
    for part in variables.parts:
        #variables.screen.blit(variables.images[part[0]], (variables.screen_width/2, variables.screen_height-10+variables.numofparts*31))
        zoomer.blit_zoom_ui(variables.images[part[0]],
                                        (part[1], part[2]))
    if variables.moving_part != []:
        zoomer.blit_zoom_ui(variables.images[variables.moving_part[0][0]], (variables.mousePos[0] / variables.zoomui[0], variables.mousePos[1] / variables.zoomui[1]))
        if not variables.leftclick: #If leftclick is just pressed

            part = variables.moving_part[0]
            part = [(variables.mouseX / variables.zoomui[0] if l == "mouseX"
                     else (variables.mouseY / variables.zoomui[1]  if l == "mouseY" else
                           l
                           )) for l in part] #Replaces "mouseX" and "mouseY" with variables.mouseX and variables.mouseY

            part_sim = variables.moving_part[1]
            part_sim = [(variables.mouseX / variables.zoomui[0] if l == "mouseX"
                         else (variables.mouseY / variables.zoomui[1] if l == "mouseY"
                               else l
                               )) for l in part_sim]

            variables.parts.append(part)
            variables.parts_sim.append(part_sim)
            variables.numofparts += 1
            variables.moving_part = []
