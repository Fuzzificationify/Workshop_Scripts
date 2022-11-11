import maya.cmds as mc

obj = mc.ls(sl=1)
name = mc.keyframe(obj, q=1, n=1, sl=1)
keys = mc.keyframe(obj, q=1, sl=1)

mc.filterCurve(name, f="simplify", startTime=keys[0], endTime=keys[-1], timeTolerance=0.15)
