import maya.cmds as mc

source, target = mc.ls(sl=1)

mc.copyKey(source, attribute=('tx', 'ty', 'tz', 'rx', 'ry', 'rz'))

layer_name = source + "_aLyr"

mc.animLayer(layer_name)
mc.select(target, replace=True)
mc.animLayer(layer_name, e=1, addSelectedObjects=1, override=1)

mc.pasteKey(target, animLayer=layer_name)


# Delete Constraint on target
child_con = mc.listRelatives(target, children=1, type='constraint')
mc.delete(child_con, constraints=1)
