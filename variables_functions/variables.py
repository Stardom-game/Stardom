from pygame.locals import *
import pygame, pymunk, os
import pymunk.pygame_util
from select import select
import json

#from pymunk.examples.arrows import height

MODE = "main_menu"
dt = 0
keys = None
screen_width = 1500
screen_height = 750
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
space = pymunk.Space()
space_trajectory = pymunk.Space()
white = (255, 255, 255)
black = (0, 0, 0)
gray = (127, 127, 127)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
magenta = (255, 0, 255)
orange = 255,127,80
darkorange = 255,99,71

buttons = []
building_uis = []
trailPoints = []
trajectory = []

current_traj_follow = 0
to_follow = None

current_accel = (0,0)
orbit_direction = 1

physics_speed = 1

DEFAULT_IMAGE_SIZE = (screen.get_width(), screen.get_height())
running = True
root_dir = (os.path.abspath(os.path.join(os.getcwd())))
menubg1 = pygame.image.load(os.path.join(root_dir, "images", "home_bg_fill1.png"))
menubg1  = pygame.transform.scale(menubg1, (2000, 1000))
bg1location1 = 0




woodRect = pygame.rect.Rect((0,0), (16, 16))


stoneRect = pygame.rect.Rect((0,16), (16, 16))

images = {
    "blank": pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha(),
    "wood": pygame.image.load(os.path.join(root_dir, "images", "wood.png")).convert_alpha(),
    "stone": pygame.image.load(os.path.join(root_dir, "images", "stone.png")).convert_alpha(),
    "planet": pygame.image.load(os.path.join(root_dir, "images", "earth.png")).convert_alpha(),
    "menubutton": pygame.image.load(os.path.join(root_dir, "images", "homescreen_button.png")),
    "commandpodbutton": pygame.image.load(os.path.join(root_dir, "images", "commandpodbutton.png")).convert_alpha(),
    "commandpodussr": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "commandmodule.png")).convert_alpha(), (128,128)),
    "fueltankru": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "fueltankru.png")).convert_alpha(), (128,128)),
    "engine1": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "engine1.png")).convert_alpha(), (128,128)),
    "buildbg": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "buildbg.png")).convert_alpha(), (screen_width, screen_height))
}
blank = pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha()
mouseX, mouseY = pygame.mouse.get_pos()
mousePos = pygame.mouse.get_pos()
mouseRect = pygame.rect.Rect((0,0), (1, 1))

physics_loading = False

draggingBlockNum = 0




blocks = {

}
planets = {

}


test = 0
blockCollision = False
newBlockCooldown = 0

exit = False


space.gravity = (0, 0)
space_trajectory.gravity = (0,0)

draw_options = pymunk.pygame_util.DrawOptions(screen)
clock = pygame.time.Clock()
fps = 60

selected_index = 0
selected_obj = None

force_offset = (0,0)

leftclick, middleclick, rightclick = False, False, False
tab_pressed = False
commandbuttonimg = pygame.image.load("images\\commandpodbutton.png").convert_alpha()
rocketfile = "save\\rocketsave.json"

numofparts = 0
