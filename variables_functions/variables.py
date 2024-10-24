from pygame.locals import *
import pygame, pymunk, os
import pymunk.pygame_util
from select import select
import json

#from pymunk.examples.arrows import height

MODE = "main_menu"
zoom = (1,1)
cam_offset = (700,100)
dt = 0
keys = None
screen = pygame.display.set_mode((1500, 750), pygame.RESIZABLE)
screen_width = screen.get_width()
screen_height = screen.get_height()
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
trajectories = {}
trajectory_follows = {}
trajectory_follows_indexes = {}
orbital_corrections = {}

current_traj_follow = 0
last_current_traj_follow = 0
to_follow = None

simulation_body = None
simulation_positions = []
simulation_velocities = []
simulation_active = False
simulate_per_frame = 50
simulate_frames = 1500
simulated_frames = 0

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
    "planet": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "earth.png")).convert_alpha(), (10000, 10000)),
    "menubutton": pygame.image.load(os.path.join(root_dir, "images", "homescreen_button.png")),
    "commandpodbutton": pygame.image.load(os.path.join(root_dir, "images", "commandpodbutton.png")).convert_alpha(),
    "commandpodussr": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "ussrcapsule.png")).convert_alpha(), (128,128)),
    "commandpodussr_unsized": pygame.image.load(os.path.join(root_dir, "images", "ussrcapsule.png")).convert_alpha(),
    "fueltankru": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "fueltankru.png")).convert_alpha(), (128,128)),
    "fueltankru_unsized": pygame.image.load(os.path.join(root_dir, "images", "fueltankru.png")).convert_alpha(),
    "engine1": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "engine1.png")).convert_alpha(), (128,128)),
    "engine1_unsized": pygame.image.load(os.path.join(root_dir, "images", "engine1.png")).convert_alpha(),
    "buildbg": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "buildbg.png")).convert_alpha(), (screen_width, screen_height)),
    "launchplatform": pygame.image.load(os.path.join(root_dir, "images", "launchplatform.png")).convert_alpha(),
    "commandpodusa": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "usacapsule.png")).convert_alpha(), (128, 128)),
    "commandpodusa_unsized": pygame.image.load(os.path.join(root_dir, "images", "usacapsule.png")).convert_alpha(),
    "sidebarbuildmenu": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "sidebarbuildmenu.png")).convert_alpha(), (91, 3000))

}
blank = pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha()
mouseX, mouseY = pygame.mouse.get_pos()
mousePos = pygame.mouse.get_pos()
mouseRect = pygame.rect.Rect((0,0), (1, 1))

physics_loading = False

draggingBlockNum = 0

selected = None




blocks = {

}
planets = {

}

joints = []
joints_in_space = []
rot_joints = []
rot_joints_in_space = []
joint_distances = []
joints_before_timewarp = []
test = 0
blockCollision = False
newBlockCooldown = 0
num_of_rockets = 0
exit = False


space.gravity = (0, 0)
space_trajectory.gravity = (0,0)

draw_options = pymunk.pygame_util.DrawOptions(screen)
clock = pygame.time.Clock()
fps = 60

selected_index = 0
selected_obj = None

force_offset = (0,0)

orbit_starting_point = (0,0)
orbit_correct_velocity = 0
orbit_should_correct = False

leftclick, middleclick, rightclick = False, False, False
tab_pressed = False
commandbuttonimg = pygame.image.load("images\\commandpodbutton.png").convert_alpha()
rocketfile = "save\\rocketsave.json"

numofparts = 0
parts = []
parts_sim = []
