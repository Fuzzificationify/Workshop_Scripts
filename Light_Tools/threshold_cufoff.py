# Threshold cutoff

import maya.cmds as mc

sel = mc.ls(sl=1)
keyframes = mc.keyframe(sel, q=1)
keyframes = sorted(set(keyframes))

for i in keyframes:
    val = mc.getAttr(sel + ".translateY", time=i)
    
    if val < 4.7:
    mc.currentTime(i)
    mc.setAttr(sel + ".translateY", time=i, 4.7)
    mc.setKeyframe(sel + ".translateY")
