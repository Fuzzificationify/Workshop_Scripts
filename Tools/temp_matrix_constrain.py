from Helper_Functions import keyframe_helpers

import math
import maya.cmds as mc
import maya.api.OpenMaya as om
from datetime import datetime


class UndoContext(object):
    def __enter__(self):
        mc.undoInfo(openChunk=True)
    def __exit__(self, *exc_info):
        mc.undoInfo(closeChunk=True)

def delete_defunct_blend(ctrls):
    for ctrl in ctrls:
        if mc.attributeQuery('blendParent1', node=ctrl, exists=1):
            mc.deleteAttr(ctrl, attribute='blendParent1')

def get_current_frame():
    frame = mc.currentTime(q=1)
    return frame

def get_keyframes_in_range(ctrl, frame_range):
    all_times = mc.keyframe(ctrl, q=1, time=(frame_range))
    float_key_times = list(set(all_times))
    int_key_times = map(int, float_key_times)
    
    return int_key_times

def clear_keys(objs, frame_range):
    mc.cutKey(objs, attribute = "t", time = frame_range)
    mc.cutKey(objs, attribute = "r", time = frame_range)

def rotate_ordering(ctrl, loc):
    rotOrder = mc.getAttr(ctrl + '.rotateOrder')
    mc.cutKey(loc, at='rotateOrder') # Delete keys if exist so change sticks
    mc.setAttr(loc + ".rotateOrder", rotOrder)
    
    return rotOrder

def setup_parent_space(control):
    child_temp_loc = mc.spaceLocator()[0]
    control_parent = mc.listRelatives(control, p=1)[0]
    mc.parent(child_temp_loc, control_parent)

    return child_temp_loc

def jnt_orient_extract(jnt):
    JO_vals = mc.getAttr(jnt + '.jointOrient')[0]
    radians_xfo = om.MVector( math.radians(JO_vals[0]), math.radians(JO_vals[1]), math.radians(JO_vals[2]) )
    
    jnt_orient_mtx = om.MTransformationMatrix()
    jnt_orient_mtx.setRotation(om.MEulerRotation(radians_xfo) )
    
    return jnt_orient_mtx

def jnt_rotation(goal_mtx, arrow, jnt_orient_mtx, rotate_order=0):
    # This is an extra step if the arrow is a joint with a joint orient.
    # Multiplying the joint orient matrix by the arrow's parent matrix, THEN inversing the result
    # !!!!!!!! No Time=f?#
    arrow_parent_mtx = om.MMatrix(mc.getAttr(arrow + '.parentMatrix')) 

    sum_mtx = om.MTransformationMatrix( jnt_orient_mtx.asMatrix() * arrow_parent_mtx)
    sum_iv_mtx = sum_mtx.asMatrix().inverse()

    return sum_iv_mtx

def for_translation(goal_mtx, arrow, time_range, flags):

    inverse_parent_mtx = om.MMatrix(mc.getAttr(arrow + '.parentInverseMatrix', **flags))

    local_mtx = om.MTransformationMatrix( (goal_mtx * inverse_parent_mtx) )
    translation_vals = local_mtx.translation(om.MSpace.kWorld)
    
    return translation_vals

def matrix_constrain(goal, arrow, start_time, end_time, rotate_order, onlyKeys):
    translation_override = 0
    flags = {}

    time_range = range(int(start_time), int(end_time + 1))

    if onlyKeys:
        time_range = get_keyframes_in_range(goal, (start_time, end_time))
     
    for f in time_range:
        # Only use -time flag if more than a single frame
        if len(time_range) > 2:
            flags["time"] = f

        # Get WorldSpace Matrix of the goal object (the control)
        goal_mtx = om.MMatrix( mc.getAttr( goal + '.worldMatrix', **flags) )

        if mc.nodeType(arrow) == "joint":
            jnt_orient_mtx = jnt_orient_extract(arrow)
            inverse_parent_mtx = jnt_rotation(goal_mtx, arrow, jnt_orient_mtx, rotate_order)
            translation_vals = for_translation(goal_mtx, arrow, time_range, flags)

            translation_override = 1
            
        else:

            inverse_parent_mtx = om.MMatrix( mc.getAttr(arrow + '.parentInverseMatrix', **flags) )

        # Multiply Goal matrix by inverse parent's matrix to find values in Arrow's local space
        # And convert to MTransformationMatrix for deconstruction
        local_mtx = om.MTransformationMatrix( (goal_mtx * inverse_parent_mtx) )
        
        if translation_override != 1:
            translation_vals = local_mtx.translation(om.MSpace.kWorld)
        
        # Apply Goal's rotation order to new Matrix
        reordered_rotation = local_mtx.rotation().reorderIt(rotate_order) 
        rotation_vals = [math.degrees(x) for x in reordered_rotation]
        
        # Set keys
        mc.setKeyframe(arrow, at='tx', value = translation_vals[0], time = (f) )
        mc.setKeyframe(arrow, at='ty', value = translation_vals[1], time = (f) )
        mc.setKeyframe(arrow, at='tz', value = translation_vals[2], time = (f) )
                      
        mc.setKeyframe(arrow, at='rx', value = rotation_vals[0], time = (f) )
        mc.setKeyframe(arrow, at='ry', value = rotation_vals[1], time = (f) )
        mc.setKeyframe(arrow, at='rz', value = rotation_vals[2], time = (f) )

    
def set_constraint_keys(ctrl, frame_range):
    mc.setKeyframe(ctrl, at='blendParent1', value = 0, time = (frame_range[0]-1))
    mc.setKeyframe(ctrl, at='blendParent1', value = 1, time = (frame_range[0]))
    
    mc.setKeyframe(ctrl, at='blendParent1', value = 1, time = (frame_range[-1]))
    mc.setKeyframe(ctrl, at='blendParent1', value = 0, time = (frame_range[-1]+1))

def axis_to_skip_if_locked(ctrl, loc):
    t_xyz_skip_list = []
    r_xyz_skip_list = []

    for axis in ['.tx', '.ty', '.tz']:
        its_locked = mc.getAttr(ctrl + axis, lock=1)
        if its_locked:
            t_xyz_skip_list.append(axis[-1].lower())
    for axis in ['.rx', '.ry', '.rz']:
        its_locked = mc.getAttr(ctrl + axis, lock=1)
        if its_locked:
            r_xyz_skip_list.append(axis[-1].lower())

    # mc.orientConstraint(loc, ctrl, skip=xyz_skip_list, mo=0)
    # if xyz_skip_list != []:
    #     print("Skip List: ", xyz_skip_list)
    return t_xyz_skip_list, r_xyz_skip_list

def delete_constraints(constraints):
    mc.delete(constraints, constraints=1)
    
 def main(controls, locators, start_time, end_time, onlyKeys=True):
    clear_keys(locators, (start_time, end_time))
    delete_defunct_blend(controls)
    constraint_list = []
    for ctrl, loc, in zip(controls, locators):

        rotate_order = rotate_ordering(ctrl, loc)
        matrix_constrain(ctrl, loc, start_time, end_time, rotate_order, onlyKeys)
        t_skip_list, r_skip_list = axis_to_skip_if_locked(ctrl, loc)
        pCon = mc.parentConstraint(loc, ctrl, mo=0, skipTranslate=t_skip_list, skipRotate=r_skip_list)[0]
        constraint_list.append(pCon)
        set_constraint_keys(ctrl, (start_time, end_time))
    
    mc.filterCurve(locators, filter='euler')
            
    return (start_time, end_time), rotate_order, constraint_list


def bake_back(ctrls, locs, start_time, end_time, onlyKeys=True, protectorKeys=True):
    if protectorKeys:
        # Set protector keys
        mc.setKeyframe(ctrls, at=['t', 'r'], time = (start_time) )
        mc.setKeyframe(ctrls, at=['t', 'r'], time = (end_time - 1) )

    # Delete keys on controls inside range 
    clear_keys(ctrls, (start_time, end_time))
    
    # Bake
    for loc, ctrl in zip(locs, ctrls):
        rotate_order = rotate_ordering(ctrl, loc) # Kinda redundant 
        matrix_constrain(loc, ctrl, start_time, end_time, rotate_order, onlyKeys)

    # Delete Constraint
    child_con = mc.listRelatives(ctrls, children=1, type='constraint')
    mc.delete(child_con, constraints=1)
    
    mc.filterCurve(ctrls, filter='euler')
    
    delete_defunct_blend(ctrls)

    # Shitty way to refresh viewport
    if start_time == end_time:
        current_time = mc.currentTime(q=1)
        mc.currentTime(current_time-1)
        mc.currentTime(current_time) 
