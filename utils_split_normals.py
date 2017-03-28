import bpy
import array

C = bpy.context
O = bpy.ops

def toggle_smooth_split_normals(obj):
	me = obj.data
	me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	use_auto_smooth = True
	if me.use_auto_smooth:
		use_auto_smooth = False
	
	me.use_auto_smooth = use_auto_smooth


def remove_split_normals(obj):
	me = obj.data
	cl_nors = array.array('f', [0.0] * (len(me.loops) * 3))
	me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	nors_split_set = tuple(zip(*(iter(cl_nors),) * 3))
	me.normals_split_custom_set(nors_split_set)
	me.use_auto_smooth = False


def apply_split_normals(obj):
	me = obj.data
	me.calc_normals_split()
	cl_nors = array.array('f', [0.0] * (len(me.loops) * 3))
	me.loops.foreach_get('normal', cl_nors)
	me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	nors_split_set = tuple(zip(*(iter(cl_nors),) * 3))
	me.normals_split_custom_set(nors_split_set)
	# Enable the use custom split normals data if available
	me.use_auto_smooth = True


bl_objects = C.selected_objects

for obj in bl_objects:
	# Toggle the visibility of the custom vertec normals
	#toggle_smooth_split_normals(obj)
	
	# Remove all custom vertex normal data from this mesh
	remove_split_normals(obj)

	# Apply blender smoothing as custom vertex normals
	#apply_split_normals(obj)