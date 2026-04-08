import bpy
import math
from mathutils import Vector, Matrix

def show_message(message="", title="Info", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

## For generating the actual mesh
def generateMesh(sentence, length = 1.0, angle = 60.0):
    # Optimized mesh generation with UI notifications
    try:
        # Create mesh
        mesh = bpy.data.meshes.new("LSystemMesh")
        obj = bpy.data.objects.new("LSystemObject", mesh)
        bpy.context.collection.objects.link(obj)

        ## New approach using a one shot generation instead of using BMesh
        # Geometry Data
        vertices = []
        edges = []

        # State - Modified for 3D Generation
        # curr_pos = (0.0, 0.0, 0.0)
        # curr_angle = 0.0
        pos = Vector((0.0, 0.0, 0.0))
        transform = Matrix.Identity(3)

        # Stack for branching
        stack = []

        # Add initial vertex
        vertices.append(pos.copy())
        curr_index = 0

        angle_rad = math.radians(angle)

        # Loop
        for ch in sentence:
            if ch == 'F':
                direction = transform @ Vector((0, length, 0))
                new_pos = pos + direction

                vertices.append(new_pos.copy())
                new_index = len(vertices) - 1

                edges.append((curr_index, new_index))

                pos = new_pos
                curr_index = new_index

            elif ch == '+':  # Yaw (Z axis)
                transform = transform @ Matrix.Rotation(angle_rad, 3, 'Z')

            elif ch == '-':
                transform = transform @ Matrix.Rotation(-angle_rad, 3, 'Z')

            elif ch == '&':  # Pitch down (X axis)
                transform = transform @ Matrix.Rotation(angle_rad, 3, 'X')

            elif ch == '^':  # Pitch up
                transform = transform @ Matrix.Rotation(-angle_rad, 3, 'X')

            elif ch == '\\':  # Roll left (Y axis)
                transform = transform @ Matrix.Rotation(angle_rad, 3, 'Y')

            elif ch == '/':  # Roll right
                transform = transform @ Matrix.Rotation(-angle_rad, 3, 'Y')

            elif ch == '[':
                stack.append((pos.copy(), transform.copy(), curr_index))

            elif ch == ']':
                if stack:
                    pos, transform, curr_index = stack.pop()

            else:
                continue

        mesh.from_pydata(vertices, edges, [])
        mesh.update()

        # Merging by distance
        import bmesh
        
        bm = bmesh.new()
        bm.from_mesh(mesh)

        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        bm.to_mesh(mesh)
        bm.free()

        ## Logging
        msg = "L-System generated successfully!"

        ## Debugging
        print(msg)

        show_message(msg, "Success", 'CHECKMARK')

    except Exception as e:
        ## Logging
        err_msg = f"Failed to generate L-System: {str(e)}"
        
        ## Debugging
        print(err_msg)
        
        show_message(err_msg, "Error", 'ERROR')
