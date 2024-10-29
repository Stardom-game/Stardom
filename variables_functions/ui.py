import pygame
import keyboard
from variables_functions import variables
from variables_functions import ui_elements, physics
from variables_functions import serialiser, rocketbuildui
import os


def close():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            variables.running = False
def menu_action():
    change_mode("building")
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    variables.musiccounter = 0
    pygame.mixer.music.load(variables.sounds["VAB"], "wav")
    pygame.mixer.music.play(loops=-1)
    
def build_action():
    change_mode("building")
    pygame.mixer.music.load(variables.sounds["VAB"], "wav")
    pygame.mixer.music.play()
    variables.musiccounter = 0


def setup():
    pygame.display.set_caption("Stardom", "-test version 1")
    change_mode("main_menu")

def update():
    if variables.MODE == "main_menu":
        update_main_menu_stars()

def placeholder():
    pass



def update_mouse():
    variables.mouseX, variables.mouseY = pygame.mouse.get_pos()
    variables.mousePos = pygame.mouse.get_pos()
    variables.mouseRect.x, variables.mouseRect.y = variables.mousePos
    variables.mouseCollision = False
    variables.leftclick, variables.middleclick, variables.rightclick = pygame.mouse.get_pressed()
def update_keys():
    variables.keys = pygame.key.get_pressed()
def update_main_menu_stars():
    variables.screen.blit(variables.menubg1, (variables.bg1location1, 0))
    variables.screen.blit(variables.menubg1, (variables.bg1location1 + variables.menubg1.get_width(), 0))
    variables.bg1location1 -= 0.5
    if variables.bg1location1 == -1 * variables.menubg1.get_width():
        variables.bg1location1 = 0
def update_buttons():
    for button in variables.buttons:
        button.update(variables.screen)



def fullscreen():
    if keyboard.is_pressed("F11"):
        pygame.display.toggle_fullscreen()


def change_mode(new_mode):
    variables.buttons = []
    variables.MODE = new_mode

    if variables.MODE == "main_menu":
        variables.buttons.append(
            ui_elements.Button(variables.screen, variables.screen.get_width() / 2 - 250, variables.screen.get_height() / 2 - 125,
                               500, 250, variables.orange, variables.white, "consolas", 15, 20,
                               "", variables.images["menubutton"], "main_menu_button", menu_action, None,True))
    if variables.MODE == "simulation":
        variables.buttons.append(
            ui_elements.Button(variables.screen, 100, 0,
                               200, 100, variables.orange, variables.white, "consolas", 15, 20,
                               "save", variables.images["blank"], "save_button", serialiser.save, None,False, True,
                               variables.white))
        variables.buttons.append(
            ui_elements.Button(variables.screen, 400, 0,
                               200, 100, variables.orange, variables.white, "consolas", 15, 20,
                               "load", variables.images["blank"], "load_button", serialiser.load, None,False, True, variables.white))
        variables.buttons.append(
            ui_elements.Button(variables.screen, 700, 0,
                               200, 100, variables.orange, variables.white, "consolas", 15, 20,
                               "build", variables.images["blank"], "startbuild_button", build_action, None,False, True, variables.white))

    if variables.MODE == "building":

        rocketbuildui.build_ui()
