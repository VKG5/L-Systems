##==== x SCRIPT USED FOR GETTING THE VERTICES OF ANY OBJECT x ====##
# BMesh for Edit Mode
import bpy, bmesh

## Function for setting the correct context
def setMode(obj, smode):
    """Efficiently switch object mode only if needed"""
    if obj.mode != smode:
        bpy.ops.object.mode_set(mode = smode)

## Selecting and setting current object active
def getCurrObj():
    """Get and activate current object"""
    obj = bpy.context.active_object
    obj.select_set(True)
    return obj

## Getting the last currently selected vertex (optimized with caching)
def getCurrVert(obj):
    """Get index of currently selected vertex using BMesh"""
    # Ensure we're in EDIT mode (caller should maintain this)
    if obj.mode != 'EDIT':
        setMode(obj, 'EDIT')
    
    # bmesh pointer to manipulate vertices
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Iterate through vertices to find selected one
    for index, vert in enumerate(bm.verts):
        ## Debugging
        #print(vert.co.to_tuple(), index)
        
        # Checking if the current vertex is selected
        if(vert.select):
            return index
        
    # In case no vertex is active/selected
    return None

## Selecting a particular vertex (optimized - single mode operation)
def selectVertexIndex(obj, index):
    """Select vertex by index - operates in EDIT mode to avoid mode switching"""
    # Ensure vertex selection mode is active
    bpy.ops.mesh.select_mode(type = 'VERT')
    
    # Get BMesh reference (assumes we're in EDIT mode via caller)
    if obj.mode != 'EDIT':
        setMode(obj, 'EDIT')
    
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Deselect all vertices using BMesh (more efficient than bpy.ops)
    for vert in bm.verts:
        vert.select = False
    
    # Select the target vertex by index using BMesh (avoids mode switch)
    bm.verts.ensure_lookup_table()
    bm.verts[index].select = True
    
    # Update mesh (required when modifying BMesh directly)
    bmesh.update_edit_mesh(obj.data)
    
    ## Debugging
    #print("Selected vertex %d" % index)

## Initialize mesh generation context (call once at start of generateMesh)
def initMeshContext(obj):
    """Initialize proper mode and BMesh context at start of mesh generation"""
    # Ensure we're in EDIT mode and get BMesh reference
    setMode(obj, 'EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    return bm