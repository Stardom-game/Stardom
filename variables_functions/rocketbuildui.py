##--IMPORTS--##

import json
import pygame
import pymunk
import keyboard
from variables_functions import variables, physics
from variables_functions import ui_elements, ui, zoomer
from variables_functions import parts_info
import os


partslist = []
##--BUILDING FUNCTIONS--##
pygame.freetype.init()
font = pygame.freetype.SysFont("Consolas", 15)



if len(variables.parts) == 0:
    a = 50
else:
    a = 0

def make_part(part):
    variables.moving_part = [part, "mouseX", "mouseY", parts_info.parts[part]["width"], parts_info.parts[part]["height"], parts_info.parts[part]["mass"]]
    variables.rocket_mass += parts_info.parts[part]["mass"]
    partslist.append(part)

    if parts_info.parts[part]["class"] == "engine":
        variables.rocket_thrust += parts_info.parts[part]["thrust"]
def back():
    ui.change_mode("main_menu")
def get_dimensions_of_rocket(get_min=False):
    max_height = 0
    min_height = 9999
    max_width = 0
    min_width = 9999
    for part in variables.parts:

        if part[1] + part[3] > max_width: #position + part_width
            part_pos_width = part[1] + part[3]
            max_width = part_pos_width
        if part[1] < min_width: #position
            part_pos_width2 = part[1]
            min_width = part_pos_width2
        if part[2] + part[4] > max_height:
            part_pos_height = part[2] + part[4]
            max_height = part_pos_height
        if part[2] < min_height:
            part_pos_height2 = part[2]
            min_height = part_pos_height2
    if not get_min:
        return [max_width-min_width, max_height-min_height]
    else:
        return [min_width, min_height]

def compound_rocket_img():
    rocket_dims = get_dimensions_of_rocket()
    rocket_pos = get_dimensions_of_rocket(True)
    out_img = pygame.Surface((rocket_dims[0], rocket_dims[1]), pygame.SRCALPHA)

    for part in variables.parts:
        out_img.blit(variables.images[part[0]], (part[1] - rocket_pos[0], part[2] - rocket_pos[1]))
    pygame.image.save(out_img, "test.png")
    return out_img
def calc_mass():
    variables.rocket_mass = 0
    for part in variables.parts:
        variables.rocket_mass += part[5]
def calc_thrust():
    variables.rocket_thrust = 0
    for part in variables.parts:
        part_name = part[0]
        part_data = parts_info.parts[part_name]
        if part_data["class"] == "engine":
            do_not_add_thrust = False
            for part_to_check in variables.parts:
                #This checks if each part is:
                #1. Below the engine
                #2. Has the same x position as the engine
                #3. Is not an engine itself
                #If all these conditions are satisfied, the thrust is not added on
                part_to_check_name = part_to_check[0]
                part_to_check_data = parts_info.parts[part_to_check_name]
                if (part_to_check[2] > part[2] and part_to_check[1] == part[1]) and part_to_check_data["class"] != "engine":
                    do_not_add_thrust = True
            if not do_not_add_thrust:
                variables.rocket_thrust += part_data["thrust"]
def launch():
    keyforlaunch = False
    for part in variables.parts:
        part_name = part[0]
        part_data = parts_info.parts[part_name]
        if part_data["class"] == "control":
            keyforlaunch = True
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(variables.sounds["simulation"], "wav")
    pygame.mixer.music.play(loops=-1)
    if variables.rocket_thrust > 0 and variables.rocket_mass <= variables.rocket_thrust and keyforlaunch:
        ui.change_mode("simulation")

    #
        rocket_dimensions = get_dimensions_of_rocket()
        variables.images["rocket"] = compound_rocket_img()
        variables.parts_origin_zero = find_part_coords_origin(variables.parts)
        calc_mass()
        calc_thrust()
        physics.create_block("rocket", 750,400,rocket_dimensions[0], rocket_dimensions[1], variables.rocket_mass, 0, 0, -1, (0,0), variables.parts_origin_zero, variables.rocket_thrust)
        original_part = None
        i = 0
        #for part in variables.parts:

        #    block_id = physics.create_block(part[0], 750+part[1], 350+part[2], part[3], part[4], part[5],0, 0)
        #    block = variables.blocks[block_id]
        #    if i == 0:
        #        original_part = block
        #    else:
        #        physics.create_joint(block, original_part)
        #    i += 1
        variables.num_of_rockets += 1
def find_part_coords_origin(parts):
    out = []
    origin_pos = get_dimensions_of_rocket(True)
    for part in parts:
        out.append([part[0], part[1]-origin_pos[0], part[2]-origin_pos[1], part[3], part[4], part[5]])
    return out
def clearscreen():
    variables.parts.clear()
    variables.numofparts = 0
    variables.currentrocket_mass = 0
def saverocket():
    root_dir = (os.path.abspath(os.path.join(os.getcwd())))
    save_path = (os.path.join(root_dir, "save"))
    with open(os.path.join(save_path, 'rocketsave.json'), 'w') as jsonfile:
        json.dump(variables.parts, jsonfile)
        #json.dump(dump, jsonfile)
def loadrocket():
    root_dir = (os.path.abspath(os.path.join(os.getcwd())))
    save_path = (os.path.join(root_dir, "save"))
    with open(os.path.join(save_path, 'rocketsave.json'), 'r') as jsonfile:
        read = json.load(jsonfile)
        variables.parts = read
    variables.parts_origin_zero = find_part_coords_origin(variables.parts)
    calc_mass()
    calc_thrust()

def zoom_in():
    variables.zoomui = (variables.zoomui[0] + 0.4, variables.zoomui[1] + 0.4)
def zoom_out():
    if variables.zoomui[0] > 0.4:
        variables.zoomui = (variables.zoomui[0] - 0.4, variables.zoomui[1] - 0.4)
def empty():
    pass
def build_ui():
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width-125, 20, 100, 75,
                            variables.white, variables.black, "consolas", 15, 20, "<",
                            variables.blank, "back button", back, None,
                            hide_fill=False, outline=False, outlinecolor=(255, 255, 255),
                            outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 125, 140, 100, 75,
                            variables.white, variables.black, "consolas", 15, 20, "Launch",
                            variables.blank, "back button", launch,None,
                            hide_fill=False, outline=False, outlinecolor=(255, 255, 255),
                            outlinethickness=5))
    part_num = 0
    for part in parts_info.parts.keys():
        part_image = parts_info.parts[part]["image"]

        variables.buttons.append(ui_elements.Button(variables.screen, 20, part_num * 70, 100, 75,
                               variables.white, variables.black, "consolas", 15, 20, "",
                               pygame.transform.scale(part_image, (62, 62)), "", make_part, part,
                               hide_fill=True, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))

        part_num += 1

    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen_width - 100, variables.screen_height-75, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Clear",
                           variables.blank, "Clear screen", clearscreen, None,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen.get_width() - 100, variables.screen.get_height() - 165, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Save",
                           variables.blank, "Saverocket", saverocket, None,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(ui_elements.Button(variables.screen, variables.screen.get_width() - 100, variables.screen.get_height() - 255, 100, 75,
                           variables.white, variables.black, "consolas", 15, 20, "Load",
                           variables.blank, "Loadrocket", loadrocket, None,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(
        ui_elements.Button(variables.screen, variables.screen.get_width() - 150, variables.screen.get_height() - 165,
                           30, 30,
                           variables.white, variables.black, "consolas", 15, 20, "+",
                           variables.blank, "zoomin", zoom_in, None,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
    variables.buttons.append(
        ui_elements.Button(variables.screen, variables.screen.get_width() - 150, variables.screen.get_height() - 255,
                           30, 30,
                           variables.white, variables.black, "consolas", 15, 20, "-",
                           variables.blank, "zoomout", zoom_out, None,
                           hide_fill=False, outline=False, outlinecolor=(255, 255, 255), outlinethickness=5))
def update():
    variables.screen.blit(pygame.transform.scale(variables.images["buildbg"], (variables.screen.get_width(), variables.screen.get_height())), (0, 0))
    variables.screen.blit(pygame.transform.scale(variables.images["sidebarbuildmenu"], (140, 3000)), (0, 0))
    my_font = pygame.font.SysFont('Segoe UI', 30)
    mass_surf = my_font.render('Mass: ' + str(variables.rocket_mass), True, variables.white)
    variables.screen.blit(mass_surf, (variables.screen_width-250, variables.screen_height-100))
    thrust_surf = my_font.render('Thrust: ' + str(variables.rocket_thrust), True, variables.white)
    variables.screen.blit(thrust_surf, (variables.screen_width - 250, variables.screen_height - 70))

    for part in variables.parts:
        #variables.screen.blit(variables.images[part[0]], (variables.screen_width/2, variables.screen_height-10+variables.numofparts*31))
        zoomer.blit_zoom_ui(variables.images[part[0]],
                                        (part[1], part[2]))
    if variables.moving_part != []:
        variables.snappedMousePos = variables.mousePos[0]//8*8, variables.mousePos[1]//8*8
        zoomer.blit_zoom_ui(variables.images[variables.moving_part[0]], ((variables.snappedMousePos[0]) // variables.zoomui[0], (variables.snappedMousePos[1]) // variables.zoomui[1]))
        if not variables.leftclick: #If leftclick is just pressed

            part = variables.moving_part
            part = [(variables.snappedMousePos[0] // variables.zoomui[0] if l == "mouseX"
                     else (variables.snappedMousePos[1] // variables.zoomui[1]  if l == "mouseY" else
                           l
                           )) for l in part] #Replaces "mouseX" and "mouseY" with variables.mouseX and variables.mouseY

            variables.parts.append(part)
            variables.numofparts += 1
            variables.moving_part = []
            calc_thrust()


