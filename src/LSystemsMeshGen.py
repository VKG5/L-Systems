import bpy
import bmesh
import math

def show_message(message="", title="Info", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

## For generating the actual mesh
def generateMesh(sentence, length, angle):
    # Optimized mesh generation with UI notifications
    try:
        obj = bpy.context.active_object
        if obj is None or obj.type != 'MESH':
            raise Exception("Active object must be a mesh")

        # Ensure edit mode ONCE
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')

        bm = bmesh.from_edit_mesh(obj.data)

        # Clear existing geometry
        bm.clear()

        # Create initial vertex
        curr_vert = bm.verts.new((0.0, 0.0, 0.0))

        # State
        curr_angle = 0.0

        # Stack for branching
        stack = []

        # Cache for trig
        cos_cache = {}
        sin_cache = {}

        def get_dir(a):
            if a not in cos_cache:
                rad = math.radians(a)
                cos_cache[a] = math.cos(rad)
                sin_cache[a] = math.sin(rad)
            return cos_cache[a], sin_cache[a]

        # Main loop
        for ch in sentence:
            if ch == '+':
                curr_angle += angle
                ## Debugging
                #print("Adding Angle")

            elif ch == '-':
                curr_angle -= angle
                ## Debugging
                #print("Subtracting Angle")

            elif ch == '[':
                # Pushing the current vertex index and angle to stack
                stack.append((curr_vert, curr_angle))

            elif ch == ']':
                # Removing the last element (vertex index and angle from stack)
                if stack:
                    curr_vert, curr_angle = stack.pop()

            elif ch == 'X':
                continue
            
            ## Consonants for moving forward
            else:
                dx, dy = get_dir(curr_angle)

                new_vert = bm.verts.new((
                    curr_vert.co.x + dx * length,
                    curr_vert.co.y + dy * length,
                    curr_vert.co.z
                ))

                bm.edges.new((curr_vert, new_vert))
                curr_vert = new_vert

        # Cleanup
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)

        # Update mesh once
        bmesh.update_edit_mesh(obj.data)

        bpy.ops.mesh.select_all(action='SELECT')

        msg = "L-System generated successfully!"

        ## Debugging
        print(msg)

        show_message(msg, "Success", 'CHECKMARK')

    except Exception as e:
        err_msg = f"Failed to generate L-System: {str(e)}"
        
        ## Debugging
        print(err_msg)
        
        show_message(err_msg, "Error", 'ERROR')
