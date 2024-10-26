from variables_functions import variables
from variables_functions.variables import selected_obj
import pygame

def update():
    keys = variables.keys
    if variables.selected_obj is not None:
        variables.cam_offset = -variables.selected_obj.body.position + ((variables.screen_width/2),  (variables.screen_height/2))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEWHEEL:
            if event.y == 1:
                variables.zoom=variables.zoom[0] + 0.05, variables.zoom[1] + 0.05
            if event.y == -1:
                if variables.zoom[0] > 0.05:
                    variables.zoom=variables.zoom[0] - 0.05, variables.zoom[1] - 0.05
