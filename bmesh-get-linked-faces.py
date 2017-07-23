# This script shows how to get all connected faces of a bmesh

import bpy
import bmesh


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
