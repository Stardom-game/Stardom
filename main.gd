extends Node2D
@export var craft : PackedScene
var added = false
# Called when the node enters the scene tree for the first time.
func _ready():
	Engine.time_scale = 1


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	if !added:
		var new_craft = craft.instantiate()
		new_craft.name = "spacecraft_alpha"
		new_craft.global_position = Vector2(-2000,0)
		add_child(new_craft)
		Variables.crafts.append(new_craft)
		added = true
