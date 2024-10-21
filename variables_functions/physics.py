
import pygame, time
import pymunk
import pymunk.pygame_util
import math, random, os, json, keyboard
from variables_functions import variables
from variables_functions.variables import blocks, mouseX, mouseY, physics_loading, selected_obj, trailPoints, \
    physics_speed, current_accel


def ballistics(current_altitude, velocity, angle, acceleration):
    print("code will be added later")


def angle_of_vector(x, y):
    return math.degrees(math.atan2(-y,x))  # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors/64563327#64563327


def draw(space, screen, draw_options):
    #variables.screen.fill("black")
    variables.space.debug_draw(draw_options)


def create_box(space, x, y, width, height, mass, elasticity, rotation = 0, circle=False):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)

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
    variables.space.add(body, shape)

    return shape
def create_block(image, x, y, width, height, mass, elasticity, rotation=0, override_id=-1):
    newBlock = create_box(variables.space, x, y, width, height, mass, elasticity, rotation)

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
        obj.apply_impulse_at_local_point((0, -200), variables.force_offset)
        # pymunk.Body.apply_impulse_at_world_point(obj, (0,-250), (obj.position.x, obj.position.y-100))

        # pymunk.Body.apply_impulse_at_world_point(obj, (250,0), (obj.position.x+100, obj.position.y))
    if mode == "down":
        # obj.apply_impulse_at_local_point((0,1000))
        obj.apply_impulse_at_local_point((0, 200), variables.force_offset)

        # pymunk.Body.apply_impulse_at_world_point(obj, (-250,0), (obj.position.x-100, obj.position.y))

def apply_grav_accel(obj):
    planet = None
    for _planet in variables.planets.values():
        planet = _planet.body
        break
    #grav_a = 1 * 10**5 * grav_accel(150, math.hypot(abs(obj.position.x-planet.position.x), abs(obj.position.y-planet.position.y)))
    distance_vector = ((planet.position.x - obj.position.x), (planet.position.y - obj.position.y))
    distance = math.hypot((planet.position.x - obj.position.x), (planet.position.y - obj.position.y))
    grav_a = variables.dt * ((6.6743015 * 10**-11) * 5000000000000000000 / (distance ** 2))
    grav_a_angle = math.atan2(distance_vector[1], distance_vector[0])

    grav_a_vector = (grav_a * math.cos(grav_a_angle), grav_a * math.sin(grav_a_angle))
    variables.current_accel = grav_a_vector[0], grav_a_vector[1]
    #grav_a_vector = (grav_a * (obj.position.x - planet.position.x), grav_a * (obj.position.y - planet.position.y))
    #pymunk.Body.apply_force_at_world_point(obj, (grav_a_vector[0], grav_a_vector[1]), obj.position)
    obj.apply_force_at_local_point((variables.current_accel[0], variables.current_accel[1]))
    #pymunk.Body.update_velocity(obj, grav_a_vector, 1, 1/variables.physics_speed)
def update(physics_speed):
    callAmount = 16
    for _ in range(callAmount):
        variables.space.step((1 / variables.fps * physics_speed) / callAmount)

    variables.dt = variables.clock.tick(variables.fps)
    pygame.display.update()

def update_cooldown():


    # draw(space, screen, draw_options)
    variables.newBlockCooldown += 1
def update_movement():
    if variables.keys[pygame.K_TAB]:
        if variables.tab_pressed == False:

            variables.tab_pressed = True
            variables.selected_index += 1
            if variables.selected_index == len(variables.blocks.keys()):
                variables.selected_index = 0
    else:
        variables.tab_pressed = False
    if variables.keys[pygame.K_w]:
        move_selected("up", variables.blocks[str(variables.selected_index)][1].body)
    if variables.keys[pygame.K_s]:
        move_selected("down", variables.blocks[str(variables.selected_index)][1].body)
    if variables.keys[pygame.K_a]:
        move_selected("left", variables.blocks[str(variables.selected_index)][1].body)
    if variables.keys[pygame.K_d]:
        move_selected("right", variables.blocks[str(variables.selected_index)][1].body)
    if variables.keys[pygame.K_9]:
        print("tab")
        variables.physics_speed = 2000

def lerp_angular_velocity():
    if variables.blocks!= {}:

        selected_obj = variables.blocks[str(variables.selected_index)][1]
        variables.trailPoints.append(selected_obj.body.position)
        if len(variables.trailPoints) > 1000:
            variables.trailPoints.pop(0)
        if len(trailPoints) > 2:
            pygame.draw.lines(variables.screen, variables.white, False, trailPoints, 5)
        apply_grav_accel(selected_obj.body)
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
