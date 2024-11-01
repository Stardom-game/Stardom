from pygame.locals import *
import pygame, pymunk, os
import pymunk.pygame_util
from select import select
import json
import platform

#from pymunk.examples.arrows import height

MODE = "main_menu"
zoom = (1,1)
zoomui = (3,3)
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

current_os = platform.system()

if current_os == "Windows":
    images = {
        "blank": pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha(),
        "wood": pygame.image.load(os.path.join(root_dir, "images", "wood.png")).convert_alpha(),
        "stone": pygame.image.load(os.path.join(root_dir, "images", "stone.png")).convert_alpha(),
        "planet": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "earth.png")).convert_alpha(), (2000, 2000)),
        "menubutton": pygame.image.load(os.path.join(root_dir, "images", "homescreen_button.png")),
        "commandpodbutton": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "commandpodbutton.png")).convert_alpha(), (32, 32)),
        "commandpodussr": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "ussrcapsule.png")).convert_alpha(), (32, 32)),
        "fueltankru": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "fueltankru.png")).convert_alpha(), (32, 32)),
        "engine1": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "engine1.png")).convert_alpha(), (32, 32)),
        "buildbg": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "buildbg.png")).convert_alpha(), (screen_width, screen_height)),
        "launchplatform": pygame.image.load(os.path.join(root_dir, "images", "launchplatform.png")).convert_alpha(),
        "commandpodusa": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "usacapsule.png")).convert_alpha(), (32, 32)),
        "sidebarbuildmenu": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "sidebarbuildmenu.png")).convert_alpha(), (91, screen_height)),
        "parachuteclosed": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "parachute(closed).png")).convert_alpha(), (32, 32)),
        "parachuteopen": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "parachute(open).png")).convert_alpha(), (32, 32)),
        "probecore": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "probecore.png")).convert_alpha(), (32, 32)),
        "stageseparator": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "decoupler.png")).convert_alpha(), (32, 4)),
        "nosecone": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "nosecone.png")).convert_alpha(), (32, 32)),
    }
elif current_os == "Darwin":
    images = {
        "blank": pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha(),
        "wood": pygame.image.load(os.path.join(root_dir, "images", "wood.png")).convert_alpha(),
        "stone": pygame.image.load(os.path.join(root_dir, "images", "stone.png")).convert_alpha(),
        "planet": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "earth.png")).convert_alpha(), (2000, 2000)),
        "menubutton": pygame.image.load(os.path.join(root_dir, "images", "homescreen_button.png")),
        "commandpodbutton": pygame.transform.scale(pygame.image.load("images/commandpodbutton.png").convert_alpha(), (32, 32)), # temp macos fix
        "commandpodussr": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "ussrcapsule.png")).convert_alpha(), (32, 32)),
        "fueltankru": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "fueltankru.png")).convert_alpha(), (32, 32)),
        "engine1": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "engine1.png")).convert_alpha(), (32, 32)),
        "buildbg": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "buildbg.png")).convert_alpha(), (screen_width, screen_height)),
        "launchplatform": pygame.image.load(os.path.join(root_dir, "images", "launchplatform.png")).convert_alpha(),
        "commandpodusa": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "usacapsule.png")).convert_alpha(), (32, 32)),
        "sidebarbuildmenu": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "sidebarbuildmenu.png")).convert_alpha(), (91, screen_height)),
        "parachuteclosed": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "parachute(closed).png")).convert_alpha(), (32, 32)),
        "parachuteopen": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "parachute(open).png")).convert_alpha(), (32, 32)),
        "probecore": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "probecore.png")).convert_alpha(), (32, 32)),
        "stageseparator": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "decoupler.png")).convert_alpha(), (32, 4)),
        "nosecone": pygame.transform.scale(pygame.image.load(os.path.join(root_dir, "images", "nosecone.png")).convert_alpha(), (32, 32)),
    }

blank = pygame.image.load(os.path.join(root_dir, "images", "blank.png")).convert_alpha()
mouseX, mouseY = pygame.mouse.get_pos()
mousePos = pygame.mouse.get_pos()
snappedMousePos = pygame.mouse.get_pos()
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
prev_leftclick = False
tab_pressed = False

if current_os == "Windows":
    commandbuttonimg = pygame.image.load("images\\commandpodbutton.png").convert_alpha()
    rocketfile = "save\\rocketsave.json"
elif current_os == "Darwin":
    commandbuttonimg = pygame.image.load("images/commandpodbutton.png").convert_alpha()
    rocketfile = "save/rocketsave.json"


numofparts = 0
moving_part = []
moving = False
parts = []
parts_origin_zero = []
parts_sim = []
rocket_mass = 0
rocket_thrust = 0
engineon = False
rcson = False

space_key_last_pressed = False
r_key_last_pressed = False
t_key_last_pressed = False
numberofparts = []
sounds = {
    "main": "audio/mainost.wav",
    "VAB" : "audio/buildost.wav",
    "simulation" : "audio/piracy.wav"
}

DEBUG = True