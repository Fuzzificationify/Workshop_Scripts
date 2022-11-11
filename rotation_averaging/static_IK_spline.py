# Static IK Spline

import maya.cmds as mc

ctrls = mc.ls(sl=1)
jnt_list = []
loc_list = []
i = 0
mc.select(cl=1)
for each in ctrls:

    j_xform = mc.xform(each, q=1, ws=1, t=1)
    jnt = mc.joint(p=j_xform)

    jnt_list.append(jnt)

    if i >= 1:
        mc.joint(jnt_list[i - 1], e=1, zso=1, sao='ydown', oj='xyz')
    i = i + 1

for n, each in enumerate(ctrls):

    loc = mc.spaceLocator()
    loc_list.append(loc)
    mc.parent(loc, jnt_list[n], relative=1)

# for j, jnt in enumerate(jnt_list):
    # if j < (len(jnt_list)-1):
        # mc.aimConstraint(loc_list[j+1], ctrls[j], aimVector=(-1, 0, 0), upVector=(0, 1, 0), skip="x")
    # else:
        # mc.orientConstraint(jnt, ctrls[j], mo=1, skip="x")
        
for j, jnt in enumerate(jnt_list):

    mc.orientConstraint(jnt, ctrls[j], mo=1, skip="x")

mc.select(jnt_list[0], jnt_list[-1])
mc.ikHandle(jnt_list[0], jnt_list[-1], solver='ikSplineSolver', twistType='easeInOut', numSpans=4)
