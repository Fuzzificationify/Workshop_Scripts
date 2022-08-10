import maya.cmds as mc

## Frame Before Snap ##
def anim_snap_get(anim_curve, snap_direction=''):

    # Get list of key's values
    selKeyVal = mc.keyframe(anim_curve, q=1, sl=1, valueChange=1)

    # Get relevant key indices
    firstKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[0]
    lastKeyIndex = mc.keyframe(anim_curve, q=1, sl=1, indexValue=1)[-1]
    

    # Get value of preceding key selection's index
    if snap_direction == 'before':
        prevKeyIndex = firstKeyIndex - 1
        prevKeyVal = mc.keyframe(anim_curve, q=1, index=(prevKeyIndex, prevKeyIndex), valueChange=1)
        valDiff = prevKeyVal[0] - selKeyVal[0]

    elif snap_direction == 'after':
        nextKeyIndex = lastKeyIndex + 1
        nextKeyVal = mc.keyframe(anim_curve, q=1, index=(nextKeyIndex, nextKeyIndex), valueChange=1)
        valDiff = nextKeyVal[0] - selKeyVal[-1]


    mc.keyframe(anim_curve, e=1, index=(firstKeyIndex, lastKeyIndex), relative=1, valueChange=valDiff)


def anim_snap_before():
    animCurves = mc.keyframe(q=1, n=1)

    for anim_curve in animCurves:
        anim_snap_get(anim_curve, snap_direction='before')

def anim_snap_after():
    animCurves = mc.keyframe(q=1, n=1)

    for anim_curve in animCurves:
        anim_snap_get(anim_curve, snap_direction='after')




def before_snap():
    valDiff = prevKeyVal[0] - selKeyVal[0]
    return valDiff

def after_snap():
    valDiff = nextKeyVal[0] - selKeyVal[-1]
    return valDiff
