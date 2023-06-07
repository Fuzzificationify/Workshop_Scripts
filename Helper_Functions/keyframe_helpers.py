# Helper function for dealing with Keyframes

import maya.cmds as mc
import maya.mel as mel

def has_keys(obj):
    if mc.keyframe(obj, q=1):
        return True
    else:
        return False

def get_anim_curve():
    anim_curve = mc.keyframe(q=1, name=1, sl=1)


def get_key_times(sel, sl_keys=True):
    # Should work on obj selection or anim_curve selection
    # Using int(sl_keys) to toggle selection flag
    all_times = mc.keyframe(sel, q=1, sl=int(sl_keys), timeChange=1) or []

    if all_times == []:
        print("No keys on selection")
        return None, None, None
        
    first_time, last_time = min(all_times), max(all_times)

    return first_time, last_time, all_times
    
    
def get_key_indexs(anim_curve):
    
    all_key_indxs = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1) or []
    if all_key_indxs == []:
        return None
    
    first_key_indx, last_key_indx = all_key_indxs[0], all_key_indxs[-1]

    return first_key_indx, last_key_indx, all_key_indxs
    
    
def check_timeslider_sel():

    aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    highlight = mc.timeControl(aTimeSlider, q=True, rangeVisible=True)
    
    if highlight: return True
    else: return False
    
    
def get_timeslider_sel_range():
    
    aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
    timeRange = mc.timeControl(aTimeSlider, q=True, rangeArray=True)
    start_time, end_time = timeRange[0], timeRange[1]
    
    if not mc.timeControl(aTimeSlider, q=True, rangeVisible=True):
        return None
    
    return start_time, end_time
    
    
def get_graphEditor_channel_sel():

    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)
    
    return graphEditorObjects
    
    
def get_scene_range():
    minTime = mc.playbackOptions(q=1, minTime=1)
    maxTime = mc.playbackOptions(q=1, maxTime=1)

    return minTime, maxTime

def get_minmax_scene_range():
    minTime = mc.playbackOptions(q=1, animationStartTime=1)
    maxTime = mc.playbackOptions(q=1, animationEndTime=1)
    
    return minTime, maxTime

def select_current_frame_key():
    # Select Graph Editor Keys on Current Frame
    time = mc.currentTime(q=1)

    # Get GraphEditor Outliner Channel Selection
    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

    mc.selectKey(clear=1)
    mc.selectKey(graphEditorObjects, replace=1, time=(time,))

def select_neighbour_key(direction):
    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

    k = mc.findKeyframe(graphEditorObjects, which=direction)
    mc.selectKey(graphEditorObjects, time=(k, k))


# Copy values from goal to arrow, like a controlled Bake
def matrix_constrain(goal, arrow, frame_range, rotate_order, onlyKeys=True):
    
    time_range = range(int(frame_range[0]), int(frame_range[-1] + 1))
    
    if onlyKeys:
        time_range = get_keyframes_in_range(goal, frame_range)
     
    for f in time_range:
         
        # Get WorldSpace Matrix of the goal object (the control)
        goal_matrix = om2.MMatrix(cmds.getAttr( goal + '.worldMatrix', time=f ) )
        
        # Find Arrow's Parent's World Inverse Matrix (the locator)
        arrow_parent = mc.listRelatives(arrow, parent=1)[0]
        inverse_parent_matrix = om2.MMatrix(cmds.getAttr( arrow_parent + '.worldInverseMatrix', time=f ) )
        
        # Multiply Goal matrix by inverse parent's matrix to find values in Arrow's local space
        # And convert to MTransformationMatrix for deconstruction
        local_matrix = om2.MTransformationMatrix( (goal_matrix * inverse_parent_matrix) )
        
        translation_vals = local_matrix.translation(om2.MSpace.kWorld)
        rotation_vals = local_matrix.rotation() # Rotation values in Radions
        
        rotation_vals.reorderIt(rotate_order) # Apply Goal's rotation order to new Matrix
        angles = [math.degrees(angle) for angle in (rotation_vals.x, rotation_vals.y, rotation_vals.z)]
        
        
        mc.setKeyframe(arrow, at='tx', value = translation_vals[0], time = (f) )
        mc.setKeyframe(arrow, at='ty', value = translation_vals[1], time = (f) )
        mc.setKeyframe(arrow, at='tz', value = translation_vals[2], time = (f) )
                      
        mc.setKeyframe(arrow, at='rx', value = angles[0], time = (f) )
        mc.setKeyframe(arrow, at='ry', value = angles[1], time = (f) )
        mc.setKeyframe(arrow, at='rz', value = angles[2], time = (f) )
