#Simple Average

import maya.cmds as mc

def simple_average(*arg):
    ctrls = arg
    print(ctrls)
    rotx = []
    roty = []
    rotz = []

    for each in ctrls:
        rx = mc.getAttr(each + ".rx")
        ry = mc.getAttr(each + ".ry")
        rz = mc.getAttr(each + ".rz")
        
        rotx.append(rx)
        roty.append(ry)
        rotz.append(rz)
        
    avg_x = sum(rotx) / len(rotx)
    avg_y = sum(roty) / len(roty)
    avg_z = sum(rotz) / len(rotz)

    for each in ctrls:
        mc.setAttr(each + ".rx", avg_x)
        mc.setAttr(each + ".ry", avg_y)
        mc.setAttr(each + ".rz", avg_z)
    
    
    
full_sel = mc.ls(sl=1)

for ctrl_a, ctrl_b in zip(full_sel[0::1], full_sel[1::1]):
    
    simple_average(ctrl_a, ctrl_b)
