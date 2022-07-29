## Frame Before Snap ##
import maya.cmds as mc

def anim_snap(anim_curve):

    # Get list of key's values
    selKeyVal = mc.keyframe(anim_curve, q=1, sl=1, valueChange=1)

    # Get relevant key indices
    firstKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[0]
    lastKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[-1]
    prevKeyIndex = firstKeyIndex - 1

    # Get value of preceding key selection's index
    prevKeyVal = mc.keyframe(anim_curve, q=1, index=(prevKeyIndex,prevKeyIndex), valueChange=1)

    valDiff = prevKeyVal[0] - selKeyVal[0]

    mc.keyframe(anim_curve, e=1, index=(firstKeyIndex, lastKeyIndex), relative=1, valueChange=valDiff)



animCurves = mc.keyframe(q=1, n=1)

for anim_curve in animCurves:
    anim_snap(anim_curve)



## Frame After Snap ##
import maya.cmds as mc

def anim_snap(anim_curve):

    # Get list of key's values
    selKeyVal = mc.keyframe(anim_curve, q=1, sl=1, valueChange=1)

    # Get relevant key indices
    firstKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[0]
    lastKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[-1]
    nextKeyIndex = lastKeyIndex + 1

    # Get value of preceding key selection's index
    nextKeyVal = mc.keyframe(anim_curve, q=1, index=(nextKeyIndex,nextKeyIndex), valueChange=1)

    valDiff = nextKeyVal[0] - selKeyVal[-1]

    mc.keyframe(anim_curve, e=1, index=(firstKeyIndex, lastKeyIndex), relative=1, valueChange=valDiff)



animCurves = mc.keyframe(q=1, n=1)

for anim_curve in animCurves:
    anim_snap(anim_curve)
