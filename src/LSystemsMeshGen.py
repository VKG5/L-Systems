import bpy
import bmesh
import math

def show_message(message="", title="Info", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

## For generating the actual mesh
def generateMesh(sentence, length = 1.0, angle = 60.0):
    # Optimized mesh generation with UI notifications
    try:
        obj = bpy.context.active_object
        if obj is None or obj.type != 'MESH':
            raise Exception("Active object must be a mesh")

        # Create new mesh (avoid editing existing one)
        mesh = bpy.data.meshes.new("LSystemMesh")
        new_obj = bpy.data.objects.new("LSystemObject", mesh)
        bpy.context.collection.objects.link(new_obj)

        ## New approach using a one shot generation instead of using BMesh
        # Geometry Data
        vertices = []
        edges = []

        # State
        curr_pos = (0.0, 0.0, 0.0)
        curr_angle = 0.0

        # Stack for branching
        stack = []

        # Add initial vertex
        vertices.append(curr_pos)
        curr_index = 0

        # Loop
        for ch in sentence:
            if ch == '+':
                curr_angle += angle

            elif ch == '-':
                curr_angle -= angle

            elif ch == '[':
                stack.append((curr_pos, curr_angle, curr_index))

            elif ch == ']':
                if stack:
                    curr_pos, curr_angle, curr_index = stack.pop()

            elif ch == 'X':
                continue

            else:
                dx = math.cos(math.radians(curr_angle)) * length
                dy = math.sin(math.radians(curr_angle)) * length

                new_pos = (
                    curr_pos[0] + dx,
                    curr_pos[1] + dy,
                    curr_pos[2]
                )

                vertices.append(new_pos)
                new_index = len(vertices) - 1

                edges.append((curr_index, new_index))

                curr_pos = new_pos
                curr_index = new_index

        # Create mesh in one shot
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
