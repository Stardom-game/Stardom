import pygame
from variables_functions import variables
def blit_zoom_rect(obj, rect):
    variables.screen.blit(pygame.transform.scale(obj, (variables.zoom[0] * obj.get_width(), variables.zoom[1] * obj.get_height())), (rect.topleft[0] * variables.zoom[0], rect.topleft[1] * variables.zoom[1]))
def blit_zoom(obj, pos):
    variables.screen.blit(pygame.transform.scale(obj, (variables.zoom[0] * obj.get_width(), variables.zoom[1] * obj.get_height())), (pos[0] * variables.zoom[0], pos[1] * variables.zoom[1]))