import bpy
import bpy
import math
       
from . import GetVertices as getVertices
#getVertices = bpy.data.texts["getVertices.py"].as_module()

def cpop(ls):
    try:
        return ls.pop(), True
        
    except IndexError:
        return [], False

## For generating the actual mesh
def generateMesh(str, length, rads):
    ## Setting the correct mode
    getVertices.setMode(bpy.context.active_object, 'OBJECT')

    # Selecting object        
    obj = getVertices.getCurrObj()

    # Toggling Edit Mode (single mode switch at start)
    getVertices.setMode(obj, 'EDIT')

    # Selecting all
    bpy.ops.mesh.select_all(action = 'SELECT')

    # Merging at center for further processing
    bpy.ops.mesh.merge(type = 'CENTER')
    
    # Resetting the vertex selection to origin
    getVertices.selectVertexIndex(obj, 0)
    
    # Initialize BMesh context for efficient mesh operations
    getVertices.initMeshContext(obj)
    
    ## Variable for storing the current angle
    currA = 0
    
    ## Variable for tracking current vertex index (eliminates expensive getCurrVert() calls)
    currVertIdx = 0
    
    ## List for storing vertex indices and angles (stack for branching)
    indexLs = []
    
    try:
        ## Debugging
        #print("\nSTEPS:\n")
        
        for i in range(len(str)):
            ## Special Characters cases
            if(str[i]=='+'):
                currA += rads
                ## Debugging
                #print("Adding Angle")
                
            elif(str[i]=='-'):
                currA -= rads
                ## Debugging
                #print("Subtracting Angle")
                
            elif(str[i]=='['):
                # Pushing the current vertex index and angle to stack (O(1) instead of O(n) with getCurrVert)
                indexLs.append((currVertIdx, currA))
                
            elif(str[i]==']'):
                # Removing the last element (vertex index and angle from stack)
                vert, flag = cpop(indexLs)
                
                if(flag):
                    ## Restore vertex and angle from stack
                    currVertIdx = vert[0]
                    currA = vert[1]
                    # Restore active vertex selection (single mode operation)
                    getVertices.selectVertexIndex(obj, currVertIdx)
                        
            elif(str[i]=='X'):
                continue
                
            ## Consonants for moving forward   
            else:
                x = round( math.cos( math.radians(currA) ), 3 ) * length
                y = round( math.sin( math.radians(currA) ), 3 ) * length
                z = 0
                
                ## TODO : DETERMINE AXIS
                bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(x, y, z)})
                
                # Incrementing vertex index (new vertex created by extrude)
                currVertIdx += 1
                
        bpy.ops.mesh.select_all(action = 'SELECT')
        
        ## Removing close points/doubles
        bpy.ops.mesh.remove_doubles()
            
        bpy.ops.object.mode_set(mode = 'OBJECT')
        
        print("Successfully Generated the Pattern!")
        
    except Exception as inst:
        print("Failed to generate the pattern!", type(inst))