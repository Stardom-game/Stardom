extends Node2D
@export var craft : PackedScene
@export var craftParent : Node
var added = false
# Called when the node enters the scene tree for the first time.
func _ready():
	Engine.time_scale = 1


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if !added:
		create_craft("test", Vector2(-2000,0))
	if Input.is_action_just_pressed("save"):
		var to_save = []
		for craft in Variables.crafts:
			to_save.append([craft.name, craft.global_position, craft.orbit_path_index, craft.orbit_path, craft.orbit_vel_path,\
			craft.last_velocity, craft.velocity_change, craft.angular_vel])
		Variables.save_data = to_save
	if Input.is_action_just_pressed("load"):
		clear_crafts()
		for craft in Variables.save_data:
			create_craft(craft[0],craft[1], true, craft[2], craft[3], craft[4], craft[5], craft[6], craft[7])
func clear_crafts():
	for child in craftParent.get_children():
		child.free()
func create_craft(name_, pos=Vector2(-2000,0), override_properties = false, \
orbit_override_index = -1, \
orbit_override_path = [], orbit_override_vel_path = [],last_velocity=Vector2(0,0), \
velocity_change=Vector2(0,0), angular_vel=0):
	var new_craft = craft.instantiate()
	new_craft.global_position = pos
	craftParent.add_child(new_craft)
	new_craft.name = name_
	Variables.crafts.append(new_craft)
	if override_properties:
		new_craft.last_velocity = last_velocity
		new_craft.velocity_change = velocity_change
		new_craft.angular_vel = angular_vel
	if orbit_override_path != [] and orbit_override_index != -1:
		new_craft.override_orbit(orbit_override_index, orbit_override_path, orbit_override_vel_path)
	added = true
