extends CharacterBody2D


const SPEED = 300.0
var calculator = null
var orbit_path = []
var orbit_vel_path = []
var orbit_path_index = -1
var angular_vel = 0
var velocity_change = Vector2(0,0)
var last_velocity = Vector2(0,0)
var last_rotation = 0
var jerk
func _ready():
	calculator = $GravAccelCalculator
func closest_point(pos, arr):
	var i = 0
	var out = null
	var out_index = -1
	var dis = 999
	for point in arr:
		if pos.distance_to(point) < dis:
			out_index = i
			dis = pos.distance_to(point)
		i += 1
	return out_index
func _physics_process(delta):
	# Add the gravity.
	var planet_pos = Vector2(0,0)
	velocity = Vector2(0,0)
	if (len(orbit_path) < orbit_path_index+500) or orbit_path_index==-1:
		calculate_orbit_path(delta)
		orbit_path_index = 0
	if Input.is_action_just_pressed("move_up") or Input.is_action_just_pressed("move_down"):
		velocity_change = last_velocity
		jerk = 9000* delta
	if Input.is_action_pressed("move_up"):
		velocity_change += Vector2(0,-5000*delta * 0.005).rotated(rotation)
		jerk += 9000 * delta
		orbit_path_index = 0
	if Input.is_action_pressed("move_down"):
		velocity_change += Vector2(0, 5000*delta * 0.005).rotated(rotation)
		jerk += 9000 * delta
		orbit_path_index = 0
	if Input.is_action_pressed("move_left"):
		angular_vel = -5
	elif Input.is_action_pressed("move_right"):
		angular_vel = 5
	else:
		angular_vel = 0
	#if Input.is_action_just_released("move_up"):
	#	velocity_change = Vector2(0,0)
	#	last_rotation = rotation
	
	
	if Input.is_action_pressed("move_up") or Input.is_action_pressed("move_down"):
		calculate_orbit_path(delta)
	
	#angular_vel += (0-angular_vel) *25 *  delta
	rotation_degrees += angular_vel
	if orbit_path_index < len(orbit_path) and orbit_path_index != -1:
		var target = orbit_path[orbit_path_index]
		if position.distance_to(target) < 15:
			orbit_path_index += 1
			target = orbit_path[orbit_path_index]
		
		var speed = orbit_path[orbit_path_index].distance_to(orbit_path[orbit_path_index+1])
		print(speed)
		velocity += (target-position).normalized() * delta * 1000 * speed
		
		last_velocity = orbit_vel_path[orbit_path_index]
	
	
	move_and_slide()
func calculate_orbit_path(delta):
	var planet_pos = Vector2(0,0)
	velocity += velocity_change
	var traj = calculator.calc_trajectory(global_position, planet_pos, 500.0, self.velocity)
	orbit_path = traj[0]
	orbit_vel_path = traj[1]
	#move_and_slide()
	
	
