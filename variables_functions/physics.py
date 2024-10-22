
import pygame, time
import pymunk
import pymunk.pygame_util
import math, random, os, json, keyboard, clock

from pygame import Vector2
from pymunk.pygame_util import DrawOptions

from variables_functions import variables
from variables_functions.variables import blocks, mouseX, mouseY, physics_loading, selected_obj, trailPoints, \
    physics_speed, current_accel, trajectory, space_trajectory, orbit_direction, orbit_starting_point, \
    orbit_correct_velocity, last_current_traj_follow


def ballistics(current_altitude, velocity, angle, acceleration):
    print("code will be added later")

def distance(x,y):
    return math.hypot(y[0]-x[0], y[1]-x[1])
def angle_of_vector(x, y):
    return math.degrees(math.atan2(-y,x))  # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors/64563327#64563327

def closest_point(pos, arr):
    i = 0
    out = None
    out_index = -1
    dis = 999
    for point in arr:
        if abs(distance(pos, point)) < dis:
            out_index = i
            dis = abs(distance(pos, point))
        i += 1
    return out_index

def draw(draw_options):
    #variables.screen.fill("black")
    variables.space_trajectory.debug_draw(draw_options)


def create_box(space, x, y, width, height, mass, elasticity, rotation = 0, circle=False, kinematic = False):
    body=None
    if not kinematic:
        body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    else:
        body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = (x, y)
    shape = None
    if not circle:
        shape = pymunk.Poly.create_box(body, (width, height))
    else:
        shape = pymunk.Circle(body, width)
    shape.mass = mass
    shape.elasticity = elasticity
    shape.friction = 2
    shape.color = (255, 0, 0, 100)
    shape.body.angle = rotation
    shape.body.center_of_gravity = (width/2, height/2)
    space.add(body, shape)

    return shape
def create_block(image, x, y, width, height, mass, elasticity, rotation=0, override_id=-1):
    newBlock = create_box(variables.space, x, y, width, height, mass, elasticity, rotation, False, False)

    newBlockRect = pygame.rect.Rect((0, 0), (width, height))
    newBlockRect.x, newBlockRect.y = x, y
    block_value = override_id
    if override_id == -1:
        block_value = len(variables.blocks.keys())
    variables.blocks[str(block_value)] = [image, newBlock, newBlockRect]
    update_rot(variables.blocks)
    variables.newBlockCooldown = 0


def get_save_data():
    data = []
    for obj in blocks.values():
        image = obj[0]
        shape = obj[1]
        body = shape.body
        rect = obj[2]
        data.append([image, shape.body.position.x, shape.body.position.y, rect.width, rect.height, shape.mass, shape.elasticity, body.angle])
    return data

def load_data(data):
    #THIS AUTOMATICALLY OVERWRITES THE EXISTING DATA, DO NOT DO " blocks = {} " IN THIS FUNCTION
    variables.physics_loading = True
    for obj in variables.blocks.values():

        shape = obj[1]

        variables.space.remove(shape)
        variables.space.remove(shape.body) #Removes all shapes and bodies from the pymunk simulation

    #Removes all blocks in the simulation with an ID higher than the highest ID in the save file, so all other blocks can be overwritten
    i = 0
    ids_to_pop = []
    for block_id in blocks.keys():
        if int(block_id) > len(data)-1:
            ids_to_pop.append(block_id)
    for id in ids_to_pop:
        blocks.pop(id, None)

    #Overwrites all blocks with the corresponding save file block
    for obj in data:
        create_block(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], i)
        i += 1

    variables.physics_loading = False
def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 5), (width, 10)],  # Ground
        [(width / 2, 5), (width, 10)],  # Ceiling
        [(5, height / 2), (10, height)],  # Left wall
        [(width - 5, height / 2), (10, height)]  # Right wall
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 2
        variables.space.add(body, shape)


def update_rot(data):
    if not physics_loading:
        for obj in data.values():
            rect = obj[2]
            block = obj[1]  # Get corresponding block for rect
            image = variables.images[obj[0]]
            blockRotationVector = block.body.rotation_vector  # Get Vector2 of body
            blockRotationAngle = angle_of_vector(blockRotationVector.x, blockRotationVector.y)  # Convert Vector2 into angle
            blockRotated = pygame.transform.rotate(image, blockRotationAngle)  # Rotate shape
            rect.centerx, rect.centery = math.floor(block.body.position.x), math.floor(
                block.body.position.y)  # Match rect position to body position
            variables.screen.blit(blockRotated, rect)
def move_selected(mode, obj):
    obj.torque = 0
    if mode == "right":
        obj.torque = 1500
    if mode == "left":
        obj.torque = -1500
    if mode == "up":
        obj.velocity += (0,-5)
    if mode == "down":
        obj.velocity += (0,5)
    if len(variables.blocks.keys()) > 0:
        obj = variables.blocks[str(variables.selected_index)][1]
        variables.orbit_starting_point = obj.body.position
        variables.orbit_correct_velocity = obj.body.velocity
        variables.trajectory, variables.trajectory_velocities = simulate_bodies(obj.body.position, obj.mass, obj.body.velocity)
        variables.orbit_should_correct = False
def apply_grav_accel(obj, kinematic = False, give_vel = False):

    planet = None
    for _planet in variables.planets.values():
        planet = _planet.body
        break
    dt_use = (1/variables.fps)
    force_multiplier = 1
    #grav_a = 1 * 10**5 * grav_accel(150, math.hypot(abs(obj.position.x-planet.position.x), abs(obj.position.y-planet.position.y)))
    distance_vector = ((planet.position.x - obj.position.x), (planet.position.y - obj.position.y))
    distance_ = math.hypot((planet.position.x - obj.position.x), (planet.position.y - obj.position.y))
    grav_a = dt_use * ((6.6743015 * 10**-11) * 5000000000000000000 / (distance_ ** 2))
    grav_a_angle = math.atan2(distance_vector[1], distance_vector[0])

    grav_a_vector = (grav_a * math.cos(grav_a_angle), grav_a * math.sin(grav_a_angle))
    variables.current_accel = grav_a_vector[0], grav_a_vector[1]
    #grav_a_vector = (grav_a * (obj.position.x - planet.position.x), grav_a * (obj.position.y - planet.position.y))
    #pymunk.Body.apply_force_at_world_point(obj, (grav_a_vector[0], grav_a_vector[1]), obj.position)
    if not kinematic:
        obj.apply_force_at_local_point((variables.current_accel[0] * dt_use * 60, variables.current_accel[1] * dt_use * 60))
    else:
        obj.velocity += (variables.current_accel[0] * 0.105* variables.physics_speed, variables.current_accel[1] * 0.105 * variables.physics_speed)

    #pymunk.Body.update_velocity(obj, grav_a_vector, 1, 1/variables.physics_speed)
def match_grav_accel(obj):
    #variables.current_traj_follow = closest_point(obj.body.position, variables.trajectory)

    if variables.physics_speed <= 1:
        if variables.orbit_should_correct and distance(variables.orbit_starting_point, obj.body.position) < 25:
            obj.body.position = variables.orbit_starting_point
            obj.body.velocity = variables.orbit_correct_velocity
            variables.orbit_should_correct = False
            print("correcting orbit")
        if distance(variables.orbit_starting_point, obj.body.position) > 150:
            variables.orbit_should_correct = True
        apply_grav_accel(obj.body, True)

    #print(distance(variables.orbit_starting_point, obj.body.position))

    if variables.physics_speed > 1:
        if variables.to_follow != None:
            #Change this first one to the apoapsis > x
            obj.body.position = variables.to_follow

        if variables.current_traj_follow + 1 < len(variables.trajectory):
            variables.to_follow = variables.trajectory[int(variables.current_traj_follow)][0], \
            variables.trajectory[int(variables.current_traj_follow)][1]

            variables.current_traj_follow += variables.physics_speed
            variables.last_current_traj_follow = variables.current_traj_follow

        else:
            variables.current_traj_follow = 0


def simulate_bodies(pos1, mass1, vel1):

    body1 = create_box(variables.space_trajectory, pos1[0], pos1[1], 16, 16, 10, 0, False, False, False)
    #body2 = create_box(variables.space_trajectory, pos2[0], pos2[1], 5, 5, 20, 0, True, True)
    body1.body.velocity = variables.selected_obj.body.velocity

    positions = []
    velocities = []
    for _ in range(1500):
        apply_grav_accel(body1.body, True)
        #body1.body.velocity = (0,5)
        positions.append(body1.body.position)
        velocities.append(body1.body.velocity)
        if len(positions) > 5 and abs(distance(body1.body.position, positions[0]) < 5):
            break
        update_trajectory_sim()

    return positions, velocities

def update_trajectory_sim():
    variables.space_trajectory.step(1/60)


def update(physics_speed):
    callAmount = 2
    for _ in range(callAmount):
        variables.space.step((1 / variables.fps * physics_speed) / callAmount)

    variables.clock.tick(variables.fps)
    variables.dt = variables.clock.get_fps()
    #if variables.clock.get_fps() > 0:
      #  print(1/variables.clock.get_fps())
    pygame.display.update()

def update_cooldown():


    # draw(space, screen, draw_options)
    variables.newBlockCooldown += 1
def update_movement():
    if str(variables.selected_index) in variables.blocks:
        obj = variables.blocks[str(variables.selected_index)][1]
        if variables.keys[pygame.K_TAB]:
            if variables.tab_pressed == False:

                variables.tab_pressed = True
                variables.selected_index += 1
                if variables.selected_index == len(variables.blocks.keys()):
                    variables.selected_index = 0
        else:
            variables.tab_pressed = False
        if variables.keys[pygame.K_w]:
            move_selected("up", obj.body)
        if variables.keys[pygame.K_s]:
            move_selected("down", obj.body)
        if variables.keys[pygame.K_a]:
            move_selected("left", obj.body)
        if variables.keys[pygame.K_d]:
            move_selected("right", obj.body)
        if variables.keys[pygame.K_9]:
            variables.physics_speed = 5
            variables.current_traj_follow = closest_point(obj.body.position, variables.trajectory)
        if variables.keys[pygame.K_1]:
            variables.current_traj_follow = closest_point(obj.body.position, variables.trajectory)
            obj.body.position = variables.trajectory[variables.current_traj_follow]
            obj.body.velocity = variables.trajectory_velocities[variables.current_traj_follow]
            variables.physics_speed = 1
            variables.current_traj_follow = 0

def lerp_angular_velocity():
    if variables.blocks!= {}:

        selected_obj = variables.blocks[str(variables.selected_index)][1]
        #variables.trailPoints.append(selected_obj.body.position)
        #if len(variables.trailPoints) > 5000:
        #    variables.trailPoints.pop(0)
        #if len(trailPoints) > 2:
        #    pygame.draw.lines(variables.screen, variables.white, False, trailPoints, 5)
        if len(variables.trajectory) > 2:
            pygame.draw.lines(variables.screen, variables.red, False, variables.trajectory, 5)
        match_grav_accel(selected_obj)
        variables.selected_obj = selected_obj

        if not variables.keys[pygame.K_a] and not variables.keys[pygame.K_d]:
            if abs(selected_obj.body.angular_velocity) > 0.02:
                selected_obj.body.angular_velocity = selected_obj.body.angular_velocity + (0-selected_obj.body.angular_velocity) * 0.05
            else:
                selected_obj.body.angular_velocity = 0

def create_parts():
    if variables.leftclick:
        if variables.newBlockCooldown > 10:  # and pygame.Rect.colliderect(mouseRect, woodRect):
            create_block("wood", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 16, 16, 10, 0, 0)
    if variables.rightclick:
        if variables.newBlockCooldown > 10:  # and pygame.Rect.colliderect(mouseRect, stoneRect):
            create_block("stone", pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 16, 16, 10, 0, 0)
def update_screen():
    variables.screen.blit(variables.images["wood"], variables.woodRect)
    variables.screen.blit(variables.images["stone"], variables.stoneRect)

    update_rot(blocks)
    update(variables.physics_speed)


def orbital_velocity(radius, velocity):
    circumference = 2* 3.142 * radius
    timeperiod = circumference/velocity
    orbital_vel = (2*3.142*radius)/timeperiod
    return orbital_vel

def grav_accel(mass, distance):
    grav_constant = 6.673
    return (grav_constant * mass) / distance **2
