# This script shows how to get all connected faces of a bmesh

import bpy
import bmesh


# Simple - get all linked faces
def get_linked_faces(f):
    
    if f.tag:
        # If the face is already tagged, return empty list
        return []
    
    # Add the face to list that will be returned
    f_linked = [f]
    f.tag = True
    
    # Select edges that link two faces
    edges = [e for e in f.edges if len(e.link_faces) == 2]
    for e in edges:
        # Select all firs-degree linked faces, that are not yet tagged
        faces = [elem for elem in e.link_faces if not elem.tag]
        
        # Recursively call this function on all connected faces
        if not len(faces) == 0:
            for elem in faces:
                # Extend the list with second-degree connected faces
                f_linked.extend(get_linked_faces(elem))

    return f_linked


""" Get linked faces 
    Args:
        f ('BMFace') - the current face to check for linked faces
    Kwargs:
        stack ('int') - the current recursive stack count.
        max_angle ('float') - the maximum angle for connected faces in radian
    Returns: 
        The connected faces by max angle threshold, material-id, 
        without exceeding max stack trace
"""
def get_linked_faces(f, stack=0, max_angle=3.1416, match_material=False):
    # Fixme: Find non-recursive alternative 
    # Make pretty
    if f.tag:
        return []

    f_linked = [f]
    m_idx = f.material_index
    f.tag = True
    # Select edges that link two faces
    edges = [e for e in f.edges if len(e.link_faces) == 2]
    for e in edges:
        faces = [elem for elem in e.link_faces if not elem.tag]
        if not len(faces) == 0:
            angle = e.calc_face_angle_signed()
            if angle <= max_angle:
                if match_material:
                    for elem in faces:
                        if f.material_index is m_idx:
                            # Recursive
                            if stack < 900:
                                f_linked.extend(get_linked_faces(elem, stack=stack + 1, max_angle=max_angle, match_material=match_material))
                            else:
                                print('Stopped recursive call, else it might exceed maximum stack count.')
                else:
                    for elem in faces:
                        # Recursive
                        if stack < 900:
                            f_linked.extend(get_linked_faces(elem, stack=stack + 1, max_angle=max_angle, match_material=match_material))
                        else:
                            print('Stopped recursive call, else it might exceed maximum stack count.')
                            
    return f_linked

def main():
    obj = bpy.context.selected_objects[0]

    # change mode to editmode
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)

    bm.faces.ensure_lookup_table()
    linked_faces = get_linked_faces(bm.faces[0])
    print(linked_faces)
    
    # Do something with the linked faces ...
    
    bm.free()
    
main()
