extends Line2D

var positions = []
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func calc_trajectory(pos, planet, mass, vel):
	var traj = simulate_bodies(pos, planet, mass, vel)
	positions = traj[0]
	return traj
func _process(delta):
	var points_to_draw = []
	for point in positions:
		points_to_draw.append(to_local(point))
	self.points = points_to_draw
func round_place(num,places):
	return (round(num*pow(10,places))/pow(10,places))
func calc_grav_accel(pos, planet, mass):
	
	var dt_use = 1.0/60.0
	var force_multiplier = 1.0
	#grav_a = 1 * 10**5 * grav_accel(150, math.hypot(abs(obj.position.x-planet.position.x), abs(obj.position.y-planet.position.y)))
	var distance_vector = planet - pos
	var distance_ = float(abs(planet.distance_to(pos)))
	var grav_a = dt_use * mass * ((6.6743015 * (10.0**-11.0)) * 50000000000000000) / (distance_ ** 2.0)
	var grav_a_angle = atan2(distance_vector.y, distance_vector.x)

	var grav_a_vector_0 = grav_a * cos(grav_a_angle)
	var grav_a_vector_1 = grav_a * sin(grav_a_angle)
	var current_accel = Vector2(grav_a_vector_0, grav_a_vector_1)
	return Vector2(current_accel.x * 0.105* 60.0 * force_multiplier, current_accel.y * 0.105* 60.0 * force_multiplier)


func simulate_bodies(pos1, planet_pos, mass1, vel1):

	#variables.simulation_body = create_box(variables.space_trajectory, pos1[0], pos1[1], 16, 16, mass1, 0, False, False, True)
	var simulation_body = [pos1, vel1]

	#body2 = create_box(variables.space_trajectory, pos2[0], pos2[1], 5, 5, 20, 0, True, True)
	var simulation_positions = []
	var simulation_velocities = []
	var simulate_frames = 10000
	var simulation_active = true
	for i in range(simulate_frames):
		simulation_positions.append(simulation_body[0])
		simulation_velocities.append(simulation_body[1])
		var new_vel = calc_grav_accel(simulation_body[0], planet_pos, mass1)
		simulation_body[1] += new_vel * (1.0/60.0)
		simulation_body[0] += simulation_body[1]
		# body1.body.velocity = (0,5)
		
		if len(simulation_positions) > 1000 and simulation_body[0].distance_to(simulation_positions[0]) < 1000:
			simulation_active = false
			break
	return [simulation_positions,simulation_velocities]
