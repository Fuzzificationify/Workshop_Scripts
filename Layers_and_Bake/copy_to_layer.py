# Paste the first object's animation onto a new animation layer of the second
# Because the script just copies keys it will only work on objs in the same space

import maya.cmds as mc

source, target = mc.ls(sl=1)
dup_onto_layer(source, target)

def dup_onto_layer(source, target):

    mc.copyKey(source, attribute=('tx', 'ty', 'tz', 'rx', 'ry', 'rz'))

    layer_name = source + "_aLyr"

    mc.animLayer(layer_name)
    mc.select(target, replace=True)
    mc.animLayer(layer_name, e=1, addSelectedObjects=1, override=1)

    mc.pasteKey(target, animLayer=layer_name)

    # Delete Constraint on target
    child_con = mc.listRelatives(target, children=1, type='constraint')
    mc.delete(child_con, constraints=1)



# WIP: New version using my Matrix function
# Makes temp loator in target's parent space to match transforms when copy / pasting
def thing():
    from My_Tools import temp_timed_constraints
    from Layers_and_Bake import copy_to_layer
    reload(copy_to_layer)
    reload(temp_timed_constraints)

    my_guy = mc.polyCube()[0]
    boss = 'pSphere3'
    temp_loc = temp_timed_constraints.setup_parent_space(boss)


    goal = 'pSphere3_loc'
    arrow = temp_loc
    start_time = 1
    end_time = 120
    rotate_order = 0
    onlyKeys = 0

    temp_timed_constraints.matrix_constrain(goal, arrow, start_time, end_time, rotate_order, onlyKeys)

    copy_to_layer.dup_onto_layer(temp_loc, boss)
