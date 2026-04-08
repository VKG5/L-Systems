import bpy
import math

def show_message(message="", title="Info", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def create_spline(curve_data, points, depth, curve_type = 'POLY'):
    if len(points) < 2:
        return

    spline = curve_data.splines.new(type = curve_type)
    spline.points.add(len(points) - 1)

    base_radius = 0.05
    branch_radius = base_radius * (0.7 ** depth)

    for i, p in enumerate(points):
        spline.points[i].co = (p[0], p[1], p[2], 1)

        # taper along branch length
        t = i / max(1, len(points) - 1)
        spline.points[i].radius = branch_radius * (1 - 0.5 * t)

## For generating the actual mesh
def generateCurve(sentence, length = 1.0, angle = 25.0, curve_type = 'POLY'):
    # Optimized mesh generation with UI notifications
    try:
        # Create curve datablock
        curve_data = bpy.data.curves.new(name="LSystemCurve", type='CURVE')
        curve_data.dimensions = '3D'
        curve_data.resolution_u = 2

        curve_obj = bpy.data.objects.new("LSystemCurveObj", curve_data)
        bpy.context.collection.objects.link(curve_obj)

        # State
        curr_pos = (0.0, 0.0, 0.0)
        curr_angle = 0.0

        # Active branch points
        current_points = [curr_pos]

        # Stack stores state ONLY (no history copy)
        stack = []

        def create_spline(points):
            if len(points) < 2:
                return

            spline = curve_data.splines.new(type='POLY')
            spline.points.add(len(points) - 1)

            for i, p in enumerate(points):
                spline.points[i].co = (p[0], p[1], p[2], 1)

        for ch in sentence:

            if ch == '+':
                curr_angle += angle

            elif ch == '-':
                curr_angle -= angle

            elif ch == '[':
                # Save state
                stack.append((curr_pos, curr_angle, current_points))

                # Start a NEW branch from current position
                current_points = [curr_pos]

            elif ch == ']':
                # Finish current branch
                create_spline(current_points)

                if stack:
                    curr_pos, curr_angle, current_points = stack.pop()

                    # IMPORTANT:
                    # Continue parent branch from same position
                    # but DO NOT duplicate history
                    current_points.append(curr_pos)

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

                current_points.append(new_pos)
                curr_pos = new_pos

        # Final spline (main trunk)
        create_spline(current_points)

        # Optional thickness
        curve_data.bevel_depth = 0.02
        curve_data.bevel_resolution = 2

        msg = "L-System generated successfully!"

        ## Debugging
        print(msg)

        show_message(msg, "Success", 'CHECKMARK')

    except Exception as e:
        err_msg = f"Failed to generate L-System: {str(e)}"
        
        ## Debugging
        print(err_msg)
        
        show_message(err_msg, "Error", 'ERROR')
