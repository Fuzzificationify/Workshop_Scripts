##  Here and Before  ##
import maya.cmds as mc

animCurveNames = mc.keyframe(q=1, n=1)

try:
    currentKey = int(mc.keyframe(q=1, sl=1)[0])
    firstKey = mc.findKeyframe(animation="keys", which="first")

except:
    currentKey = mc.currentTime(q=1)
    firstKey = mc.findKeyframe(animation="keysOrObjects", which="first")


mc.selectKey(clear=1)
for curv in animCurveNames:
    mc.selectKey(curv, add=1, k=1, time=(currentKey, firstKey))




##  Here and After  ##
import maya.cmds as mc

animCurveNames = mc.keyframe(q=1, n=1)

try:
    currentKey = int(mc.keyframe(q=1, sl=1)[0])
    lastKey = mc.findKeyframe(animation="keys", which="last")

except:
    currentKey = mc.currentTime(q=1)
    lastKey = mc.findKeyframe(animation="keysOrObjects", which="last")


mc.selectKey(clear=1)
for curv in animCurveNames:
    mc.selectKey(curv, add=1, k=1, time=(currentKey, lastKey))
