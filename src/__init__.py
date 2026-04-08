# To register script as an add-on
bl_info = {
    'name' :'L-System Generator',
    'author' : 'Varun Kumar Gupta',
    'version' : (1,2,0),
    'blender' : (3,3,0),
    'location' : '3D Viewport',
    'description' : 'L-System Generator based on Axioms and Strings',
    'warning' : '',
    'wiki_url' : '',
    'category' : 'UI',
}

import bpy
import os
from bpy.props import *

from . import LSystems as lsystems
#lsystems = bpy.data.texts["l-systems.py"].as_module()


'''
Main Code
'''
# ======= RULE PROPERTY GROUP =======
class LSystemRule(bpy.types.PropertyGroup):
    # Dynamic Rule container instead of fixed rules
    rule: bpy.props.StringProperty(
        name = "Rule",
        description = "Format A : AB",
        default = "F:FX"
    )


# ======= HELPER FUNCTIONS =======
def ensureRulesCount(scene, target):
    rules = scene.rules_collection

    # Add rules if needed
    while(len(rules) < target):
        rules.add()

    # Remove extra rules
    while(len(rules) > target):
        rules.remove(len(rules) - 1)


# Callback for numRules (Auto update UI)
def updateRules(self, context):
    ensureRulesCount(context.scene, context.scene.numRules)


## Callback for updating presets
def updatePreset(self, context):
    if context.scene.presetVal != 'custom':
        presetClass(context, context.scene.presetVal)


# ======= GLOBAL VARIABLES =======
# Properties/Inputs for our add-on
# Format : ("Name", bpy.props.<propertyName> (Int, String, Enum, Float, etc.)
PROPS = [
    ## Presets
    ("presetVal", bpy.props.EnumProperty( name = 'Presets ',
                                          description = 'Some presets for you to play around with',
                                          items = [
                                            ('custom', 'None', 'Custom Pattern'),
                                            ('kochSnow', 'Koch Snowflake', 'A variant of the Koch curve to create a snowflake'),
                                            ('koch', 'Koch Curve', 'A variant of the Koch curve which uses only right angles'),
                                            ('sierpinski', 'Sierpinski Triangle', 'The Sierpinski triangle'),
                                            ('sierpinskiCurve', 'Sierpinski Arrowhead Curve', 'Sierpiński arrowhead curve'),
                                            ('dragon', 'Dragon Curve', 'The dragon curve'),
                                            ('binaryTree', 'Fractal Binary Tree', 'A fractal binary tree'),
                                            ('fractalPlant', 'Fractal Plant', 'Barnsley fern'),
                                            ('tree3d', '3D Tree', '3D Tree with'),
                                            ('bush3d', '3D Bush', '3D Bush'),
                                            ('coral3d', '3D Coral', '3D Coral Reef Structure')
                                            ],
                                         update=updatePreset)),

    ("genType", bpy.props.EnumProperty( name = 'Generation Type',
                                        description = 'What kind of geometry to generate for the defined l-system',
                                        items = [
                                            ('MESH', "Mesh", "Generate as mesh"),
                                            ('CURVE', "Curve", "Generate as curve")
                                        ],
                                        default = 'MESH')),

    ("axiom", bpy.props.StringProperty( name = 'Axiom',
                                        description = 'The starting point of our L-System',
                                        default = "F" )),
                                        
    ("generations", bpy.props.IntProperty( name = 'Generations',
                                           description = 'Iterations/Generations : How many times to run the loop',
                                           default = 3, min = 1, max = 100)),
    
    ("numRules", bpy.props.IntProperty( name = 'Number of Rules',
                                        description = 'The number of rules in your L-System',
                                        default = 1, min = 1, max = 20,
                                        update = updateRules)),
                                        
    ("angle", bpy.props.FloatProperty( name = 'Angle',
                                        description = 'Angle by which each segment will rotate (Degrees)',
                                        default = 60, min = 0, max = 360)),
                                        
    ("length", bpy.props.FloatProperty( name = 'Length',
                                        description = 'The length of each generated segment',
                                        default = 1, min = 0.05, max = 10)),
]


## Class for pre-setting values
def presetClass(context, preset):
    scn = context.scene

    match preset:
        # ======= 2D PRESETS =======
        case 'kochSnow':
            scn.axiom = 'F--F--F'
            scn.generations = 5
            scn.angle = 60
            scn.length = 1.0
            rules = ['F:F+F--F+F']
        
        case 'koch':
            scn.axiom = 'F'
            scn.generations = 3
            scn.angle = 90
            scn.length = 1.0
            rules = ['F:F+F-F-F+F']
            
        case 'sierpinski':
            scn.axiom = 'F-G-G'
            scn.generations = 4
            scn.angle = 120
            scn.length = 1.0
            rules = ['F:F-G+F+G-F', 'G:GG']
            
        case 'sierpinskiCurve':
            scn.axiom = 'F'
            scn.generations = 4
            scn.angle = 60
            scn.length = 1.0
            rules = ['F:G-F-G', 'G:F+G+F']
        
        case 'dragon':
            scn.axiom = 'F'
            scn.generations = 10
            scn.angle = 90
            scn.length = 1.0
            rules = ['F:F+G', 'G:F-G']
        
        case 'binaryTree':
            scn.axiom = 'F'
            scn.generations = 7
            scn.angle = 45
            scn.length = 1.0
            rules = ['F:G[-F]+F', 'G:GG']
        
        case 'fractalPlant':
            scn.axiom = 'X'
            scn.generations = 6
            scn.angle = 25
            scn.length = 1.0
            rules = ['X:F+[[X]-X]-F[-FX]+X', 'F:FF']
        
        # ======= 3D PRESETS =======
        case 'tree3d':
            scn.axiom = 'F'
            scn.generations = 5
            scn.angle = 22.5
            scn.length = 1.0
            rules = ['F:F[+F][&F][-F][^F]F']
        
        case 'bush3d':
            scn.axiom = 'F'
            scn.generations = 4
            scn.angle = 20
            scn.length = 1.0
            rules = ['F:F[+F]F[&F]F[-F]F[^F]']
        
        case 'coral3d':
            scn.axiom = 'F'
            scn.generations = 4
            scn.angle = 25
            scn.length = 1.0
            # \\ is required for backslash (Escape character)
            rules = ['F:F[+F]/F[\\\\F]&F[^F]-F']
        
        case default:
            return
        
    ## Apply rules dynamically
    scn.numRules = len(rules)
    ensureRulesCount(scn, scn.numRules)

    for i, r in enumerate(rules):
        scn.rules_collection[i].rule = r
                    
                            
'''
Class that calls code
'''
# Operator Class
class generateLSystems(bpy.types.Operator):
    bl_idname = "opr.generate_l_system"
    bl_label = "Generate L-System(s)"
    bl_description = "Generate an L-System based on Axioms, Generations and parameters provided"
    
    def execute(self, context):
        ## Debugging
        #print(params)
        
        # Pre-setting the values, handled in callback function
        # if(context.scene.presetVal != 'custom'):
        #     presetClass(context, context.scene.presetVal)
        
        ## Collect rules dynamically
        passRules = [r.rule for r in context.scene.rules_collection if r.rule.strip()]
        
        lsystems.generateLSystem( bpy.context.scene.axiom, 
                                  bpy.context.scene.generations, 
                                  len(passRules), 
                                  bpy.context.scene.angle, 
                                  bpy.context.scene.length,
                                  bpy.context.scene.genType,
                                  passRules )
        
        return {'FINISHED'}


''' 
Class that generates the UI
'''
# UI Class
class demoUI(bpy.types.Panel):
    # Creates side panel in the 3D Viewport under Misc
    bl_idname = "VIEW3D_PT_L_Systems"
    bl_label = "L-Systems"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lumi_Tools" 
    
    # To draw/create the actual panels
    def draw(self, context):
        # Generating fields that will be visible in the Panel
        layout = self.layout
        col = layout.column(align = True)
        
        layout.label(text="L-Systems Parameters: ")
        col = layout.column(align = True)
              
        for(prop_name, _) in PROPS:
            row = col.row(align = True)
            row.prop(context.scene, prop_name)    
        
        layout.label(text="L-System Rules: ", icon = 'ERROR')
        layout.label(text="Enter the rules in format 'A(Rule Variable):AB(Actual Rule)'")
        
        col = layout.column(align = True)
        col.scale_y = 1.5

        ## Debugging
        #print(bpy.context.scene.numRules)

        ## Dynamic Rules UI
        for i, rule in enumerate(context.scene.rules_collection):
            row = col.row(align=True)
            row.prop(rule, "rule", text=f"Rule {i+1}")
        
        col = layout.column(align = True)
        col.scale_y = 2
        col.operator("opr.generate_l_system", text="Generate System", icon = 'DISCLOSURE_TRI_RIGHT')

        ## Grammar helper
        box = layout.box()
        box.label(text="3D Grammar:")
        box.label(text="F/G: Forward")
        box.label(text='X: Skip')
        box.label(text="+ - : Z rotation")
        box.label(text="& ^ : X rotation")
        box.label(text="\\ / : Y rotation")
        box.label(text="[ ] : Branching")
        
        
'''
Driver Code
This part registers the classes with Blender and makes the add-on actually work!
Don't skip this part!!
'''

# To auomate the installation and uninstallation of multiple scripts/classes
# Just add the class names in this list
CLASSES = [
    LSystemRule,
    generateLSystems,
    demoUI
]    


# To register all the classes
def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    # Registering the Properties before the classes
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
        
    bpy.types.Scene.rules_collection = bpy.props.CollectionProperty(type=LSystemRule)

    # Delay initializing the rules
    def init_rules():
        if bpy.context.scene:
            ensureRulesCount(bpy.context.scene, bpy.context.scene.numRules)
        return None
    
    bpy.app.timers.register(init_rules, first_interval=0.1)
        

# To unregister all the classes
def unregister():
    # Remove collection first
    del bpy.types.Scene.rules_collection

    # Un-registering the Properties before the classes
    for(prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
    
    # Unregister classes last (Reverse order)
    for cls in CLASSES:
        bpy.utils.unregister_class(cls)

        
# Calling the register or constructor
if __name__ == "__main__":
    register()
