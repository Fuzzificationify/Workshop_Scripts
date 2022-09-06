import maya.cmds as mc

ctrls = mc.ls(sl=1)
rots = []

for each in ctrls:
    rot = mc.getAttr(each + ".rz")
    rots.append(rot)
    
avg = sum(rots) / len(rots)

for each in ctrls:
    mc.setAttr(each + ".rz", avg)
    
