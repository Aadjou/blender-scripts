import bpy
import array

C = bpy.context
O = bpy.ops

def toggle_split_normals(obj):
	# Toggle the use of custom split normals. Custom split normals are preserved.
	me = obj.data
	# This will override blender smoothing for the entire mesh. 
	# (False -> hard shaded, True -> smooth shaded)
	#me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	use_auto_smooth = True
	if me.use_auto_smooth:
		use_auto_smooth = False
	
	me.use_auto_smooth = use_auto_smooth


def remove_split_normals(obj):
	# Remove all custom split normal information from the mesh.
	me = obj.data
	cl_nors = array.array('f', [0.0] * (len(me.loops) * 3))
	# This will override blender smoothing for the entire mesh. 
	# (False -> hard shaded, True -> smooth shaded)
	#me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	nors_split_set = tuple(zip(*(iter(cl_nors),) * 3))
	me.normals_split_custom_set(nors_split_set)
	me.use_auto_smooth = False


def apply_split_normals(obj):
	# Write the blender internal smoothing as custom split vertex normals
	me = obj.data
	me.calc_normals_split()
	cl_nors = array.array('f', [0.0] * (len(me.loops) * 3))
	me.loops.foreach_get('normal', cl_nors)
	me.polygons.foreach_set('use_smooth', [False] * len(me.polygons))
	nors_split_set = tuple(zip(*(iter(cl_nors),) * 3))
	me.normals_split_custom_set(nors_split_set)
	# Enable the use custom split normals data
	me.use_auto_smooth = True


bl_objects = C.selected_objects

for obj in bl_objects:
	# Toggle the visibility of the custom vertex normals
	#toggle_split_normals(obj)
	
	# Remove all custom vertex normal data from this mesh
	remove_split_normals(obj)

	# Apply blender smoothing as custom vertex normals
	#apply_split_normals(obj)