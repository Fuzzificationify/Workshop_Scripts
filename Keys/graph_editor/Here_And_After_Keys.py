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

# If there's a key selection, run just on those curves
try:
    animCurveNames = mc.keyframe(q=1, n=1)

    currentKey = int(mc.keyframe(q=1, sl=1)[0])
    lastKey = mc.findKeyframe(animation="keys", which="last")

    mc.selectKey(clear=1)
    for curv in animCurveNames:
        mc.selectKey(curv, add=1, k=1, time=(currentKey, lastKey))

# If there's no key selection, use graph Channel selection and current time
except:
    graphEditorObjects = mc.selectionConnection('graphEditor1FromOutliner', q=1, object=1)

    currentKey = mc.currentTime(q=1)
    lastKey = mc.findKeyframe(animation="keysOrObjects", which="last")

    mc.selectKey(clear=1)
    for curv in graphEditorObjects:
        mc.selectKey(curv, add=1, k=1, time=(currentKey, lastKey))

