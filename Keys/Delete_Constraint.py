import maya.cmds as mc

selObj = mc.ls(sl=1)

# Delete Constraint
child_con = mc.listRelatives(selObj, children=1, type='constraint')
mc.delete(child_con, constraints=1)
