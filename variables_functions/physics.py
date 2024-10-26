
import pygame, time
import pymunk
import pymunk.pygame_util
import math, random, os, json, keyboard, clock

from pygame import Vector2
from pygame.transform import rotate
from pymunk.pygame_util import DrawOptions

from variables_functions import variables
from variables_functions.variables import blocks, physics_loading, joint_distances, physics_speed, cam_offset
from variables_functions import zoomer


def ballistics(current_altitude, velocity, angle, acceleration):
    print("code will be added later")

def distance(x,y):
    return math.hypot(y[0]-x[0], y[1]-x[1])
def angle_of_vector(x, y):
    return math.degrees(math.atan2(-y,x))  # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors/64563327#64563327
def rotate_vector(vector, angle): #https://www.kodeclik.com/how-to-rotate-and-scale-a-vector-in-python/
    (x,y) = vector
    angler = angle
    newx = x*math.cos(angler) - y*math.sin(angler)
    newy = x*math.sin(angler) + y*math.cos(angler)
    return (newx, newy)
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
    variables.space.debug_draw(draw_options)


def create_box(space, x, y, width, height, mass, elasticity, rotation = 0, circle=False, kinematic = False, velocity = (0,0)):
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
    shape.body.velocity = (velocity[0], velocity[1])
    space.add(body, shape)


    return shape
def create_block(image, x, y, width, height, mass, elasticity, rotation=0, override_id=-1, velocity = (0,0)):
    newBlock = create_box(variables.space, x, y, width, height, mass, elasticity, rotation, False, False, velocity)

    newBlockRect = pygame.rect.Rect((0, 0), (width, height))
    newBlockRect.x, newBlockRect.y = x, y
    block_value = override_id
    if override_id == -1:
        block_value = len(variables.blocks.keys())
    variables.blocks[str(block_value)] = [image, newBlock, newBlockRect]
    update_rot(variables.blocks)
    variables.newBlockCooldown = 0

    return str(block_value)

def create_joint(block1, block2):
    #block1[1].filter = pymunk.ShapeFilter(group=variables.num_of_rockets)
    #block2[1].filter = pymunk.ShapeFilter(group=variables.num_of_rockets)
    variables.joints.append([block1, block2, block1[1].body.position - block2[1].body.position])
def remove_joint(block1, block2):
    variables.joints.remove([block1, block2, block1[1].body.position - block2[1].body.position])
def remove_joint_from_block(block1):
    for joint in variables.joints:
        if joint[0] == block1:
            variables.joints.remove(joint)
            break
def decouple():
    for block in variables.parts_blocks:
        if block[0] == "decoupler":
            remove_joint_from_block(block)
def get_save_data():
    data = []
    for obj in blocks.values():
        image = obj[0]
        shape = obj[1]
        body = shape.body
        rect = obj[2]
        data.append([image, shape.body.position.x, shape.body.position.y, rect.width, rect.height, shape.mass, shape.elasticity, body.angle, body.velocity])
    final_data = {
        "selected_index": variables.selected_index,
        "blocks": data
    }
    return final_data

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

    objects = data["blocks"]
    sel_index = data["selected_index"]
    #Overwrites all blocks with the corresponding save file block
    for obj in objects:
        create_block(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], i, obj[8])
        i += 1
    selected_index = sel_index
   # variables.trajectory, variables.trajectory_velocities = simulate_bodies(selected_obj.body.position, selected_obj.mass,
   #                                                                         selected_obj.body.velocity)

    variables.physics_loading = False
    variables.simulated_frames = 999999999 #Ends all simulations
    variables.trajectory = []
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
            #rect.centerx, rect.centery = math.floor(block.body.position.x), math.floor(
            #    block.body.position.y)  # Match rect position to body position

            #https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
            pos_to_blit = math.floor(block.body.position.x), math.floor(
                block.body.position.y)
            pos_on_img = rect.width/2, rect.height/2
            image_rect = image.get_rect(topleft=(pos_to_blit[0] - pos_on_img[0], pos_to_blit[1]-pos_on_img[1]))
            offset_center_to_pivot = pygame.math.Vector2(pos_to_blit) - image_rect.center
            rotated_offset = offset_center_to_pivot.rotate(-blockRotationAngle)

            rotated_image_center = (pos_to_blit[0] - rotated_offset.x, pos_to_blit[1] - rotated_offset.y)
            rotated_image = pygame.transform.rotate(image, blockRotationAngle)
            rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

            zoomer.blit_zoom_rect(rotated_image, rotated_image_rect)
def move_selected(mode, obj):
    obj.torque = 0
    if mode == "right":
        obj.torque = 4500
    if mode == "left":
        obj.torque = -4500
    if mode == "up":
        #obj.velocity += rotate_vector((0,-5), obj.angle)
        obj.apply_force_at_local_point((0,-1000))
    if mode == "down":
        obj.velocity += rotate_vector((0,5), obj.angle)
    obj = variables.blocks[str(variables.selected_index)][1]
    variables.orbital_corrections[str(variables.selected_index)] = [obj.body.position, obj.body.velocity, False]
    trajs,vels = simulate_bodies(obj.body.position, obj.mass, obj.body.velocity, obj.body.angle, obj.body.angular_velocity)
    variables.trajectories[str(variables.selected_index)] = [trajs,vels]
def apply_grav_accel(obj, kinematic = False, timewarp_dt = False, get_vel = False):
    if not get_vel:
        last_obj_angle = obj.angle
        obj.angle = 0
    planet = None
    for _planet in variables.planets.values():
        planet = _planet.body
        break
    dt_use = (1/variables.fps)
    if timewarp_dt:
        pass
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
    if not get_vel:
        if not kinematic:
            obj.apply_force_at_local_point((variables.current_accel[0] * dt_use * variables.fps, variables.current_accel[1] * dt_use * variables.fps))
        else:
            obj.velocity += (round(variables.current_accel[0] * 0.105* variables.physics_speed * force_multiplier, 10), round(variables.current_accel[1] * 0.105 * variables.physics_speed * force_multiplier, 10))
        obj.angle = last_obj_angle
    else:
        return round(variables.current_accel[0] * 0.105 * variables.physics_speed * force_multiplier, 10), round(variables.current_accel[1] * 0.105 * variables.physics_speed * force_multiplier, 10)
    #pymunk.Body.update_velocity(obj, grav_a_vector, 1, 1/variables.physics_speed)
def match_grav_accel(obj, obj_index):
    #variables.current_traj_follow = closest_point(obj.body.position, variables.trajectory)

    if variables.physics_speed <= 1:
        if str(obj_index) in variables.orbital_corrections.keys():
            #In orbital_corrections: each block has three elements in their array:
            #0 -> starting orbit position
            #1 -> starting orbit velocity
            #2 -> bool orbit should correct
            if variables.orbital_corrections[str(obj_index)][2] and distance(variables.orbital_corrections[str(obj_index)][0], obj.body.position) < 25:
                obj.body.position = variables.orbital_corrections[str(obj_index)][0]
                obj.body.velocity = variables.orbital_corrections[str(obj_index)][1]
                variables.orbital_corrections[str(obj_index)][0] = obj.body.position
                variables.orbital_corrections[str(obj_index)][2] = False

                print("correcting orbit")
            if distance(variables.orbital_corrections[str(obj_index)][0], obj.body.position) > 150:
                variables.orbital_corrections[str(obj_index)][2] = True
        apply_grav_accel(obj.body, True)

    # variables.trajectory_follows_indexes[str(obj_index)] -> current traj follow index
    # variables.trajectory_follows[str(obj_index)] -> current traj position to follow
    if variables.physics_speed > 1:
        if str(obj_index) in variables.trajectory_follows.keys():
            #obj.body.velocity = (0,0)
            obj.body.position = variables.trajectory_follows[str(obj_index)][0], variables.trajectory_follows[str(obj_index)][1]
            obj.body.angular_velocity = 0

        if str(obj_index) in variables.trajectories.keys():
            if str(obj_index) in variables.trajectory_follows_indexes.keys():
                if variables.trajectory_follows_indexes[str(obj_index)] < len(variables.trajectories[str(obj_index)][0]):
                    variables.trajectory_follows[str(obj_index)] = variables.trajectories[str(obj_index)][0][int(variables.trajectory_follows_indexes[str(obj_index)])]

                    variables.trajectory_follows_indexes[str(obj_index)] += variables.physics_speed
                    #variables.last_current_traj_follow = variables.current_traj_follow

                else:
                    variables.trajectory_follows_indexes[str(obj_index)] = 0


def simulate_bodies(pos1, mass1, vel1, angle1, anglevel1):

    variables.simulation_body = create_box(variables.space_trajectory, pos1[0], pos1[1], 16, 16, mass1, 0, False, True, False)
    #body2 = create_box(variables.space_trajectory, pos2[0], pos2[1], 5, 5, 20, 0, True, True)
    variables.simulation_body.body.velocity = vel1
    variables.simulation_body.body.angle = angle1
    variables.simulation_body.body.angular_velocity = anglevel1

    variables.simulation_positions = []
    variables.simulation_velocities = []

    variables.simulate_frames = 10000
    variables.simulate_per_frame =200

    variables.simulated_frames = 0
    variables.simulation_active = True
    for _ in range(250):

        apply_grav_accel(variables.simulation_body.body, True, True)
        # body1.body.velocity = (0,5)
        variables.simulation_positions.append(variables.simulation_body.body.position)
        variables.simulation_velocities.append(variables.simulation_body.body.velocity)
        if len(variables.simulation_positions) > 700 and abs(
                distance(variables.simulation_body.body.position, variables.simulation_positions[0]) < 1):
            variables.simulation_active = False
            break
        update_trajectory_sim()
    return variables.simulation_positions, variables.simulation_velocities

def update_trajectory_sim():
    variables.space_trajectory.step(1/variables.fps)


def update(physics_speed):
    #if variables.simulation_active:
    if variables.simulation_active:
        for _ in range(variables.simulate_per_frame):

            apply_grav_accel(variables.simulation_body.body, True, True)
            #body1.body.velocity = (0,5)
            variables.simulation_positions.append(variables.simulation_body.body.position)
            variables.simulation_velocities.append(variables.simulation_body.body.velocity)
            if len(variables.simulation_positions) > 700 and abs(distance(variables.simulation_body.body.position, variables.simulation_positions[0]) < 1):
                variables.simulation_active = False
                break
            update_trajectory_sim()
            variables.simulated_frames += 1
            if variables.simulated_frames >= variables.simulate_frames:
                variables.simulation_active = False
                break


    callAmount = 1
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
       # if variables.selected_obj != None:
        #    trajectory, trajectory_velocities = simulate_bodies(variables.selected_obj.body.position,
       #                                                                         variables.selected_obj.mass,
        #                                                                       variables.selected_obj.body.velocity,
        #                                                                        variables.selected_obj.body.angle,
        #                                                                        variables.selected_obj.body.angular_velocity)
        #    variables.trajectories[str(variables.selected_index)] = [trajectory, trajectory_velocities]
        if variables.keys[pygame.K_SPACE] and variables.space_key_last_pressed != variables.keys[pygame.K_SPACE]:
            variables.engineon = not variables.engineon
            print("engine on")
        variables.space_key_last_pressed = variables.keys[pygame.K_SPACE]
        if variables.keys[pygame.K_r] and variables.r_key_last_pressed != variables.keys[pygame.K_r]:
            variables.rcson = not variables.rcson
        variables.r_key_last_pressed = variables.keys[pygame.K_r]
        if variables.engineon:
            move_selected("up", obj.body)
        #if variables.keys[pygame.K_w] and variables.rcson == True:
       #     move_selected("up", obj.body)
       # if variables.keys[pygame.K_s] and variables.engineon == False and variables.rcson == True:
        #    move_selected("down", obj.body)
        if variables.rcson:
            if variables.keys[pygame.K_a] and variables.rcson == True:
                move_selected("left", obj.body)
            if variables.keys[pygame.K_d] and variables.rcson == True:
                move_selected("right", obj.body)
        if variables.keys[pygame.K_m]:
            decouple()
        if variables.keys[pygame.K_9]:
            variables.physics_speed = 15
            i = 0

            for block in variables.blocks.values():

                body = block[1].body
                if str(i) in variables.trajectories.keys():

                    variables.trajectory_follows_indexes[str(i)] = closest_point(body.position, variables.trajectories[str(i)][0])
                    variables.trajectory_follows[str(i)] = variables.trajectories[str(i)][0][variables.trajectory_follows_indexes[str(i)]]

                i += 1

        if variables.keys[pygame.K_1]:
            i = 0
            for block in variables.blocks.values():
                body = block[1].body
                if str(i) in variables.trajectories.keys():
                    variables.trajectory_follows[str(i)] = closest_point(body.position, variables.trajectories[str(i)][0])
                    trajectory = variables.trajectories[str(i)][0]
                    velocities = variables.trajectories[str(i)][1]
                    body.position = trajectory[variables.trajectory_follows[str(i)]]
                    body.velocity = velocities[variables.trajectory_follows[str(i)]]
                    variables.trajectory_follows_indexes[str(i)] = 0
                i += 1
            variables.physics_speed = 1

def lerp_angular_velocity():
    if variables.blocks!= {}:

        selected_obj = variables.blocks[str(variables.selected_index)][1]
        #variables.trailPoints.append(selected_obj.body.position)
        #if len(variables.trailPoints) > 5000:
        #    variables.trailPoints.pop(0)
        #if len(trailPoints) > 2:
        #    pygame.draw.lines(variables.screen, variables.white, False, trailPoints, 5)
        for joint in variables.joints:
            body1 = joint[0][1].body
            body2 = joint[1][1].body
            dis = rotate_vector(joint[2], body2.angle)
            body1.position = body2.position + dis
            body1.angle = body2.angle
        for traj in variables.trajectories.values():
            trajectory = traj[0]
            to_draw = [(l[0] * variables.zoom[0] + variables.cam_offset[0], l[1] * variables.zoom[1] + variables.cam_offset[1]) for l in trajectory]
            if len(trajectory) > 2:
                pygame.draw.lines(variables.screen, variables.red, False, to_draw, 5)

        i = 0
        for block in variables.blocks.values():
            match_grav_accel(block[1], i)
            #else:
             #   print(block)
            i += 1

        #if timewarp > 1, all joints retain same distance apart

        variables.selected_obj = selected_obj
        if not variables.keys[pygame.K_a] and not variables.keys[pygame.K_d]:
            if abs(selected_obj.body.angular_velocity) > 0.02:
                selected_obj.body.angular_velocity = selected_obj.body.angular_velocity + (0-selected_obj.body.angular_velocity) * 0.05
            else:
                selected_obj.body.angular_velocity = 0

def create_parts():
    #if variables.leftclick:
     #   if variables.newBlockCooldown > 10:  # and pygame.Rect.colliderect(mouseRect, woodRect):
     #       create_block("wood", pygame.mouse.get_pos()[0] / variables.zoom[0], pygame.mouse.get_pos()[1] / variables.zoom[1], 16, 16, 10, 0, 0)
    if variables.rightclick:
        if variables.newBlockCooldown > 10:  # and pygame.Rect.colliderect(mouseRect, stoneRect):
            create_block("stone", pygame.mouse.get_pos()[0] / variables.zoom[0], pygame.mouse.get_pos()[1] / variables.zoom[1], 16, 16, 10, 0, 0)
def update_screen():
   # variables.screen.blit(variables.images["wood"], variables.woodRect)
    #variables.screen.blit(variables.images["stone"], variables.stoneRect)

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
